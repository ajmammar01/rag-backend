# app/services/vector_db.py
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from fastapi import HTTPException
import os

# 1. Initialize the persistent client pointing to your local directory
# This creates a folder named 'chroma_db' in your project root
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 2. Select the local embedding model (defaults to all-MiniLM-L6-v2)
embedding_function = OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)
def save_chunks_to_vector_store(collection_name: str, token_split_texts: list[str]) -> int:
    """
    Takes a list of text chunks, embeds them locally, and saves them to ChromaDB.
    Returns the total number of documents currently in the collection.
    """
    # 3. Get or create the collection with our embedding machine tied to it
    chroma_collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=embedding_function
    )
    
    # 4. Generate unique string IDs for every single text chunk [ "0", "1", "2" ... ]
    ids = [str(i) for i in range(len(token_split_texts))]
    
    # 5. Push them into the local database file structure
    chroma_collection.add(ids=ids, documents=token_split_texts)
    
    # 6. Return the updated total count to confirm it worked
    return chroma_collection.count()



def query_retrieval(collection_name: str, queries: list[str], n_results: int = 10) -> list[str]:
    """
    Queries the local ChromaDB collection for the most relevant text chunks based on the input query.
    Returns a list of the top n_results matching text chunks.
    """
    # 1. Get the collection by name
    try:    
        chroma_collection = chroma_client.get_collection(name=collection_name)
    except Exception:
        raise HTTPException(status_code=404, detail="Collection not found. Please upload the PDF first to create the collection.")
    
    # 2. Perform a similarity search using the embedding function
    results = chroma_collection.query(
        query_texts=queries,
        n_results=n_results
    )
    
    # 3. Extract and return the matching documents (text chunks)
    # Because Multi-Query returns a list of lists, we flatten and use dict.fromkeys() 
    # to preserve ordering while eliminating duplicate chunks.
    raw_documents = [doc for sublist in results['documents'] for doc in sublist]
    retrieved_documents = list(dict.fromkeys(raw_documents))
    return retrieved_documents
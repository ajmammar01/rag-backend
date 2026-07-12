from fastapi import APIRouter, UploadFile, File
from app.services.pdf_worker import extract_text_from_pdf, chunk_text
from pydantic import BaseModel
from app.services.vector_db import save_chunks_to_vector_store, query_retrieval
from app.services.reranker import rerank_documents
from app.services.llm_client import expand_query, rag


class QueryRequest(BaseModel):
    question: str
    collection_name: str

    
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF, extract its text, split it into chunks,
    and save those chunks natively to ChromaDB.
    """

    # Read uploaded file as bytes
    file_bytes = await file.read()

    # Extract text from PDF
    text = extract_text_from_pdf(file_bytes)

    # Split text into embedding-friendly chunks
    chunks = chunk_text(text)

    # Clean and sanitize the filename to use as a unique ChromaDB collection name
    # (Removes spaces, extensions, and forces lowercase)
    collection_name = file.filename.replace(".pdf", "").replace(" ", "_").lower()

    # Save the chunks natively into your local Chroma DB database directory
    total_database_records = save_chunks_to_vector_store(collection_name, chunks)

    return {
        "status": "success",
        "filename": file.filename,
        "collection_created": collection_name,
        "characters_extracted": len(text),
        "chunks_created": len(chunks),
        "total_database_records": total_database_records,
        "preview": chunks[0] if chunks else ""
    }


@router.post("/query")
async def query(request: QueryRequest):
    """
    Accepts a user query, expands it into multiple variations,
    retrieves relevant chunks from ChromaDB, reranks them,
    and finally uses RAG to generate a final answer.
    """

    # Step 1: Expand the user's query into multiple variations
    expanded_queries = expand_query(request.question)

    # Step 2: Retrieve relevant chunks from ChromaDB for each expanded query
    retrieved_chunks = query_retrieval(collection_name=request.collection_name, queries=expanded_queries)

    # Step 3: Rerank the retrieved chunks based on relevance to the original query
    reranked_chunks = rerank_documents(original_query=request.question, unique_documents=retrieved_chunks)

    # Step 4: Use RAG to generate a final answer based on the reranked chunks
    final_answer = rag(query=request.question, retrieved_chunks=reranked_chunks)

    return {
        "original_query": request.question,
        "expanded_queries": expanded_queries,
        "retrieved_chunks": retrieved_chunks,
        "reranked_chunks": reranked_chunks,
        "final_answer": final_answer
    }
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder('BAAI/bge-reranker-base')


def rerank_documents(original_query: str, unique_documents: list[str], top_n: int = 3) -> list[str]:
    """
    Scores retrieved documents against the original user query using a Cross-Encoder,
    sorts them by relevance, and returns the top_n best chunks.
    """
    # 1. Create the pairs matching every document against the original user question
    pairs = [[original_query, doc] for doc in unique_documents]
    
    # 2. Get the numerical relevance scores from the model
    scores = cross_encoder.predict(pairs)
    
    # 3. Zip documents and scores together so they stay locked together during sorting
    scored_docs = list(zip(unique_documents, scores))
    
    # 4. Sort the zipped list based on the score (x[1]) in descending order (highest score first)
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    # 5. Extract just the sorted text chunks, slicing down to the top_n winners
    reranked_top_chunks = [doc for doc, score in scored_docs]
    
    return reranked_top_chunks[:top_n]
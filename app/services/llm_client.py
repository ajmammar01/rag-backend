from openai import OpenAI

client = OpenAI()



def call_llm(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Calls the LLM with a system prompt and user prompt, returning the model's response.

    Args:
        system_prompt (str): The system-level instructions for the model.
        user_prompt (str): The user's query or input.
        model (str): The model to use (default is "gpt-4o-mini").

    Returns:
        str: The model's response.
    """
    

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()


def expand_query(query: str,  model: str = "gpt-4o-mini", num_queries: int=3) -> list[str]:
    """
    Expands a user's query with multiquery expansion using the LLM.
    """

    system_prompt = (
        f"You are a business intelligence assistant. Breakdown or generate {num_queries} "
        "different variations or sub-questions related to the user's query. "
        "These variations should explore different semantic angles (e.g., if they ask about revenue, "
        "ask about segments, drivers, or regional performance). "
        "Output each query on a new line. Do not include numbers, bullets, or explanations."
    )

    output = call_llm(system_prompt=system_prompt, user_prompt=query, model=model)

    queries = [q.strip() for q in output.split("\n") if q.strip()]

    if query not in queries:
        queries.insert(0, query)

    return queries


def rag(query: str, retrieved_chunks: list[str]):
    """
    Performs Retrieval-Augmented Generation (RAG) by combining the user's query with retrieved chunks.
    """

    system_prompt = (
        "You are a helpful assistant that answers questions based on provided context. "
        "Use the context to answer the question. If the context does not contain the answer, "
        "respond with 'I don't know.'"
    )

    context = "\n\n".join(retrieved_chunks)

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    answer = call_llm(system_prompt=system_prompt, user_prompt=user_prompt)

    return answer
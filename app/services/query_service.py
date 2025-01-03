from app.services.retriever_service import retrieve_relevant_chunks
from app.utils.embedding import embed_query
from app.utils.response_generation import generate_response


def process_query(query: str) -> str:
    query_embedding = embed_query(query)
    retrieved_docs = retrieve_relevant_chunks(query_embedding)
    context = " ".join(retrieved_docs)
    response = generate_response(query, context)
    return response


if __name__ == "__main__":
    query = "France"
    response = process_query(query)
    print("Query:", query)
    print("Response:", response)

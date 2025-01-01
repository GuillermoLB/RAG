from app.utils.embedding import get_embeddings
from app.utils.response_generation import generate_response
from app.repos.sql.vector_repo import search_vectors

def process_query(query: str) -> str:
    query_embedding = get_embeddings(query)
    retrieved_docs = search_vectors(query_embedding)
    context = " ".join(retrieved_docs)
    response = generate_response(query, context)
    return response

if __name__ == "__main__": 
    query = "France"
    response = process_query(query)
    print("Query:", query)
    print("Response:", response)
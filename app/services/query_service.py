from app.models.embedding_model import get_embeddings
from app.models.generation_model import generate_response
from app.database.relational_db import search_vectors

def process_query(query: str) -> str:
    # Step 1: Embed the query
    query_embedding = get_embeddings(query)
    
    # Step 2: Retrieve documents
    retrieved_docs = search_vectors(query_embedding)
    
    # Step 3: Generate response
    context = " ".join(retrieved_docs)
    response = generate_response(query, context)
    return response

if __name__ == "__main__": 
    query = "What is the capital of France?"
    response = process_query(query)
    print("Query:", query)
    print("Response:", response)
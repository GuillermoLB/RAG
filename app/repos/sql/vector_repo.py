import numpy as np
from app.database.models import Chunk
from app.dependencies import get_db


def search_vectors(query_embedding: np.ndarray, top_k: int = 5) -> list:

    db = next(get_db())
    query_embedding = np.array(query_embedding).reshape(1, -1)
    
    # Retrieve all chunks and their embeddings
    chunks = db.query(Chunk).all()
    chunk_embeddings = np.array([chunk.embedding for chunk in chunks])
    
    # Compute cosine similarity between query embedding and chunk embeddings
    similarities = np.dot(chunk_embeddings, query_embedding.T).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    # Retrieve the most similar document contents
    top_chunks = [chunks[i].content for i in top_indices]
    return top_chunks
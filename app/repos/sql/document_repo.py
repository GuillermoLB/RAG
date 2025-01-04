import numpy as np
from sqlalchemy.orm import Session

from app.domain.models import Chunk
from app.dependencies import get_db


# Method to store a new document along with its chunks
def store_document(db: Session, title: str):
    # Store the document
    db_document = Document(title=title)
    db.add(db_document)
    db.commit()
    return db_document


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

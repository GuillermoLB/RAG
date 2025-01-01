import numpy as np
from sqlalchemy.orm import Session
from app.database.models import Base, Document, Chunk
from app.dependencies import get_db

# Method to store a new document along with its chunks
def store_document(db: Session, title: str, chunks: list):
    # Store the document
    db_document = Document(title=title)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Store the chunks
    for chunk in chunks:
        chunk_content = chunk['chunk_text']
        chunk_embedding = chunk['embedding']
        db_chunk = Chunk(document_id=db_document.id, content=chunk_content, embedding=chunk_embedding)
        db.add(db_chunk)
    
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
import os
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from app.database.models import Base, Document, Chunk

# Load the .env file
load_dotenv()

# Access environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# Create the SQLAlchemy engine
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        chunk_serialized_text = chunk['serialized_text']
        chunk_embedding = chunk['embedding']
        db_chunk = Chunk(document_id=db_document.id, content=chunk_content, embedding=chunk_embedding)
        db.add(db_chunk)
    
    db.commit()
    return db_document

def store_chunk(db: Session, document_id: int, content: str, serialized_text: str, embedding):
    # Store the chunk
    db_chunk = Chunk(document_id=document_id, content=content, serialized_text=serialized_text, embedding=embedding)
    db.add(db_chunk)
    db.commit()
    return db_chunk

def search_vectors(query_embedding: np.ndarray, top_k: int = 5) -> list:
    """
    Search for the most similar vectors in the database.

    Args:
        query_embedding (np.ndarray): The query embedding vector.
        top_k (int): The number of top similar vectors to retrieve.

    Returns:
        list: A list of the most similar document contents.
    """
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

# Function to drop the database tables
def drop_db():
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped.")

# Function to initialize the database and create tables
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

# Function to retrieve and print stored documents
def get_stored_documents():
    db = SessionLocal()
    documents = db.query(Document).all()
    for document in documents:
        print(f"Document ID: {document.id}, Title: {document.title}")
        for chunk in document.chunks:
            print(f"  Chunk ID: {chunk.id}, Content: {chunk.content}, Serialized Text: {chunk.serialized_text}, Embedding: {chunk.embedding}")

if __name__ == "__main__":
    drop_db()
    init_db()
    get_stored_documents()
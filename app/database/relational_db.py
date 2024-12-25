import os
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
        db_chunk = Chunk(document_id=db_document.id, content=chunk_content)
        db.add(db_chunk)
    
    db.commit()
    return db_document

def store_chunk(db: Session, document_id: int, content: str):
    # Store the chunk
    db_chunk = Chunk(document_id=document_id, content=content)
    db.add(db_chunk)
    db.commit()
    return db_chunk

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
            print(f"  Chunk ID: {chunk.id}, Content: {chunk.content}")

if __name__ == "__main__":
    drop_db()
    init_db()
    get_stored_documents()
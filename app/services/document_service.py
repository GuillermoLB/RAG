from app.utils.preprocessing import preprocess_text
from app.utils.chunking import chunk_document
from app.utils.embedding import embed_chunks
from app.schemas import DocumentCreate, ChunkCreate
from app.dependencies import get_db
from app.repos.sql.document_repo import store_document
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
data_file_path = os.getenv('DATA_FILE_PATH')

def ingest_document(db: Session):
    document = preprocess_text(data_file_path)
    chunks = chunk_document(document)
    embedded_chunks = embed_chunks(chunks)
    store_document(db, data_file_path, embedded_chunks)

if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    ingest_document(db)
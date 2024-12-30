from app.utils.preprocessing import preprocess_text
from app.schemas import DocumentCreate, ChunkCreate
from app.database.relational_db import get_db, store_document
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
data_files_path = os.getenv('DATA_FILES_PATH')

async def ingest_document(db: Session):
    chunk_data = preprocess_text(data_files_path)
    chunks = [ChunkCreate(**chunk) for chunk in chunk_data]
    document = DocumentCreate(title="Sample Document", chunks=chunks)
    store_document(db, document)

if __name__ == "__main__":
    ingest_document()
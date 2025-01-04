import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repos.sql.document_repo import store_document
from app.services import retriever_service
from app.utils.chunking import chunk_document
from app.utils.embedding import embed_chunks
from app.services.extraction_service import extract_text
from langchain_core.documents import Document as LCDocument
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector

# Load environment variables from .env file
load_dotenv()

# Reload environment variables to ensure the latest values are used
load_dotenv(override=True)
data_file_path = os.getenv("DATA_FILE_PATH")
embed_model_id = os.getenv("EMBED_MODEL_ID")

# Initialize the embeddings object
embeddings = HuggingFaceEmbeddings(model_name=embed_model_id)

def extract_document(db: Session):
    document = extract_text(data_file_path)
    split_document_and_index_chunks(db, document, embeddings)
    store_document(db, document)

def split_document_and_index_chunks(
    session: Session,
    document: LCDocument,
    embeddings: HuggingFaceEmbeddings
):
    # Your implementation here
    pass


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    extract_document(db)

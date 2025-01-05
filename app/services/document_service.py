import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services import retriever_service
from app.services.extraction_service import extract_text
from langchain_core.documents import Document as LCDocument
from langchain_community.embeddings import HuggingFaceEmbeddings

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

def split_document_and_index_chunks(
    session: Session,
    document: LCDocument,
    embeddings: HuggingFaceEmbeddings
):
    chunks = retriever_service.split_text_into_chunks(document)
    retriever_service.index_chunks(chunks, embeddings)


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    extract_document(db)

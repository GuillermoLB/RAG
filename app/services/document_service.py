from uuid import uuid4
from fastapi import UploadFile
from loguru import logger
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.dependencies import get_db, get_settings
from app.domain.schemas import Document
from app.repos.sql import document_repo
from app.services import retriever_service
from app.services.extraction_service import extract_text
from app.repos.filesystem import local_repo

settings = get_settings()
data_file_path = settings.DATA_FILE_PATH
embed_model_id = settings.EMBED_MODEL_ID

# Initialize the embeddings object
embeddings = HuggingFaceEmbeddings(model_name=embed_model_id)


def validate_document(
    file_name: str,
    session: Session,
) -> Document:
    logger.info(f"Validating document {file_name}")
    document = Document(
        name=file_name,
        uuid=uuid4(),
    )

    return document


def upload_document(
    file: UploadFile,
    session: Session,
    document: Document
) -> Document:
    logger.info(f"Uploading document {document.name}")
    uploaded_document = local_repo.upload_document(
        document=document, file_path=settings.DATA_FILE_PATH)
    db_document = document_repo.create_document(
        session=session, document=uploaded_document)

    return db_document


def extract_document(settings: Settings, embeddings: Embeddings):
    document = extract_text(data_file_path)
    chunk_store = retriever_service.get_vector_store(
        settings=settings,
        collection_name="document_chunks",
        embeddings=embeddings),
    split_document_and_index_chunks(document, embeddings)


def split_document_and_index_chunks(
    document: LCDocument,
    embeddings: HuggingFaceEmbeddings
):
    chunks = retriever_service.split_text_into_chunks(document)
    retriever_service.index_chunks(chunks, settings, embeddings)


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    extract_document(db)

from uuid import uuid4
from fastapi import UploadFile
from loguru import logger
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.dependencies import get_settings
from app.domain.models import Document
from app.ocr.file_handler import save_tmp_copy
from app.repos.sql import document_repo
from app.services import retriever_service
from app.services.extraction_service import extract_text
from app.repos.filesystem.local_repo import LocalFileSystemRepository

local_repo = LocalFileSystemRepository()


def validate_document(
    file_name: str,
    session: Session,
) -> Document:
    logger.info(f"Validating document {file_name}")
    document = Document(
        name=file_name,
        uuid=uuid4(),
    )
    # TODO: Validate if isn't in the database

    return document


def upload_document(
    file: UploadFile,
    session: Session,
    data_file_path: str,
    document: Document
) -> Document:
    logger.info(f"Uploading document {document.name}")
    local_repo.upload_document(
        file=file, files_path=data_file_path)
    db_document = document_repo.create_document(
        session=session, document=document)

    return db_document


def extract_document(session: Session, data_file_path: str, embeddings: Embeddings, document_id: int) -> Document:
    document = document_repo.read_document(
        session, document_id)
    extracted_text = extract_text(
        data_file_path + "/" + document.name)
    split_document_and_index_chunks(
        document=document, embeddings=embeddings, extracted_text=extracted_text)
    # TODO: Add a flag for extracted
    return document


def split_document_and_index_chunks(
    document: Document,
    embeddings: HuggingFaceEmbeddings,
    extracted_text: str,
):
    chunks = retriever_service.split_text_into_chunks(extracted_text)
    retriever_service.index_chunks(
        chunks=chunks, document=document, embeddings=embeddings)

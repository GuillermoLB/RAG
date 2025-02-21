import io
from pathlib import Path
from fastapi import UploadFile
import pytest
from langchain_core.language_models import BaseLanguageModel
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.domain.models import Document
from app.domain.schemas import DocumentStatus
from app.services.document_service import extract_document, upload_document, validate_document
from app.tests.conftest import DocumentFactory, session


def test_validate_document(session: Session):
    file_name = "test_document.pdf"
    document = validate_document(file_name, session)

    assert isinstance(document, Document)
    assert document.name == file_name


def test_extract_document(
        settings: Settings,
        embeddings: BaseLanguageModel,
        session: Session,
):
    document = DocumentFactory()
    document = extract_document(
        session=session,
        data_file_path=settings.DATA_FILE_PATH,
        embeddings=embeddings,
        document_id=document.id,
    )

    assert document.status == DocumentStatus.EXTRACTED

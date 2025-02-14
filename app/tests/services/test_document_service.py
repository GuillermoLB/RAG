import pathlib
from pytest import Session
from langchain_core.language_models import BaseLanguageModel
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.domain.models import Document
from app.services.document_service import extract_document, validate_document
from app.tests.conftest import DocumentFactory

filepath = f"{pathlib.Path(__file__).parent.parent}/resources/doc1.txt"


def test_validate_document(session: Session):
    file_name = "test_document.pdf"
    document = validate_document(file_name, session)

    assert isinstance(document, Document)
    assert document.name == file_name


def test_extract_document(
        session: Session,
        settings: Settings,
        llm: BaseLanguageModel,
        embeddings: BaseLanguageModel,
):
    document = DocumentFactory()
    document = extract_document(
        session=session,
        settings=settings,
        llm=llm,
        embeddings=embeddings,
        document_id=document.id,
    )

    # TODO: Add extracted flag assertion when implemented
    assert True

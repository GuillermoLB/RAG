import uuid
import pytest
from loguru import logger
from sqlalchemy.orm import Session
from app.domain.models import Document
from app.repos.sql import document_repo
from app.tests.conftest import DocumentFactory, session


def test_create_document(session):
    document = Document(name="test_document", uuid=uuid.uuid4())
    created_document = document_repo.create_document(
        session=session, document=document)

    assert created_document.id is not None
    assert created_document.name == document.name

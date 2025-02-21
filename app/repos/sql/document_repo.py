from loguru import logger
import numpy as np
from sqlalchemy.orm import Session

from app.domain.models import Document
from app.domain.schemas import DocumentUpdate


def create_document(session: Session, document: Document) -> Document:
    logger.info(f"Creating document {document.name}")
    if not document:
        return None
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


def read_document(
    session: Session,
    document_id: int,
) -> Document:
    document = session.get(Document, document_id)
    if not document:
        return None
    return document


def update_document(session: Session, document: Document, document_update: DocumentUpdate) -> Document:
    logger.info(f"Updating document {document.name}")
    document_data = document_update.dict(exclude_unset=True)
    for key, value in document_data.items():
        setattr(document, key, value)
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

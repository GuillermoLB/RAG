from loguru import logger
import numpy as np
from sqlalchemy.orm import Session

from app.domain.models import Document


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

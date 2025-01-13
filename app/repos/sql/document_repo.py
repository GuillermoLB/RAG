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

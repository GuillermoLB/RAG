import numpy as np
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.models import Chunk
from app.domain.schemas import Document


def create_document(session: Session, document: Document) -> Document:
    if not document:
        return None
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

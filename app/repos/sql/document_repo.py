import numpy as np
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.domain.models import Chunk


# Method to store a new document along with its chunks
def store_document(db: Session, title: str):
    # Store the document
    db_document = Document(title=title)
    db.add(db_document)
    db.commit()
    return db_document

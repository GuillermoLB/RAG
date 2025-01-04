from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_active_user, get_db
from app.domain.schemas import User
from app.services.document_service import extract_document

router = APIRouter()


@router.post("/ingest")
async def ingest_document_endpoint(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    try:
        # Await the ingest_document function
        extract_document(db)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.document_service import ingest_document
from app.auth.auth import get_current_active_user
from app.schemas import User

router = APIRouter()

@router.post("/ingest")
async def ingest_document(current_user: User = Depends(get_current_active_user)):
    try:
        # Ingest the document
        ingest_document()
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
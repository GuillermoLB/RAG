from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.document_service import ingest_document
from app.dependencies import get_current_active_user
from app.schemas import User
from app.dependencies import get_db

router = APIRouter()

@router.post("/ingest")
async def ingest_document_endpoint(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    try:
        # Await the ingest_document function
        ingest_document(db)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
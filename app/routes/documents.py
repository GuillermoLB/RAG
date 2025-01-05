from fastapi import APIRouter, HTTPException

from app.services.document_service import extract_document
from ..dependencies import SessionDep, UserDep

router = APIRouter()


@router.post("/ingest")
async def ingest_document_endpoint(
    db: SessionDep, current_user: UserDep
):
    try:
        # Await the ingest_document function
        extract_document(db)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

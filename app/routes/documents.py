from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import ingest_document

router = APIRouter()

@router.post("/ingest")
async def ingest_document():
    try:
        # Ingest the document
        ingest_document()
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
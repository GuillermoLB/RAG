from fastapi import APIRouter, HTTPException

from app.services.document_service import extract_document

from ..dependencies import EmbeddingsDep, SessionDep, SettingsDep, UserDep

router = APIRouter()


@router.post("/ingest")
async def ingest_document_endpoint(
        settings: SettingsDep,
        db: SessionDep,
        current_user: UserDep,
        embeddings: EmbeddingsDep):
    try:
        # Await the ingest_document function
        extract_document(settings=settings, embeddings=embeddings)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

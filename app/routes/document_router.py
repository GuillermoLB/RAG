from fastapi import APIRouter, HTTPException, UploadFile

from app.services import document_service
from app.services.document_service import extract_document

from app.services.qa_service import generate_response

from ..dependencies import EmbeddingsDep, LLMDep, SessionDep, SettingsDep, UserDep

router = APIRouter()


@router.get("/upload")
async def upload_document_endpoint(
        session: SessionDep,
        settings: SettingsDep,
        file: UploadFile):

    try:
        file_name = file.filename
        document = document_service.validate_document(
            file_name=file_name,
            session=session,
        )

        document = document_service.upload_document(
            file=file,
            db=SessionDep,
            document=document,
        )
    except (HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=str(e))

    return {"message": "Upload a document"}


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


@router.post("/ask")
async def handle_qa_process(
        query: str,
        llm: LLMDep,
        current_user: UserDep,
        embeddings: EmbeddingsDep,
        settings: SettingsDep):
    try:
        response = generate_response(query, llm, embeddings, settings)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

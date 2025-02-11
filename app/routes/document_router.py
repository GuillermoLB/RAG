from fastapi import APIRouter, HTTPException, UploadFile

from app.services import document_service
from app.services.document_service import extract_document

from app.services.qa_service import generate_response

from ..dependencies import EmbeddingsDep, LLMDep, SessionDep, SettingsDep, UserDep

router = APIRouter()


@router.post("/upload")
def upload_document_endpoint(
        session: SessionDep,
        settings: SettingsDep,
        current_user: UserDep,
        file: UploadFile):

    try:
        file_name = file.filename
        document = document_service.validate_document(
            file_name=file_name,
            session=session,
        )

        document = document_service.upload_document(
            file=file,
            session=session,
            document=document,
        )
    except (HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=str(e))

    return document


@router.post("/{document_id}/extracted")
def extract_document(
        session: SessionDep,
        settings: SettingsDep,
        embeddings: EmbeddingsDep,
        document_id: int):
    try:
        extracted_document = document_service.extract_document(
            session=session,
            settings=settings,
            embeddings=embeddings,
            document_id=document_id,
        )
        return extracted_document
    except (HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=str(e))

    return {"message": "Extracted document"}


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

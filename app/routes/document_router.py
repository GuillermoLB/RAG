from fastapi import APIRouter, HTTPException, UploadFile

from app.error.exceptions import RAGException
from app.services import document_service

from ..dependencies import EmbeddingsDep, SessionDep, SettingsDep, UserDep

documents = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@documents.post("/upload")
def upload_document(
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
        return document
    except (RAGException, HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=e.error)


@documents.post("/{document_id}/extracted")
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
    except (RAGException, HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=e.error)

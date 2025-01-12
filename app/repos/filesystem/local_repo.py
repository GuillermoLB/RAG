from loguru import logger
import pathlib
import shutil
from pathlib import Path

from fastapi import UploadFile

from app.domain.schemas import Document

from .base import FilesystemBaseRepository


class LocalFileSystemRepository(FilesystemBaseRepository):

    def upload_document(
        self, document: Document, file_path: str
    ) -> Document:
        document_path = Path(file_path).joinpath(document.name)
        with open(document_path, "wb") as file:
            shutil.copyfileobj(document.file.file, file)
        logger.info(f"Uploaded document to {document_path}")
        return document

    def delete_document_files(
        self, project_name: str, document_name: str, files_path: str
    ):
        document_path = (
            Path(files_path).joinpath(project_name).joinpath(
                "documents", document_name)
        )
        document_path.unlink()
        logger.info(f"Deleted document at {document_path}")

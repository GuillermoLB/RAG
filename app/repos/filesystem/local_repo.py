from loguru import logger
import pathlib
import shutil
from pathlib import Path

from fastapi import UploadFile

from app.domain.schemas import Document

from .base import FilesystemBaseRepository


class LocalFileSystemRepository(FilesystemBaseRepository):

    def upload_document(
        self, file: UploadFile, files_path: str
    ) -> tuple[bytes, Path]:
        root_dir = Path(files_path)
        documents_dir = root_dir
        file_path = documents_dir.joinpath(file.filename)
        file_bytes = file.file.read()
        file_path.write_bytes(file_bytes)
        return file_bytes, file_path

    def delete_document_files(
        self, project_name: str, document_name: str, files_path: str
    ):
        document_path = (
            Path(files_path).joinpath(project_name).joinpath(
                "documents", document_name)
        )
        document_path.unlink()
        logger.info(f"Deleted document at {document_path}")

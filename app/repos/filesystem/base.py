from ...domain import models


class FilesystemBaseRepository:

    def upload_document(self, **kwargs) -> models.Document:
        raise NotImplementedError

    def delete_document_files(self, **kwargs) -> dict:
        raise NotImplementedError

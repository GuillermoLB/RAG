import io
from pathlib import Path

import pytest
from fastapi import UploadFile

from app.repos.filesystem.local_repo import LocalFileSystemRepository


def test_upload_document(tmp_path, local_repo):
    # Create a fake file (simulate UploadFile)
    file_content = b"Sample document content"
    file_name = "testfile.pdf"
    file_obj = io.BytesIO(file_content)
    upload_file = UploadFile(filename=file_name, file=file_obj)

    # Use tmp_path as the files_path
    files_path = str(tmp_path)
    returned_bytes, returned_path = local_repo.upload_document(
        file=upload_file, files_path=files_path
    )

    # Check that the returned bytes match the file content
    assert returned_bytes == file_content
    # Verify that the file was actually written
    written_file = Path(files_path) / file_name
    assert written_file.exists()
    assert written_file.read_bytes() == file_content


def test_delete_document_files(tmp_path, local_repo):
    # Setup: create a dummy file in a subdirectory
    project = "my_project"
    documents_dir = tmp_path / project / "documents"
    documents_dir.mkdir(parents=True)
    doc_name = "testfile.pdf"
    file_path = documents_dir / doc_name
    file_path.write_text("dummy content")

    # Verify file exists before deletion
    assert file_path.exists()

    # Call delete_document_files and then verify deletion.
    local_repo.delete_document_files(
        project_name=project,
        document_name=doc_name,
        files_path=str(tmp_path)
    )
    assert not file_path.exists()

import pathlib
from httpx import AsyncClient
import pytest
from app.main import app

from fastapi import status


filepath = f"{pathlib.Path(__file__).parent.parent}/resources/doc1.pdf"

pytestmark = pytest.mark.asyncio


async def test_upload_document_works(client: AsyncClient):
    res = await client.post(
        "/upload", files={"file": ("doc1.pdf", open(filepath, "rb"), "application/pdf")})

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"id": 1, "name": "doc1.pdf"}

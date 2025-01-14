import pathlib
from httpx import AsyncClient
import pytest
from app.main import app


filepath = f"{pathlib.Path(__file__).parent.parent}/resources/doc1.pdf"

pytestmark = pytest.mark.asyncio


async def test_upload_document_works(client: AsyncClient):
    res = await client.post(
        "/upload", files={"file": ("doc1.pdf", open(filepath, "rb"), "application/pdf")})

    assert res.status_code == 200
    assert res.json() == {"message": "Upload a document"}

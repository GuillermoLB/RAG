from uuid import UUID
from app.domain.models import Document
from app.domain.schemas import default_uuid


d1 = Document(id=100, name="mock", uuid=UUID(default_uuid))


def mock_document(*args, **kwargs):
    return d1

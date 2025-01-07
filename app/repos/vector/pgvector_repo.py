from langchain.indexes import index, IndexingResult
from langchain.vectorstores.pgvector import PGVector
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings


from ...domain.models import PGEmbedding, PGUpsertionRecord

from ...dependencies import get_settings


class VectorIndex:
    def __init__(
        self,
        documents: list[LCDocument],
        embeddings: Embeddings,
    ) -> None:
        self.documents = documents

        self.vector_store = PGVector(
            collection_name="docs",
            connection_string=get_settings().get_connection_str(),
            embedding_function=embeddings,
        )

    def index(self) -> IndexingResult:
        return index(
            docs_source=self.documents,
            vector_store=self.vector_store,
        )

from langchain.indexes import IndexingResult, SQLRecordManager, index
from langchain.vectorstores.pgvector import PGVector
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings

from ...dependencies import get_settings


class VectorIndex:
    def __init__(
        self,
        documents: list[LCDocument],
        embeddings: Embeddings,
    ) -> None:
        self.documents = documents

        namespace = f"pgvector/document_chunks"
        self.record_manager = SQLRecordManager(
            namespace, db_url=get_settings().get_connection_str()
        )
        self.record_manager.create_schema()
        self.vector_store = PGVector(
            collection_name="document_chunks",
            connection_string=get_settings().get_connection_str(),
            embedding_function=embeddings,
        )

    def index(self) -> IndexingResult:
        return index(
            docs_source=self.documents,
            vector_store=self.vector_store,
            record_manager=self.record_manager
        )

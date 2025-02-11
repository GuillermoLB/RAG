from fastapi import Depends
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from loguru import logger

from app.core.config import Settings
from app.dependencies import get_embeddings, get_settings
from app.domain.models import Document
from app.repos.vector.pgvector_repo import VectorIndex


def get_vector_store(
        settings: Settings,
        collection_name: str,
        embeddings: Embeddings) -> PGVector:
    logger.info(f"Getting vector store for {collection_name}")
    return PGVector(
        embedding_function=embeddings,
        connection_string=settings.get_connection_str(),
        collection_name=collection_name,
        use_jsonb=True,
    )


def split_text_into_chunks(document: LCDocument) -> list[LCDocument]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=0,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents([document])
    return chunks


def index_chunks(
        settings: Settings,
        chunks: list[LCDocument],
        document: Document,
        embeddings: Embeddings):
    document_metadata = {
        "name": document.name,
        "document_uuid": str(document.uuid),
    }
    [chunk.metadata.update(document_metadata) for chunk in chunks]
    chunks_index = VectorIndex(
        documents=chunks,
        embeddings=embeddings,
    )
    result = chunks_index.index()
    logger.debug(f"Chunks indexed: {result}")

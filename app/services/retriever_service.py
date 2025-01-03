import logging

from langchain.retrievers import EnsembleRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pgvector import DistanceStrategy, PGVector
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document as LDocument
from langchain_core.embeddings import Embeddings
from sqlalchemy import String, cast, func, select, update
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.domain.models import Document

def get_vector_store(
    settings: Settings, collection_name: str, embeddings: Embeddings
) -> PGVector:
    return PGVector(
        collection_name=collection_name,
        connection_string=settings.get_connection_str(),
        embedding_function=embeddings,
        distance_strategy=DistanceStrategy.COSINE,
    )
    

    
def split_text_into_chunks(text: str) -> list[LDocument]:
    logger.info("Splitting document into smaller chunks")
    langchain_doc = LDocument(page_content=str(text))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=0,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents([langchain_doc])
    return chunks

def index_chunks(chunks: list[LDocument], document: Document, embeddings: Embeddings):
    if document.category:
        category_id = document.category.id
    else:
        category_id = None
    document_metadata = {
        "project_id": document.project_id,
        "name": document.name,
        "document_uuid": str(document.uuid),
        "category_id": category_id,
        "collection": document.collection,
        "source": document.location,
    }
    [chunk.metadata.update(document_metadata) for chunk in chunks]
    logger.debug(f"Document split into: {len(chunks)} chunks")
    chunks_index = VectorIndex(
        collection_type=CollectionType.document_chunks,
        documents=chunks,
        cleanup="incremental",
        source_id_key="document_uuid",
        embeddings=embeddings,
    )
    result = chunks_index.index()
    logger.debug(f"Chunks indexed: {result}")

def retrieve_relevant_chunks(
    store: PGVector,
    filter: dict,
    threshold: float,
    query: str,
) -> list[LDocument]:
    similarity_retriever = store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": threshold,
            "filter": filter,
        },
    )
    similar_chunks = similarity_retriever.get_relevant_documents(query=query)
    return similar_chunks[:5]
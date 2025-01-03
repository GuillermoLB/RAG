import logging

from langchain.retrievers import EnsembleRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pgvector import DistanceStrategy, PGVector
from langchain_community.retrievers import BM25Retriever
from langchain_core.embeddings import Embeddings
from sqlalchemy import String, cast, func, select, update
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from langchain_core.documents import Document as LCDocument
from app.core.config import Settings, settings


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
    

    
def split_text_into_chunks(document: LCDocument) -> list[LCDocument]:
    #logger.info("Splitting document into smaller chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=0,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents([document])
    return chunks

def index_chunks(chunks: list[LCDocument], document: Document, embeddings: Embeddings):
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="docs",
        connection=settings.get_connection_str(),
        use_jsonb=True,
    )
    
# def retrieve_relevant_chunks(
#     store: PGVector,
#     filter: dict,
#     threshold: float,
#     query: str,
# ) -> list[LDocument]:
#     similarity_retriever = store.as_retriever(
#         search_type="similarity_score_threshold",
#         search_kwargs={
#             "k": 20,
#             "score_threshold": threshold,
#             "filter": filter,
#         },
#     )
#     similar_chunks = similarity_retriever.get_relevant_documents(query=query)
#     return similar_chunks[:5]
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from fastapi import Depends
from langchain_core.vectorstores.base import VectorStoreRetriever
from app.dependencies import get_settings, get_embeddings

from app.core.config import Settings


def get_vector_store(collection_name: str, documents: LCDocument,embeddings=Depends(get_embeddings), settings=Settings)->PGVector:
    return PGVector.from_documents(
        documents=documents,  # You need to provide the actual documents here
        embeddings=embeddings,
        collection_name=collection_name,
        connection_string=settings.get_connection_str(),
        use_jsonb=True,
    )
    
def get_retriever(collection_name: str, embeddings=Depends(get_embeddings), settings=Settings)->VectorStoreRetriever:
    retriever = PGVector(
        embedding_function=embeddings,
        collection_name=collection_name,
        connection_string=settings.get_connection_str(),
        use_jsonb=True,
    ).as_retriever()
    return retriever
    
def split_text_into_chunks(document: LCDocument) -> list[LCDocument]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=0,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents([document])
    return chunks

def index_chunks(chunks: list[LCDocument], settings: Settings, embeddings: Embeddings):
    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="docs",
        connection_string=settings.get_connection_str(),
        use_jsonb=True,
    )
    return vector_store
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings

from app.core.config import Settings


def get_vector_store(
    collection_name: str, embeddings: Embeddings, settings: Settings
) -> PGVector:
    return PGVector(
        collection_name=collection_name,
        connection_string=settings.get_connection_str(),
        embedding_function=embeddings,
    )
    
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
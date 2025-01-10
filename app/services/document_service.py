from langchain.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.dependencies import get_db, get_settings
from app.services import retriever_service
from app.services.extraction_service import extract_text

settings = get_settings()
data_file_path = settings.DATA_FILE_PATH
embed_model_id = settings.EMBED_MODEL_ID

# Initialize the embeddings object
embeddings = HuggingFaceEmbeddings(model_name=embed_model_id)

# instantiate once per document


def get_vector_store(
    settings: Settings, collection_name: str, embeddings: Embeddings
) -> PGVector:
    return PGVector(
        collection_name=collection_name,
        connection_string=settings.get_connection_str(),
        embedding_function=embeddings,
    )


def extract_document(settings: Settings, embeddings: Embeddings):
    document = extract_text(data_file_path)
    chunk_store = get_vector_store(
        settings=settings,
        collection_name="document_chunks",
        embeddings=embeddings),
    split_document_and_index_chunks(document, embeddings)


def split_document_and_index_chunks(
    document: LCDocument,
    embeddings: HuggingFaceEmbeddings
):
    chunks = retriever_service.split_text_into_chunks(document)
    retriever_service.index_chunks(chunks, settings, embeddings)


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    extract_document(db)

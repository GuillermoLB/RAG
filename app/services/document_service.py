import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repos.sql.document_repo import store_document
from app.services import retriever_service
from app.utils.chunking import chunk_document
from app.utils.embedding import embed_chunks
from app.services.extraction_service import extract_text
from langchain_core.documents import Document as LCDocument
from langchain_core.embeddings import Embeddings
from langchain.vectorstores.pgvector import PGVector

load_dotenv()
data_file_path = os.getenv("DATA_FILE_PATH")


def extract_document(db: Session):
    document = extract_text(data_file_path)
    split_document_and_index_chunks(db, document)
    store_document(db, document)
    
def split_document_and_index_chunks(
    session: Session,
    document: LCDocument,
    embeddings: Embeddings
):
    # index chunks
    chunks = retriever_service.split_text_into_chunks(document)
    retriever_service.index_chunks(chunks, document, embeddings)


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    extract_document(db)

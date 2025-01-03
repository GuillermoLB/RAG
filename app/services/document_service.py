import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repos.sql.document_repo import store_document
from app.utils.chunking import chunk_document
from app.utils.embedding import embed_chunks
from app.utils.preprocessing import preprocess_text

load_dotenv()
data_file_path = os.getenv("DATA_FILE_PATH")


def ingest_document(db: Session):
    document = preprocess_text(data_file_path)
    chunks = chunk_document(document)
    embedded_chunks = embed_chunks(chunks)
    store_document(db, data_file_path, embedded_chunks)
    
def split_document_and_index_chunks(
    session: Session,
    document: Document,
    embeddings: Embeddings,
    parsing: Parsing,
    chunk_store: PGVector = None,
):
    if document.has_layout():
        # index layout blocks
        blocks = ocr.get_layout_blocks(parsing)
        retriever_service.index_blocks(blocks, document, embeddings)
        # mark sections
        category = document.get_effective_category()
        if category.has_sections():
            entries = category.get_section_entries()
            mark_sections(session, chunk_store, document, entries, blocks)
    else:
        # index chunks
        chunks = retriever_service.split_text_into_chunks(parsing.text)
        retriever_service.index_chunks(chunks, document, embeddings)


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    ingest_document(db)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document as LCDocument
from sqlalchemy.orm import Session

from app.dependencies import get_settings, get_db
from app.services import retriever_service
from app.services.extraction_service import extract_text


settings = get_settings()
data_file_path = settings.DATA_FILE_PATH
embed_model_id = settings.EMBED_MODEL_ID

# Initialize the embeddings object
embeddings = HuggingFaceEmbeddings(model_name=embed_model_id)

def extract_document(db: Session):
    document = extract_text(data_file_path)
    split_document_and_index_chunks(db, document, embeddings)

def split_document_and_index_chunks(
    session: Session,
    document: LCDocument,
    embeddings: HuggingFaceEmbeddings
):
    chunks = retriever_service.split_text_into_chunks(document)
    retriever_service.index_chunks(chunks, settings, embeddings)


if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    extract_document(db)

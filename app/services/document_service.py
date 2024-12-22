from app.utils.preprocessing import preprocess_text
from app.database.vector_store import store_vector

def ingest_document(doc_text: str):
    preprocessed_text = preprocess_text(doc_text)
    embedding = get_embeddings(preprocessed_text)
    store_vector(preprocessed_text, embedding)

from app.utils.preprocessing import preprocess_text
from app.models.embedding_model import get_embeddings
#from app.database.vector_store import store_vector
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
data_files_path = os.getenv('DATA_FILES_PATH')

def ingest_document():
    # Preprocess the document text to get chunks
    chunks = preprocess_text(data_files_path)
    
    # Iterate over each chunk to generate embeddings and store them
    for chunk in chunks:
        chunk_text = chunk["chunk_text"]
        embedding = get_embeddings(chunk_text)
        #store_vector(chunk_text, embedding)

if __name__ == "__main__":
    ingest_document()
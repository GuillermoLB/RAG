import os

from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from loguru import logger

# Load environment variables from .env file
load_dotenv()

# Load the model identifier from the .env file
model_id = os.getenv("EMBED_MODEL_ID")

# Initialize HuggingFaceEmbeddings
embeddings_model = HuggingFaceEmbeddings(model_name=model_id)


def embed_query(text: str):
    return embeddings_model.embed_query(text)


def embed_chunks(chunks):
    logger.info("Embedding chunks")
    chunk_texts = [
        chunk.page_content if isinstance(chunk, Document) else chunk for chunk in chunks
    ]
    embeddings = embeddings_model.embed_documents(chunk_texts)
    chunk_data = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_info = {
            "index": i,
            "chunk_text": chunk.page_content if isinstance(chunk, Document) else chunk,
            "embedding": embedding,
        }
        chunk_data.append(chunk_info)
    return chunk_data

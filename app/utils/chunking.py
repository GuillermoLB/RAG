import os

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

# Add the root directory to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# Load environment variables from .env file
load_dotenv()

# Load the model and tokenizer using the model identifier from the .env file
model_id = os.getenv("EMBED_MODEL_ID")
max_tokens = int(os.getenv("MAX_TOKENS"))


def chunk_document(document):
    logger.info(f"Initializing tokenizer with model ID: {model_id}")
    logger.info("Chunking document")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    return texts

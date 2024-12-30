import sys
import os

# Add the root directory to sys.path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from pathlib import Path
from docling.document_converter import DocumentConverter
from loguru import logger
from tqdm import tqdm
from docling.chunking import HybridChunker
from transformers import AutoTokenizer

# Load environment variables from .env file
load_dotenv()

# Load the model and tokenizer using the model identifier from the .env file
model_id = os.getenv("EMBED_MODEL_ID")
max_tokens = int(os.getenv("MAX_TOKENS"))

def chunk_document(document):
    logger.info(f"Initializing tokenizer with model ID: {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    logger.info("Chunking document")
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=max_tokens,
    )
    chunk_iter = chunker.chunk(dl_doc=document)
    return list(chunk_iter)
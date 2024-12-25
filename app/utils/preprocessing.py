import sys
import os
import argparse

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from pathlib import Path
from docling.document_converter import DocumentConverter
from loguru import logger
from tqdm import tqdm
from docling.chunking import HybridChunker
from transformers import AutoTokenizer
from app.database.relational_db import store_document, get_db, get_stored_documents
from app.models.embedding_model import get_embeddings

# Load the .env file
load_dotenv()

# Access environment variables
data_files_path = os.getenv('DATA_FILES_PATH', 'data')  # Default to 'data' if not set
embed_model_id = os.getenv('EMBED_MODEL_ID')
max_tokens = int(os.getenv('MAX_TOKENS', 512))  # Ensure max_tokens is an integer

def convert_document(input_path: Path):
    """
    Convert the document using DocumentConverter.

    Args:
        input_path (Path): The path to the input document.

    Returns:
        Document: The converted document.
    """
    logger.info(f"Converting document: {input_path}")
    converter = DocumentConverter()
    result = converter.convert(input_path)
    return result.document

def initialize_tokenizer(model_id: str):
    """
    Initialize the tokenizer.

    Args:
        model_id (str): The model ID for the tokenizer.

    Returns:
        AutoTokenizer: The initialized tokenizer.
    """
    logger.info(f"Initializing tokenizer with model ID: {model_id}")
    return AutoTokenizer.from_pretrained(model_id)

def chunk_document(doc, tokenizer, max_tokens: int):
    """
    Chunk the document using HybridChunker.

    Args:
        doc (Document): The document to be chunked.
        tokenizer (AutoTokenizer): The tokenizer to use for chunking.
        max_tokens (int): The maximum number of tokens per chunk.

    Returns:
        list: A list of chunks.
        HybridChunker: The chunker used for chunking.
    """
    logger.info("Chunking document")
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=max_tokens,
    )
    chunk_iter = chunker.chunk(dl_doc=doc)
    return list(chunk_iter), chunker

def serialize_chunks(chunks, tokenizer, chunker):
    """
    Serialize chunks and return a list of chunk information.

    Args:
        chunks (list): The list of chunks to serialize.
        tokenizer (AutoTokenizer): The tokenizer to use for serialization.
        chunker (HybridChunker): The chunker used for chunking.

    Returns:
        list: A list of dictionaries containing chunk information.
    """
    logger.info("Serializing chunks")
    chunk_data = []
    for i, chunk in enumerate(chunks):
        txt_tokens = len(tokenizer.tokenize(chunk.text, max_length=None))
        ser_txt = chunker.serialize(chunk=chunk)
        ser_tokens = len(tokenizer.tokenize(ser_txt, max_length=None))
        embedding = get_embeddings(chunk.text)

        chunk_info = {
            "index": i,
            "chunk_text": chunk.text,
            "chunk_text_tokens": txt_tokens,
            "serialized_text": ser_txt,
            "serialized_text_tokens": ser_tokens,
            "embedding": embedding,
        }
        chunk_data.append(chunk_info)
    logger.info(f"Serialized {len(chunks)} chunks")
    return chunk_data

def preprocess_text(data_files_path: str):
    """
    Preprocess text by converting and chunking documents.

    Args:
        data_files_path (str): The path to the directory containing the data files.

    Returns:
        list: A list of dictionaries containing chunk information.
    """
    data_files_path = Path(data_files_path)  # Convert to Path object
    logger.info(f"Data files path: {data_files_path}")
    
    # Check if the directory exists
    if not data_files_path.exists():
        logger.error(f"Directory does not exist: {data_files_path}")
        return []
    
    # Initialize the tokenizer
    tokenizer = initialize_tokenizer(embed_model_id)
    
    # Process each file in the raw data directory with tqdm progress bar
    pdf_files = list(data_files_path.glob("*.pdf"))
    logger.info(f"Found {len(pdf_files)} PDF files.")
    
    all_chunk_data = []
    
    for input_path in tqdm(pdf_files, desc="Processing files"):
        logger.info(f"Processing file: {input_path.name}")

        # Convert the document
        doc = convert_document(input_path)
        
        # Chunk the document
        chunks, chunker = chunk_document(doc, tokenizer, max_tokens)

        # Serialize chunks
        chunk_data = serialize_chunks(chunks, tokenizer, chunker)
    
        all_chunk_data.extend(chunk_data)
        
        # Store the document and its chunks
        db = next(get_db())
        store_document(db, input_path.name, chunk_data)
        
        # Log the processed document
        logger.info(f"Processed document: {doc}")
        print(f"Processed document: {doc}")

    return all_chunk_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess text or retrieve stored documents.")
    parser.add_argument("command", choices=["preprocess", "retrieve"], help="Command to execute")
    args = parser.parse_args()

    if args.command == "preprocess":
        preprocess_text(data_files_path)
    elif args.command == "retrieve":
        get_stored_documents()
import sys
import os
import argparse

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from pathlib import Path
from docling.document_converter import DocumentConverter
from loguru import logger

load_dotenv()

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

def preprocess_text(data_file_path: str):
    """
    Preprocess text by converting and chunking documents.

    Args:
        data_files_path (str): The path to the directory containing the data files.

    Returns:
        list: A list of dictionaries containing chunk information.
    """
    data_files_path = Path(data_file_path)  # Convert to Path object
    logger.info(f"Data file path: {data_file_path}")

    # Convert the document
    doc = convert_document(data_file_path)
    
    # Log the processed document
    logger.info(f"Processed document: {doc}")

    return doc
import os
import sys

# Add the root directory to sys.path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from pathlib import Path

from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
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

    logger.info(f"Data file path: {data_file_path}")

    # Convert the document
    doc = convert_document(data_file_path)

    # Log the processed document
    logger.info(f"Processed document: {doc}")

    return doc

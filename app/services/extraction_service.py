from loguru import logger
from langchain_core.documents import Document as LCDocument
from langchain_core.document_loaders import BaseLoader
from dotenv import load_dotenv
from docling.document_converter import DocumentConverter
from typing import Iterator
from pathlib import Path
import os
import sys

# Add the root directory to sys.path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))


load_dotenv()


class DoclingPDFLoader(BaseLoader):

    def __init__(self, file_path: str | list[str]) -> None:
        self._file_paths = file_path if isinstance(
            file_path, list) else [file_path]
        self._converter = DocumentConverter()

    def lazy_load(self) -> Iterator[LCDocument]:
        for source in self._file_paths:
            dl_doc = self._converter.convert(source).document
            text = dl_doc.export_to_markdown()
            yield LCDocument(page_content=text)


def convert_document(input_path: Path):
    """
    Convert the document using DocumentConverter.

    Args:
        input_path (Path): The path to the input document.

    Returns:
        Document: The converted document.
    """
    loader = DoclingPDFLoader(input_path)
    result = loader.load()
    return result


def extract_text(data_file_path: str) -> LCDocument:

    logger.info(f"Data file path: {data_file_path}")

    # Convert the document
    doc = convert_document(data_file_path)

    # Log the processed document
    logger.info(f"Processed document: {doc}")

    return doc[0]

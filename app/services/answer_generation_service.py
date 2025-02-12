from langchain_core.embeddings import Embeddings
from langchain_ollama import ChatOllama
from loguru import logger

from app.core.config import Settings
from app.ml.qa.qa_chain import get_qa_chain


def generate_response(
        settings: Settings,
        query: str,
        llm: ChatOllama,
        embeddings: Embeddings) -> str:
    rag_chain = get_qa_chain(llm=llm, embeddings=embeddings, settings=settings)
    response = rag_chain.invoke({"input": query})
    logger.info(f"Generated response: {response}")

    return response

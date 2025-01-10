from typing import Any
from fastapi import Depends
from loguru import logger
from langchain_core.embeddings import Embeddings
from app.dependencies import get_settings, get_embeddings
from app.services.retriever_service import get_vector_store
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from app.core.config import Settings
from langchain_ollama import ChatOllama
from langchain_core.vectorstores.base import VectorStoreRetriever
from app.ml.qa.qa_chain import get_qa_chain




def generate_response(query: str, llm: ChatOllama, embeddings: Embeddings, settings: Settings) -> str:
    rag_chain = get_qa_chain(llm=llm, embeddings=embeddings, settings=settings)
    response = rag_chain.invoke({"input": query})
    logger.info(f"Generated response: {response}")

    return response

def main():
    settings = get_settings()
    query = "What is the capital of France?"

    # Initialize the LLM
    llm = ChatOllama(model=settings.CHAT_LLM.config["model"], temperature=settings.CHAT_LLM.config["temperature"])

    # Initialize the embeddings
    embeddings = get_embeddings()

    # Generate the response
    response = generate_response(query, llm, embeddings, settings)
    print(response)

if __name__ == "__main__":
    main()
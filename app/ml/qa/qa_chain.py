from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_ollama import ChatOllama
from loguru import logger

from app.core.config import Settings
from app.services.retriever_service import get_vector_store


def build_prompt() -> ChatPromptTemplate:
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    instruction = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    logger.info("Built prompt")
    return instruction


def get_qa_chain(
        llm: BaseLanguageModel,
        embeddings: Embeddings,
        settings: Settings) -> LLMChain:

    prompt = build_prompt()
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retriever = get_vector_store(
        settings=settings,
        collection_name="document_chunks",
        embeddings=embeddings).as_retriever()
    logger.info("Built retriever")
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    logger.info("Built QA chain")
    return rag_chain

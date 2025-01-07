from typing import Any
from fastapi import Depends
from loguru import logger
from app.dependencies import get_settings, get_embeddings
from app.services.retriever_service import get_vector_store
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from langchain_ollama import ChatOllama
from langchain_core.vectorstores.base import VectorStoreRetriever

settings = get_settings()

def initialize_llm(model_id: str) -> ChatOllama:
    return ChatOllama(model=model_id, temperature=0)


def generate_response(query: str, llm: ChatOllama, retriever: VectorStoreRetriever) -> str:
    logger.info(f"Enter generator")
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    logger.info("Before ChatPromptTemplate")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
        
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": query})

    return response

def main(embeddings=Depends(get_embeddings)):
    model_id = settings.RESPONSE_MODEL_ID
    llm = initialize_llm(model_id)
    vector_store = get_vector_store("docs", embeddings, settings)

    query = "Who is Guillermo?"
    response = generate_response(query, llm, vector_store)
    print(response)

if __name__ == "__main__":
    main()

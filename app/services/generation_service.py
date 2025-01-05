from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from app.dependencies import get_settings
from app.dependencies import get_db
from app.services.retriever_service import get_vector_store

settings = get_settings()

model_id = settings.RESPONSE_MODEL_ID
embed_model_id = settings.EMBED_MODEL_ID

embeddings = HuggingFaceEmbeddings(model_name=embed_model_id)

def generate_response(query: str) -> str:
    llm = ChatOllama(
    model=model_id,
    temperature=0
    )
    vector_store = get_vector_store("docs", embeddings, settings)
    
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(vector_store.as_retriever(), question_answer_chain)

    response = rag_chain.invoke({"input": query})
    return response

if __name__ == "__main__":
    # Create a new database session
    db = next(get_db())
    response = generate_response("Who is Guillermo?")
    print(response)

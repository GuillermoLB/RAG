import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from app.services.retriever_service import get_vector_store
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

# Load environment variables from .env file
load_dotenv()

model_id = os.getenv("RESPONSE_GENERATION_MODEL_ID")


llm = ChatOllama(
    model="mistral",
    temperature=0
)

# Define ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful and informative assistant. Answer user questions based on the provided context."),
    HumanMessage(content="{history}\n\n{text}\n\n{question}"),
])

# Create a RetrievalQA chain
vector_store = get_vector_store(settings)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(),
    chain_type="stuff",
    verbose=True,
    prompt=chat_prompt
)

if __name__ == "__main__":
    response_generator_msg = SystemMessage(content="You are an AI assistant that answer user queries")
    query_msg = HumanMessage(content="Is Guillermo a machine learning engineer?")
    ai_msg = llm.invoke([response_generator_msg] + [query_msg])
    print(ai_msg)
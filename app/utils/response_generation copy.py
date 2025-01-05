import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from app.services.retriever_service import get_vector_store
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from langchain.chains import create_retrieval_chain

# Load environment variables from .env file
load_dotenv()

model_id = os.getenv("RESPONSE_GENERATION_MODEL_ID")


llm = ChatOllama(
    model="mistral",
    temperature=0
)

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
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

results = rag_chain.invoke({"input": "What was Nike's revenue in 2023?"})

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
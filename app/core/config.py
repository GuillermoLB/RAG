from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from app.domain.schemas import LLModel, LLMType

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "db"
    EMBED_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    QA_MODEL_ID: str = "mistral"
    QA_MODEL_URL: str
    MAX_TOKENS: int = 512
    DATA_FILE_PATH: str = "data"
    LANGSMITH_API_KEY: str
    LANGSMITH_TRACING: bool = True
    LANGCHAIN_PROJECT: str
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    VECTOR_DIMENSION: int = 768

    @property
    def QA_LLM(self):
        from app.domain.schemas import LLModel, LLMType
        return LLModel(
            config={
                "model": self.QA_MODEL_ID,
                "temperature": 0.0,
                "base_url": self.QA_MODEL_URL
            },
            type=LLMType.QA,
            fake=False,
        )

    def get_connection_str(self):
        """
        Construct and return the database connection string.
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


def build_llm(llm: LLModel) -> BaseModel:

    if llm.type == LLMType.QA:
        return ChatOllama(**llm.config)
    elif llm.type == LLMType.EMBEDDINGS:
        return HuggingFaceEmbeddings(**llm.config)
    else:
        pass

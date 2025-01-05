from dotenv import load_dotenv
from pydantic_settings import  BaseSettings

# Load environment variables from .env file
load_dotenv(override=True)

class Settings(BaseSettings):
    POSTGRES_USER:str = "user"
    POSTGRES_PASSWORD:str = "password"
    POSTGRES_HOST:str= "localhost"
    POSTGRES_PORT:int = 5432
    POSTGRES_DB:str= "db"
    EMBED_MODEL_ID:str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_TOKENS:int=512
    RESPONSE_MODEL_ID:str = "mistral"
    DATA_FILE_PATH:str ="data/1.pdf"
    LANGSMITH_API_KEY:str
    LANGSMITH_TRACING:bool=True
    LANGCHAIN_PROJECT:str
    SECRET_KEY:str="your_secret_key"
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    

    def get_connection_str(self):
        """
        Construct and return the database connection string.
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
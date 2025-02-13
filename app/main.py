import logging

from fastapi import FastAPI

from app.routes.document_router import documents
from app.routes.user_router import users
from app.routes.token_router import tokens
from app.routes.answer_generation_router import answer_generations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(documents)
app.include_router(users)
app.include_router(tokens)
app.include_router(answer_generations)


@app.get("/")
def health_check():
    return {"status": "OK"}

import logging

from fastapi import FastAPI

from app.routes.document_router import documents
from app.routes.user_router import users

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(documents)
app.include_router(users)


@app.get("/")
def health_check():
    return {"status": "OK"}

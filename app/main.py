import logging

from fastapi import FastAPI

from app.routes import document_router, user_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(document_router.router, tags=["documents"])
app.include_router(user_router.router, tags=["users"])


@app.get("/")
def health_check():
    return {"status": "OK"}

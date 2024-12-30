import logging
from fastapi import FastAPI
from app.routes import query, documents, auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(auth.router, tags=["Auth"])

@app.get("/")
def health_check():
    return {"status": "OK"}

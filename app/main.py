import logging

from fastapi import FastAPI

from app.routes import document_router, query_router, user_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(query_router.router, prefix="/query", tags=["Query"])
app.include_router(
    document_router.router,
    prefix="/documents",
    tags=["Documents"])
app.include_router(user_router.router, tags=["Auth"])


@app.get("/")
def health_check():
    return {"status": "OK"}

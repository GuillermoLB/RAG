from fastapi import FastAPI
from app.routes import query, documents

app = FastAPI()

# Include API routes
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])

@app.get("/")
def health_check():
    return {"status": "OK"}

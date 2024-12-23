from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import ingest_document

router = APIRouter()

@router.post("/ingest")
async def ingest_document_route(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        content = await file.read()
        # Convert bytes to string (assuming the file is a text file)
        doc_text = content.decode("utf-8")
        # Ingest the document
        ingest_document(doc_text)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
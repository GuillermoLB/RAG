from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.query_service import process_query
from app.auth.auth import get_current_active_user
from app.schemas import User

router = APIRouter()

@router.post("/")
async def handle_query(query: str, current_user: User = Depends(get_current_active_user)):
    try:
        response = process_query(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

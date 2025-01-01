from fastapi import APIRouter, HTTPException, Depends
from app.services.query_service import process_query
from app.dependencies import get_current_active_user
from app.schemas import User
from ..dependencies import (
    SessionDep,
    UserDep,
)

router = APIRouter()

@router.post("/")
async def handle_query(query: str, current_user: UserDep):
    try:
        response = process_query(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

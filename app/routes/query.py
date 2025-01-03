from fastapi import APIRouter, HTTPException

from app.domain.schemas import User
from app.services.query_service import process_query

from ..dependencies import SessionDep, UserDep

router = APIRouter()


@router.post("/")
async def handle_query(query: str, current_user: UserDep):
    try:
        response = process_query(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

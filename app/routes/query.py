from fastapi import APIRouter, HTTPException

from app.services.generation_service import generate_response

from ..dependencies import SessionDep, UserDep

router = APIRouter()


@router.post("/")
async def handle_query(query: str, current_user: UserDep):
    try:
        response = generate_response(query)
        return {"response": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

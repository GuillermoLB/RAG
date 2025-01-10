from fastapi import APIRouter, HTTPException
from app.services.qa_service import generate_response

from ..dependencies import UserDep, SessionDep, SettingsDep, EmbeddingsDep, LLMDep

router = APIRouter()

@router.post("/")
async def handle_query(query: str, llm: LLMDep, current_user: UserDep, embeddings: EmbeddingsDep, settings: SettingsDep):
    try:
        response = generate_response(query, llm, embeddings, settings)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
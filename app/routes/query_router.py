from fastapi import APIRouter, HTTPException, Depends
from app.services.generation_service import generate_response, initialize_llm
from app.dependencies import get_embeddings, get_settings
from app.services.retriever_service import get_retriever
from ..dependencies import UserDep, SessionDep, SettingsDep, EmbeddingsDep

router = APIRouter()

@router.post("/")
async def handle_query(query: str, current_user: UserDep, embeddings: EmbeddingsDep, settings: SettingsDep):
    llm = initialize_llm(settings.RESPONSE_MODEL_ID)
    retriever = get_retriever("document_chunks", embeddings, settings)
    try:
        response = generate_response(query, llm, retriever)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
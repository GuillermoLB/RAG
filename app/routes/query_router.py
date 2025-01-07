from fastapi import APIRouter, HTTPException, Depends
from app.services.generation_service import generate_response, initialize_llm
from app.dependencies import get_embeddings, get_settings
from app.services.retriever_service import get_retriever
from ..dependencies import UserDep

router = APIRouter()

@router.post("/")
async def handle_query(current_user: UserDep, query: str, embeddings=Depends(get_embeddings), settings=Depends(get_settings)):
    llm = initialize_llm(settings.RESPONSE_MODEL_ID)
    retriever = get_retriever("docs", embeddings, settings)
    try:
        response = generate_response(query, llm, retriever)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
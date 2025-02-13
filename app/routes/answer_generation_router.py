from fastapi import APIRouter, HTTPException

from app.error.exceptions import RAGException
from app.services.answer_generation_service import generate_response

from ..dependencies import EmbeddingsDep, LLMDep, SettingsDep, UserDep


answer_generations = APIRouter(
    prefix="/answer_generations",
    tags=["answer_generations"],
)


@answer_generations.post("")
async def create_answer_generation(
        settings: SettingsDep,
        query: str,
        llm: LLMDep,
        current_user: UserDep,
        embeddings: EmbeddingsDep):
    try:
        response = generate_response(
            settings=settings, query=query, llm=llm, embeddings=embeddings)
        return response
    except (RAGException, HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=e.error)

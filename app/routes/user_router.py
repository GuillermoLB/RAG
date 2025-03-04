import logging
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep
from app.error.exceptions import RAGException
from app.repos.sql import user_repo
from app.domain.schemas import UserRead, UserCreate


users = APIRouter(
    tags=["users"],
    prefix="/users",
)

logger = logging.getLogger(__name__)


@users.post("",
            summary="Create a new user",
            response_model=UserRead,
            responses={
                400: {"description": "User already exists"},
                201: {"description": "User created successfully"}
            })
async def create_user(session: SessionDep, user: UserCreate):
    try:
        logger.debug(f"Creating user: {user.username}")
        user = user_repo.create_user(session, user)
        return user
    except (RAGException, HTTPException) as e:
        raise HTTPException(status_code=e.code, detail=e.error)

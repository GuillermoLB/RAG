import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import SettingsDep
from app.error.exceptions import RAGException
from app.domain.schemas import Token
from app.dependencies import SessionDep
from app.services.token_service import create_access_token
from app.services.user_service import authenticate_user

tokens = APIRouter(
    tags=["tokens"],
    prefix="/tokens",
)

logger = logging.getLogger(__name__)


@tokens.post("",
             response_model=Token,
             summary="Create access token",
             responses={
                 200: {
                     "description": "Successfully created access token",
                     "content": {
                         "application/json": {
                                    "example": {
                                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                        "token_type": "bearer"
                                    }
                         }
                     }
                 },
                 400: {
                     "description": "Incorrect username or password"
                 }
             })
async def login_for_access_token(
    settings: SettingsDep,
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()

):
    """
    Create JWT access token for authentication.

    Parameters:
    - **username**: Required username
    - **password**: Required password

    Returns:
    - **access_token**: JWT token for authentication
    - **token_type**: Bearer
    """
    try:
        user = authenticate_user(
            session, form_data.username, form_data.password)
        access_token = create_access_token(
            data={"sub": user.username}, settings=settings)
    except RAGException as e:
        raise HTTPException(status_code=e.code, detail=e.error)
    return {"access_token": access_token, "token_type": "bearer"}

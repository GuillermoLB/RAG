from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.dependencies import get_session
from app.domain import schemas
from app.repos.sql.user_repo import create_user
from app.services.authentication_service import (authenticate_user,
                                                 create_access_token)

settings = Settings()
users = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        db: Session = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, settings=settings)
    return {"access_token": access_token, "token_type": "bearer"}


@users.post("/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_session)):
    return create_user(db, user)

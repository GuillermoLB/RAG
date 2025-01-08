from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from langchain_core.embeddings import Embeddings

from app.core.config import Settings
from app.domain.models import User as UserModel
from app.domain.schemas import User
from app.services.authentication_service import verify_password, verify_token
from langchain.embeddings import HuggingFaceEmbeddings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@lru_cache
def get_settings():
    return Settings()

# Create the SQLAlchemy engine
engine = create_engine(get_settings().get_connection_str())

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_embeddings():
    return HuggingFaceEmbeddings(model_name=get_settings().EMBED_MODEL_ID)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, get_settings(),credentials_exception)
    user = db.query(UserModel).filter(UserModel.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


SessionDep = Annotated[Session, Depends(get_db)]
SettingsDep = Depends(get_settings)
UserDep = Annotated[User, Depends(get_current_active_user)]
EmbeddingsDep = Annotated[Embeddings, Depends(get_embeddings)]

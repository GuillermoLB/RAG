from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Enum


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ChunkBase(BaseModel):
    content: str
    embedding: List[float]


class ChunkCreate(ChunkBase):
    pass


class Chunk(ChunkBase):
    id: int
    document_id: int

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    title: str


class DocumentCreate(DocumentBase):
    chunks: List[ChunkCreate]


class Document(DocumentBase):
    id: int
    user_id: Optional[int]
    chunks: List[Chunk]

    class Config:
        orm_mode = True
        
class LLMType(str, Enum):
    CHAT_LLM = "CHAT"
    EMBEDDINGS = "EMBEDDINGS"
    
class LLModel(BaseModel):
    type: str
    config: dict
    fake: bool

    model_config = {
        "arbitrary_types_allowed": True
    }
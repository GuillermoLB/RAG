from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, SecretStr
from sqlalchemy import Enum

default_uuid = "00000000-0000-0000-0000-000000000001"


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: SecretStr


class UserRead(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[int] = None
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


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

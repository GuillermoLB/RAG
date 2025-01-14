from typing import Optional
from uuid import UUID

import uuid
from pgvector.sqlalchemy import Vector
from sqlalchemy import (ARRAY, JSON, Boolean, Column, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

# Create a Base class for the models
Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String, index=True)
    chunks: Mapped[Optional[int]] = mapped_column(Integer)
    uuid: Mapped[UUID] = mapped_column(index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


class LangchainPgCollection(Base):
    __tablename__ = 'langchain_pg_collection'

    name = Column(String)
    cmetadata = Column(JSON)
    uuid: Mapped[UUID] = mapped_column(primary_key=True)


class LangchainPgEmbedding(Base):
    __tablename__ = 'langchain_pg_embedding'

    collection_id: Mapped[UUID] = mapped_column(
        ForeignKey("langchain_pg_collection.uuid")
    )
    embedding = Column(Vector)
    document = Column(String)
    cmetadata = Column(JSONB)
    custom_id = Column(String)
    uuid: Mapped[UUID] = mapped_column(primary_key=True)

    collection = relationship("LangchainPgCollection", backref="embeddings")

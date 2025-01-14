from typing import Any, Optional
from uuid import UUID

import uuid
from app.core.config import Settings
from pgvector.sqlalchemy import Vector
from sqlalchemy import (ARRAY, JSON, Boolean, Column, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column, WriteOnlyMapped

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[Optional[UUID]] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    disabled: Mapped[Optional[bool]]


class LangchainPgCollection(Base):
    __tablename__ = "langchain_pg_collection"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    cmetadata: Mapped[dict[str, Any]] = mapped_column(JSONB)
    embeddings: WriteOnlyMapped["LangchainPgEmbedding"] = relationship(
        back_populates="collection",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class LangchainPgEmbedding(Base):
    __tablename__ = "langchain_pg_embedding"
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    collection_id: Mapped[UUID] = mapped_column(
        ForeignKey("langchain_pg_collection.uuid")
    )
    collection: Mapped["LangchainPgCollection"] = relationship(
        back_populates="embeddings"
    )
    embedding: Mapped[list[float]] = mapped_column(
        Vector(Settings().VECTOR_DIMENSION))
    document: Mapped[str] = mapped_column(String)
    cmetadata: Mapped[dict[str, Any]] = mapped_column(JSONB)
    custom_id: Mapped[str] = mapped_column(String)

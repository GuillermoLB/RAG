import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import (ARRAY, JSON, UUID, Boolean, Column, ForeignKey,
                        Integer, String)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship

# Create a Base class for the models
Base = declarative_base()


class document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, index=True)
    chunks = Column(Integer, nullable=True)
    uuid = Column(UUID, index=True)


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
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class LangchainPgEmbedding(Base):
    __tablename__ = 'langchain_pg_embedding'

    collection_id = Column(UUID(as_uuid=True), ForeignKey(
        'langchain_pg_collection.uuid'), nullable=False)
    embedding = Column(Vector)
    document = Column(String)
    cmetadata = Column(JSONB)
    custom_id = Column(String)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    collection = relationship("LangchainPgCollection", backref="embeddings")

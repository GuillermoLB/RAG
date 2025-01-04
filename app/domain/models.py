from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

# Create a Base class for the models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(
        Vector(384)
    )

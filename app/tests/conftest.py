import pathlib
from typing import AsyncGenerator
import uuid
from factory.alchemy import SQLAlchemyModelFactory
from factory import Sequence
from httpx import AsyncClient
import psycopg2
import pytest_asyncio
from sqlalchemy import UUID, Engine, create_engine
from app.domain.models import Document, User, Base
import pytest
from alembic import command
from alembic.config import Config
from pgvector.psycopg2 import register_vector
from app.main import app
from sqlalchemy.orm import scoped_session, sessionmaker
from langchain.vectorstores.pgvector import PGVector
from app.core.config import Settings
from app.dependencies import get_embeddings, get_settings

from app.database import database, password, port, server, user


@pytest.fixture(scope="session")
def settings() -> Settings:
    settings = get_settings()
    settings.POSTGRES_DB = "postgres_tests"
    return settings


@pytest.fixture(scope="session")
def embeddings(settings):
    embeddings = get_embeddings()
    return embeddings


@pytest.fixture(scope="session")
def engine(settings: Settings) -> Engine:
    engine = create_engine(settings.get_connection_str())
    params = {
        "database": database,
        "user": user,
        "password": password,
        "host": server,
        "port": port,
    }

    # Connect to the default database
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create the test database
    cursor.execute("DROP DATABASE IF EXISTS postgres_tests")
    cursor.execute("CREATE DATABASE postgres_tests")

    # Connect to the test database
    params["database"] = "postgres_tests"
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn_or_curs=cursor)

    return engine


@pytest.fixture(scope="session")
def tables(engine, settings: Settings, embeddings):
    alembic_cfg = Config(
        pathlib.Path(__file__).parent.parent.parent.joinpath("alembic.ini")
    )
    # alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))
    command.upgrade(alembic_cfg, "head")

    PGVector(
        collection_name="document_chunks",
        connection_string=settings.get_connection_str(),
        embedding_function=embeddings,
    )

    yield

    Base.metadata.drop_all(engine)


scopedsession = scoped_session(sessionmaker())


@pytest.fixture
def session(engine: Engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = scopedsession(autoflush=False, bind=connection)
    session.begin_nested()
    yield session
    transaction.rollback()
    # session.close()
    scopedsession.remove()


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = scopedsession
        sqlalchemy_session_persistence = "flush"
    username = "test_user"
    hashed_password = "test_password"
    disabled = False


class DocumentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Document
        sqlalchemy_session = scopedsession
        sqlalchemy_session_persistence = "flush"

    uuid = Sequence(lambda n: str(uuid.uuid4()))
    name = Sequence(lambda n: f"document{n+1}.pdf")

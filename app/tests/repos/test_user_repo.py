from uuid import uuid4

import pytest

from app.domain.schemas import UserCreate
from app.repos.sql import user_repo
from app.tests.conftest import DocumentFactory, UserFactory, session


def test_create_user(session):
    new_user = UserCreate(username="test_user", password="test_password")
    user = user_repo.create_user(session, new_user)
    assert user.username == "test_user"


def test_read_user(session):
    user = UserFactory()
    user_read = user_repo.read_user_by_name(session, user.username)
    assert user.username == user_read.username

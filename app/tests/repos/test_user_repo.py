from uuid import uuid4

import pytest

from app.domain.schemas import UserCreate
from app.repos.sql import user_repo
from app.tests.conftest import DocumentFactory, UserFactory, session


def test_create_user_works(session):
    new_user = UserCreate(username="test_user", password="test_password")
    user = user_repo.create_user(session, new_user)
    assert user.username == "test_user"

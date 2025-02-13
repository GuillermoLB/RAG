from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domain.models import User
from app.domain.schemas import UserCreate
from app.utils.authentication import get_password_hash
from ...error.codes import Errors
from ...error.exceptions import UserException


def create_user(db: Session, user: UserCreate) -> User:
    db_user = db.query(User).filter(
        User.username == user.username).first()
    if db_user:
        raise UserException(error=Errors.E001.format(
            username=db_user.username), code=400)
    hashed_password = get_password_hash(user.password.get_secret_value())
    db_user = User(
        username=user.username,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user_by_name(session: Session, username: str) -> User:
    db_user = session.query(User).filter(User.username == username).first()
    return db_user

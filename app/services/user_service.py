from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.error.codes import Errors
from app.error.exceptions import UserException
from app.repos.sql import user_repo
from app.utils.authentication import verify_password


def authenticate_user(session: Session, username: str, password: str):
    user = user_repo.read_user_by_name(session, username)
    if not user or not verify_password(password, user.hashed_password):
        raise UserException(error=Errors.E003.format(
            username=username), code=400)
    return user

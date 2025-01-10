from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domain.models import User as UserModel
from app.domain.schemas import UserCreate
from app.services.authentication_service import get_password_hash


def create_user(db: Session, user: UserCreate):
    db_user = db.query(UserModel).filter(
        UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

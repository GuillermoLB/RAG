from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from app.core.config import Settings
from app.domain.schemas import TokenData
from app.error.codes import Errors
from app.error.exceptions import AuthenticationException, UserException


def create_access_token(
        data: dict,
        settings: Settings,
        expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, settings: Settings) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthenticationException(error=Errors.E010, code=401)
        token_data = TokenData(username=username)
    except JWTError:
        raise AuthenticationException(error=Errors.E010, code=401)
    return token_data

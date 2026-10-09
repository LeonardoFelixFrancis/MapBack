from app.core.config import settings
from datetime import timedelta, datetime, timezone
from typing import Optional, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.user import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (timedelta(minutes=settings.TOKEN_EXPIRE))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (timedelta(days=settings.TOKEN_EXPIRE))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)

def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, settings.HASH_ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: IUnitOfWork = Depends(get_uow),
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if payload.get("type") != "access" or not isinstance(email, str):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with uow:
        user = uow.users.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access is required",
        )
    return current_user
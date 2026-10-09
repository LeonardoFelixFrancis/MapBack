from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from app.schemas.auth import Token, RefreshRequest
from app.core.auth import create_access_token, create_refresh_token, decode_token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork
from app.core.config import settings
from jose import JWTError

router = APIRouter(prefix="")

@router.post("/token", response_model=Token)
def login_for_access_token(response: Response, 
                           form_data: OAuth2PasswordRequestForm = Depends(), 
                           uow: IUnitOfWork = Depends(get_uow)) -> dict:
    with uow:
        user = uow.users.validate_user_password(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_refresh_token({"sub": user.email})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

        return {"access_token": access_token, "token_type": "bearer"}
        
@router.post("/refresh", response_model=Token)
def refresh_access_token(refresh_token: Optional[str] = Cookie(None)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not refresh_token:
        raise credentials_exception

    try:
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise credentials_exception

        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": username})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out"}
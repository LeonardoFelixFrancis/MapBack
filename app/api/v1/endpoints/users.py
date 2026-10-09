from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="")

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, uow: IUnitOfWork = Depends(get_uow)) -> UserResponse:
    with uow:
        service = UserService(uow)
        return service.create_user(user)

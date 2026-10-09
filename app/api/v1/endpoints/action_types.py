from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.unit_of_work import get_uow
from app.core.auth import require_admin
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.action_type import (
    ActionTypeCreate,
    ActionTypeResponse,
    ActionTypeUpdate,
)
from app.services.action_type import ActionTypeService
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("/", response_model=ActionTypeResponse, status_code=status.HTTP_201_CREATED)
def create_type(
    action_type: ActionTypeCreate,
    uow: IUnitOfWork = Depends(get_uow),
    _: UserResponse = Depends(require_admin),
) -> ActionTypeResponse:
    with uow:
        return ActionTypeService(uow).create_type(action_type)


@router.get("/", response_model=list[ActionTypeResponse])
def list_types(uow: IUnitOfWork = Depends(get_uow)) -> list[ActionTypeResponse]:
    with uow:
        return ActionTypeService(uow).list_types()


@router.get("/{type_id}", response_model=ActionTypeResponse)
def get_type(
    type_id: int, uow: IUnitOfWork = Depends(get_uow)
) -> ActionTypeResponse:
    with uow:
        action_type: ActionTypeResponse | None = ActionTypeService(uow).get_type(
            type_id
        )
        if action_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
        return action_type


@router.put("/{type_id}", response_model=ActionTypeResponse)
def update_type(
    type_id: int,
    action_type_data: ActionTypeUpdate,
    uow: IUnitOfWork = Depends(get_uow),
    _: UserResponse = Depends(require_admin),
) -> ActionTypeResponse:
    with uow:
        action_type: ActionTypeResponse | None = ActionTypeService(uow).update_type(
            type_id, action_type_data
        )
        if action_type is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
        return action_type


@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_type(
    type_id: int,
    uow: IUnitOfWork = Depends(get_uow),
    _: UserResponse = Depends(require_admin),
) -> Response:
    with uow:
        deleted = ActionTypeService(uow).delete_type(type_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

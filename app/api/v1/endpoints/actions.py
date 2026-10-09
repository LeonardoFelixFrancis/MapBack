from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.core.unit_of_work import get_uow
from app.core.auth import require_admin
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.user import UserResponse
from app.schemas.action import ActionCreate, ActionResponse, ActionUpdate
from app.services.action import ActionService

router = APIRouter()


@router.post(
    "/", response_model=ActionResponse, status_code=status.HTTP_201_CREATED
)
def create_action(
    action: ActionCreate,
    uow: IUnitOfWork = Depends(get_uow),
    _: UserResponse = Depends(require_admin),
) -> ActionResponse:
    with uow:
        return ActionService(uow).create_action(action)


@router.get("/", response_model=list[ActionResponse])
def list_actions(
    q: str | None = Query(default=None, max_length=255),
    state: list[str] = Query(default=[]),
    region: list[str] = Query(default=[]),
    uow: IUnitOfWork = Depends(get_uow),
) -> list[ActionResponse]:
    with uow:
        return ActionService(uow).list_actions(q, state, region)


@router.get("/{action_id}", response_model=ActionResponse)
def get_action(
    action_id: int, uow: IUnitOfWork = Depends(get_uow)
) -> ActionResponse:
    with uow:
        action: Optional[ActionResponse] = ActionService(uow).get_action(action_id)
        if action is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found",
            )
        return action


@router.put("/{action_id}", response_model=ActionResponse)
def update_action(
    action_id: int,
    action_data: ActionUpdate,
    uow: IUnitOfWork = Depends(get_uow),
    _: UserResponse = Depends(require_admin),
) -> ActionResponse:
    with uow:
        action: Optional[ActionResponse] = ActionService(uow).update_action(
            action_id, action_data
        )
        if action is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found",
            )
        return action


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action(
    action_id: int,
    uow: IUnitOfWork = Depends(get_uow),
    _: UserResponse = Depends(require_admin),
) -> Response:
    with uow:
        deleted = ActionService(uow).delete_action(action_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Action not found",
            )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

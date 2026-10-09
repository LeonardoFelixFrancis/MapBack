from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.auth import get_current_user
from app.core.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.favorite import FavoriteResponse
from app.schemas.user import UserResponse
from app.services.favorite import FavoriteService

router = APIRouter()


def current_user_id(current_user: UserResponse) -> int:
    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )
    return current_user.id


@router.get("/", response_model=list[FavoriteResponse])
def list_favorites(
    current_user: UserResponse = Depends(get_current_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> list[FavoriteResponse]:
    with uow:
        return FavoriteService(uow).list_favorites(current_user_id(current_user))


@router.post(
    "/{action_id}", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED
)
def add_favorite(
    action_id: int,
    current_user: UserResponse = Depends(get_current_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> FavoriteResponse:
    with uow:
        favorite = FavoriteService(uow).add_favorite(
            current_user_id(current_user), action_id
        )
        if favorite is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Action not found"
            )
        return favorite


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    action_id: int,
    current_user: UserResponse = Depends(get_current_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> Response:
    with uow:
        FavoriteService(uow).remove_favorite(current_user_id(current_user), action_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

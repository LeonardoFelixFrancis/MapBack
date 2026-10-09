from typing import Any, Protocol
from app.interfaces.repositories.action import IActionRepository
from app.interfaces.repositories.action_type import IActionTypeRepository
from app.interfaces.repositories.favorite import IFavoriteRepository
from app.interfaces.repositories.user import IUserRepository


class IUnitOfWork(Protocol):

    def __enter__(self) -> "IUnitOfWork":
        pass

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        pass

    @property
    def users(self) -> IUserRepository:
        pass

    @property
    def actions(self) -> IActionRepository:
        pass

    @property
    def action_types(self) -> IActionTypeRepository:
        pass

    @property
    def favorites(self) -> IFavoriteRepository:
        pass
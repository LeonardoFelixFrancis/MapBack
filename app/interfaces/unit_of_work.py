from typing import Any, Protocol
from app.interfaces.repositories.user import IUserRepository

class IUnitOfWork(Protocol):

    def __enter__(self) -> "IUnitOfWork":
        pass

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        pass

    @property
    def users(self) -> IUserRepository:
        pass
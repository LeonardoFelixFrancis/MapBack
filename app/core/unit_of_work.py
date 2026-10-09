from typing import Type, TypeVar, Dict, Any, Callable, Optional
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

from app.interfaces.unit_of_work import IUnitOfWork
from app.interfaces.repositories.action import IActionRepository
from app.interfaces.repositories.action_type import IActionTypeRepository
from app.interfaces.repositories.favorite import IFavoriteRepository
from app.interfaces.repositories.user import IUserRepository

from app.repositories.action import ActionRepository
from app.repositories.action_type import ActionTypeRepository
from app.repositories.favorite import FavoriteRepository
from app.repositories.user import UserRepository

T = TypeVar("T")

class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session_factory = session_factory
        self.session: Optional[Session] = None
        self._users: Optional[IUserRepository] = None
        self._actions: Optional[IActionRepository] = None
        self._action_types: Optional[IActionTypeRepository] = None
        self._favorites: Optional[IFavoriteRepository] = None

    def __enter__(self) -> "UnitOfWork":
        self.session = self.session_factory()
        return self

    @property
    def users(self) -> IUserRepository:

        if self.session is None:
            raise Exception("Db session was not created.")

        if self._users is None:
            self._users = UserRepository(self.session)
        return self._users

    @property
    def actions(self) -> IActionRepository:
        if self.session is None:
            raise Exception("Db session was not created.")

        if self._actions is None:
            self._actions = ActionRepository(self.session)
        return self._actions

    @property
    def action_types(self) -> IActionTypeRepository:
        if self.session is None:
            raise Exception("Db session was not created.")

        if self._action_types is None:
            self._action_types = ActionTypeRepository(self.session)
        return self._action_types

    @property
    def favorites(self) -> IFavoriteRepository:
        if self.session is None:
            raise Exception("Db session was not created.")

        if self._favorites is None:
            self._favorites = FavoriteRepository(self.session)
        return self._favorites


    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.session is None:
            return

        if exc_type is not None:
            self.session.rollback()
        else:
            try:
                self.session.commit()
            except Exception:
                self.session.rollback()
                raise
            finally:
                self.session.close()

def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)
from typing import Type, TypeVar, Dict, Any, Callable, Optional
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

from app.interfaces.unit_of_work import IUnitOfWork
from app.interfaces.repositories.user import IUserRepository

from app.repositories.user import UserRepository

T = TypeVar("T")

class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session_factory = session_factory
        self.session: Optional[Session] = None
        self._users: Optional[IUserRepository] = None

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
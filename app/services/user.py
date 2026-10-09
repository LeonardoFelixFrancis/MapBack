from app.interfaces.unit_of_work import IUnitOfWork
from app.schemas.user import UserCreate, UserResponse

class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def create_user(self, data: UserCreate) -> UserResponse:
        new_user = self.uow.users.create_user(data)
        return new_user
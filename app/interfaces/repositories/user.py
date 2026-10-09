from typing import Protocol, Optional
from app.schemas.user import UserResponse, UserCreate

class IUserRepository(Protocol):
    
    def get_by_email(self, email: str) -> Optional[UserResponse]:
        pass

    def create_user(self, user_data: UserCreate, flush: bool = False) -> UserResponse:
        pass

    def validate_user_password(self, email: str, password: str) -> Optional[UserResponse]:
        pass
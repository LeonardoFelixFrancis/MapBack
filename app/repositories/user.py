from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password
from typing import Optional

from app.interfaces.repositories.user import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return UserResponse.model_validate(user)

    def create_user(self, user_data: UserCreate, flush: bool=False) -> UserResponse:
        hashed_password = get_password_hash(user_data.password)

        new_user = User(
            email = user_data.email,
            password = hashed_password,
            is_admin=False,
        )

        self.db.add(new_user)

        if flush:
            self.db.flush()
            self.db.refresh(new_user)

        return UserResponse.model_validate(new_user)

    def validate_user_password(self, email: str, password: str) -> Optional[UserResponse]:
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return UserResponse.model_validate(user)


    
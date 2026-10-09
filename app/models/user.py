from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index = True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index = True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    
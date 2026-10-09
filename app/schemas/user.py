from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

    model_config = ConfigDict(extra="forbid")

class UserResponse(UserBase):
    id: Optional[int]
    is_admin: bool

    class Config:
        from_attributes = True
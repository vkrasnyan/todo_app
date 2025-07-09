from typing import Optional

from pydantic import BaseModel, Field

from constants.user import (
    MAX_NICKNAME_LENGTH,
    MIN_NICKNAME_LENGTH,
    MIN_PASSWORD_LENGTH,
)


class UserBase(BaseModel):
    username: str = Field(
        min_length=MIN_NICKNAME_LENGTH, max_length=MAX_NICKNAME_LENGTH
    )
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password_confirm: Optional[str] = None


class UserCreateDB(UserBase):
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

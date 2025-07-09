from typing import List

from pydantic import BaseModel, Field

from constants.task import (
    MAX_DESCRIPTION_LENGTH,
    MIN_DESCRIPTION_LENGTH,
)
from schemas.paginate import PaginatedResponseBase
from schemas.user import UserResponse


class TaskBase(BaseModel):
    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    title: str
    description: str = Field(
        min_length=MIN_DESCRIPTION_LENGTH, max_length=MAX_DESCRIPTION_LENGTH
    )
    is_done: bool = False


class TaskCreateDB(TaskCreate):
    owner_id: int


class TaskResponse(TaskCreate):
    id: int
    is_done: bool
    owner: UserResponse

    class Config:
        from_attributes = True


class TaskStatusUpdate(BaseModel):
    is_done: bool


class TaskPaginatedResponse(PaginatedResponseBase):
    objects: List[TaskResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

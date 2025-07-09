from pydantic import BaseModel
from typing import Optional

class TaskCollaboratorBase(BaseModel):
    task_id: int
    user_id: int
    can_read: bool = False
    can_update: bool = False

    class Config:
        from_attributes = True


class TaskCollaboratorCreate(TaskCollaboratorBase):
    pass


class TaskCollaboratorResponse(TaskCollaboratorBase):
    id: int

    class Config:
        from_attributes = True

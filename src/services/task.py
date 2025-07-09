from sqlalchemy.ext.asyncio import AsyncSession

from crud.task import task_crud
from models.user import User
from models.task import Task
from schemas.tasks import TaskCreate, TaskCreateDB


async def create(
    db: AsyncSession, create_schema: TaskCreate, owner: User
) -> Task:
    create_data = TaskCreateDB(
        owner_id=owner.id, **create_schema.model_dump(exclude_unset=True)
    )
    task = await task_crud.create(
        db=db, create_schema=create_data
    )

    return task

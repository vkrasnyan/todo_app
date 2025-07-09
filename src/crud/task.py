from typing import Optional, Sequence

from sqlalchemy import select, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.task import Task
from schemas.tasks import TaskCreate

from .async_crud import BaseAsyncCRUD


class TaskCRUD(BaseAsyncCRUD[Task, TaskCreate]):
    async def get_by_id_and_owner(
        self, db: AsyncSession, task_id: int, owner_id: int
    ) -> Optional[Task]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.owner))
            .where(
                self.model.id == task_id,
                self.model.owner_id == owner_id
            )
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_all_by_owner(
        self, db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Task]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.owner))
            .where(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update_status(
        self, db: AsyncSession, task_id: int, owner_id: int, is_done: bool
    ) -> Optional[Task]:
        stmt = (
            update(self.model)
            .where(
                self.model.id == task_id,
                self.model.owner_id == owner_id
            )
            .values(is_done=is_done)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(stmt)
        await db.commit()

        return await self.get_by_id_and_owner(db, task_id, owner_id)

    async def delete_by_id_and_owner(
        self, db: AsyncSession, task_id: int, owner_id: int
    ) -> bool:
        stmt = (
            delete(self.model)
            .where(
                self.model.id == task_id,
                self.model.owner_id == owner_id
            )
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0

    async def search_by_title(
        self, db: AsyncSession, owner_id: int, title_query: str
    ) -> Sequence[Task]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.owner))
            .where(
                self.model.owner_id == owner_id,
                self.model.title.ilike(f"%{title_query}%")
            )
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def count_by_owner(self, db: AsyncSession, owner_id: int) -> int:
        stmt = select(func.count()).select_from(self.model).where(self.model.owner_id == owner_id)
        result = await db.execute(stmt)
        return result.scalar_one()


task_crud = TaskCRUD(Task)


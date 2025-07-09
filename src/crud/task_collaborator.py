from typing import Optional, List

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.task_collaborator import TaskCollaborator
from schemas.task_collaborator import TaskCollaboratorCreate

from .async_crud import BaseAsyncCRUD


class TaskCollaboratorCRUD(BaseAsyncCRUD[TaskCollaborator, TaskCollaboratorCreate]):

    async def get_by_task_and_user(
        self, db: AsyncSession, task_id: int, user_id: int
    ) -> Optional[TaskCollaborator]:
        stmt = select(self.model).where(
            self.model.task_id == task_id,
            self.model.user_id == user_id,
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_all_by_task(
        self, db: AsyncSession, task_id: int
    ) -> List[TaskCollaborator]:
        stmt = select(self.model).where(self.model.task_id == task_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def assign_rights(
        self, db: AsyncSession, task_id: int, user_id: int, can_read: bool, can_update: bool
    ) -> TaskCollaborator:
        existing = await self.get_by_task_and_user(db, task_id, user_id)
        if existing:
            existing.can_read = can_read
            existing.can_update = can_update
            await db.commit()
            await db.refresh(existing)
            return existing

        new_collab = self.model(
            task_id=task_id,
            user_id=user_id,
            can_read=can_read,
            can_update=can_update,
        )
        db.add(new_collab)
        await db.commit()
        await db.refresh(new_collab)
        return new_collab

    async def remove_rights(
        self, db: AsyncSession, task_id: int, user_id: int
    ) -> bool:
        stmt = delete(self.model).where(
            self.model.task_id == task_id,
            self.model.user_id == user_id,
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0

    async def has_read_permission(
        self, db: AsyncSession, task_id: int, user_id: int
    ) -> bool:
        collab = await self.get_by_task_and_user(db, task_id, user_id)
        return bool(collab and collab.can_read)

    async def has_update_permission(
        self, db: AsyncSession, task_id: int, user_id: int
    ) -> bool:
        collab = await self.get_by_task_and_user(db, task_id, user_id)
        return bool(collab and collab.can_update)


task_collaborator_crud = TaskCollaboratorCRUD(TaskCollaborator)


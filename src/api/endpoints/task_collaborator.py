from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.task import task_crud
from crud.task_collaborator import task_collaborator_crud
from models.user import User
from schemas.task_collaborator import TaskCollaboratorCreate, TaskCollaboratorResponse

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=TaskCollaboratorResponse)
async def assign_permissions(
    data: TaskCollaboratorCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    task = await task_crud.get_by_id_and_owner(db, data.task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=403, detail="Not owner of the task")

    collab = await task_collaborator_crud.assign_rights(
        db, data.task_id, data.user_id, data.can_read, data.can_update
    )
    return collab


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_permissions(
    task_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    task = await task_crud.get_by_id_and_owner(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=403, detail="Not owner of the task")

    success = await task_collaborator_crud.remove_rights(db, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permissions not found")


@router.get("/check_read/", response_model=bool)
async def check_read_permission(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    has_perm = await task_collaborator_crud.has_read_permission(
        db, task_id, current_user.id
    )
    return has_perm


@router.get("/check_update/", response_model=bool)
async def check_update_permission(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    has_perm = await task_collaborator_crud.has_update_permission(
        db, task_id, current_user.id
    )
    return has_perm

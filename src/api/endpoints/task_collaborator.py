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
    if data.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already the owner of the task."
        )

    task = await task_crud.get_by_id_and_owner(
        db, task_id=data.task_id,
        owner_id=current_user.id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of the task."
        )

    collaborator = await task_collaborator_crud.assign_rights(
        db=db,
        task_id=data.task_id,
        user_id=data.user_id,
        can_read=data.can_read,
        can_update=data.can_update,
    )
    return collaborator


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_permissions(
    task_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are the owner and cannot revoke your own access."
        )

    task = await task_crud.get_by_id_and_owner(
        db, task_id=task_id, owner_id=current_user.id
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of the task."
        )

    success = await task_collaborator_crud.remove_rights(db, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permissions not found for the specified user."
        )


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

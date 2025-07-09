from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.task import task_crud
from crud.task_collaborator import task_collaborator_crud
from models.user import User
from schemas.tasks import (
    TaskCreate,
    TaskPaginatedResponse,
    TaskResponse,
    TaskStatusUpdate
)
from services import task as task_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    application: TaskCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await task_service.create(
            db=db, owner=current_user, create_schema=application
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get("/search/", response_model=list[TaskResponse])
async def search_tasks(
    query: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    return await task_crud.search_by_title(
        db=db, owner_id=current_user.id, title_query=query
    )


@router.get("/all/", response_model=TaskPaginatedResponse)
async def read_tasks(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    tasks = await task_crud.get_all_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    total = await task_crud.count_by_owner(db=db, owner_id=current_user.id)

    return TaskPaginatedResponse(
        limit=limit,
        offset=skip,
        total=total,
        objects=[TaskResponse.from_orm(task) for task in tasks]
    )


@router.get("/{task_id}/", response_model=TaskResponse)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    task = await task_crud.get_by_id_and_owner(db, task_id, current_user.id)
    if not task:
        task = await task_collaborator_crud.get_task_if_collaborator(
            db, task_id, current_user.id
        )
    if not task:
        raise HTTPException(status_code=404, detail="Not found")

    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    is_owner = await task_crud.get_by_id_and_owner(db, task_id, current_user.id)
    if is_owner:
        task = await task_crud.update_status(db, task_id, current_user.id, payload.is_done)
    else:
        has_access = await task_collaborator_crud.can_update(db, task_id, current_user.id)
        if not has_access:
            raise HTTPException(status_code=403, detail="No permission to update")
        task = await task_crud.update_by_collaborator(db, task_id, payload.is_done)

    return task


@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    deleted = await task_crud.delete_by_id_and_owner(
        db=db, task_id=task_id, owner_id=current_user.id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )

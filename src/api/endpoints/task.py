from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import get_current_user
from api.dependencies.database import get_async_db
from crud.task import task_crud
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
    if found_task := await task_crud.get_by_id_and_owner(
        db=db, task_id=task_id, owner_id=current_user.id
    ):
        return found_task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
    )


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    task = await task_crud.update_status(
        db=db,
        task_id=task_id,
        owner_id=current_user.id,
        is_done=payload.is_done,
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )
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

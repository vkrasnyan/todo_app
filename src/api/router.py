from fastapi import APIRouter

from api.endpoints.task import router as task_router
from api.endpoints.user import router as user_router
from api.endpoints.task_collaborator import router as task_collaborator_router

api_router = APIRouter(prefix="/api")
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(
    task_router, prefix="/task", tags=["Tasks"]
)

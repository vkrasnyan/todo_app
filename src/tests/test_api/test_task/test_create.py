from typing import Callable

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import user_crud
from models.task import Task
from models.user import User
from schemas.tasks import TaskCreate

ROOT_ENDPOINT = "/todo/api/task/"


class TestTaskCreate:
    async def test_create_success(
        self,
        async_session: AsyncSession,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable
    ) -> None:
        data = TaskCreate(
            username="MyUser",
            password="12345678",
            password_confirm="12345678",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 201
        await async_session.close()
        created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert created_user is not None

    async def test_create_with_invalid_password(
        self, async_session: AsyncSession, http_client: AsyncClient
    ) -> None:
        data = UserCreate(
            username="MyUser",
            password="12345678",
            password_confirm="123456789",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=data.model_dump()
        )
        assert response.status_code == 400
        await async_session.close()
        response_data = response.json()
        assert response_data["detail"] == "Passwords don't match!"
        not_created_user = await user_crud.get_by_username(
            db=async_session, username=data.username
        )
        assert not_created_user is None

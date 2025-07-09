from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserLogin

ROOT_ENDPOINT = "/todo/api/user/"


class TestLogin:
    async def test_login_success(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserLogin(username=user_fixture.username, password="secret")
        response = await http_client.post(
            f"{ROOT_ENDPOINT}login/", json=data.model_dump()
        )
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"
        refresh_token = tokens["refresh_token"]
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = await http_client.post(
            ROOT_ENDPOINT + "refresh/", json=data.model_dump(), headers=headers
        )
        assert response.status_code == 200
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"

    async def test_login_invalid_password(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserLogin(
            username=user_fixture.username, password="another password"
        )
        response = await http_client.post(
            f"{ROOT_ENDPOINT}login/", json=data.model_dump()
        )
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["detail"] == f"Wrong username or password!"

    async def test_login_invalid_username(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = UserLogin(username="wrong username", password="secret")
        response = await http_client.post(
            ROOT_ENDPOINT + "login/", json=data.model_dump()
        )
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == f"User {data.username} not found."

    async def test_login_blank_data(
        self,
        http_client: AsyncClient,
        async_session: AsyncSession,
        user_fixture: User,
    ) -> None:
        data = {}
        response = await http_client.post(f"{ROOT_ENDPOINT}login/", json=data)
        assert response.status_code == 422

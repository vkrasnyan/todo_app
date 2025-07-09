from httpx import AsyncClient

from models.user import User

ROOT_ENDPOINT = "/todo/api/user/"


class TestAuthLogout:
    async def test_logout_clears_cookies(
            self,
            http_client: AsyncClient,
            user_fixture: User,
    ) -> None:
        endpoint_login = f"{ROOT_ENDPOINT}login/"
        endpoint_logout = f"{ROOT_ENDPOINT}logout/"
        response = await http_client.post(endpoint_login, json={
            "username": user_fixture.username,
            "password": "secret"
        })
        assert response.status_code == 200

        data = response.json()
        access_token = data["access_token"]

        response = await http_client.delete(
            endpoint_logout,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 204

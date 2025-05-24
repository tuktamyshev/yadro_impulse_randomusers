from unittest.mock import AsyncMock
from uuid import uuid4

from starlette.testclient import TestClient

from adapters.user_repository import UserListDTO, UserReadDTO


class TestHomepage:
    def test_homepage(self, client: TestClient, user_repo: AsyncMock, fake_user: UserReadDTO) -> None:
        user_repo.get_list.return_value = UserListDTO(
            items=[fake_user],
            total=1,
        )
        response = client.get("/homepage")
        assert response.status_code == 200
        assert "John" in response.text
        assert "Doe" in response.text
        assert "john@example.com" in response.text
        assert "1234567890" in response.text

    def test_homepage_random_user_success(
        self, client: TestClient, user_repo: AsyncMock, fake_user: UserReadDTO
    ) -> None:
        user_repo.get_random_user.return_value = fake_user
        response = client.get("/homepage/random")
        assert response.status_code == 200
        assert "John" in response.text
        assert "Doe" in response.text
        assert "john@example.com" in response.text
        assert "1234567890" in response.text

    def test_homepage_random_user_not_found(self, client: TestClient, user_repo: AsyncMock) -> None:
        user_repo.get_random_user.return_value = None
        response = client.get("/homepage/random")
        assert response.status_code == 404
        assert response.json() == {"detail": "Нет доступных пользователей"}

    def test_homepage_user_detail_success(
        self, client: TestClient, user_repo: AsyncMock, fake_user: UserReadDTO
    ) -> None:
        user_repo.get_by_uuid_or_none.return_value = fake_user
        response = client.get(f"/homepage/{fake_user.uuid}")
        assert response.status_code == 200
        assert "John" in response.text
        assert "Doe" in response.text
        assert "john@example.com" in response.text
        assert "1234567890" in response.text

    def test_homepage_user_detail_not_found(self, client: TestClient, user_repo: AsyncMock) -> None:
        user_repo.get_by_uuid_or_none.return_value = None
        response = client.get(f"/homepage/{uuid4()}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Пользователь не найден"}

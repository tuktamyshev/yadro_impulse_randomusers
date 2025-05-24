from unittest.mock import AsyncMock

from dishka import Provider, provide

from adapters.user_service import UserService


class MockUserServiceProvider(Provider):
    @provide
    def users_service(self) -> UserService:
        return AsyncMock()

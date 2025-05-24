from unittest.mock import AsyncMock

from dishka import Provider, provide

from adapters.user_repository import UserRepository


class MockRepositoriesProvider(Provider):
    @provide
    def user_repository(self) -> UserRepository:
        return AsyncMock()

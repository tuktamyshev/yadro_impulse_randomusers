from typing import AsyncIterable
from unittest.mock import AsyncMock

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


class MockDatabaseProvider(Provider):
    @provide
    def db_engine(self) -> AsyncEngine:
        return AsyncMock()

    @provide
    def db_sessionmaker(
        self,
    ) -> async_sessionmaker[AsyncSession]:
        return AsyncMock()

    @provide(scope=Scope.REQUEST)
    async def db_session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as _:
            yield AsyncMock()

from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config.db import DatabaseConfig


class SQLAlchemyDatabaseProvider(Provider):
    @provide
    def db_engine(self, config: DatabaseConfig) -> AsyncEngine:
        return create_async_engine(
            config.URI,
            echo=config.ECHO,
            echo_pool=config.ECHO_POOL,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
        )

    @provide
    def db_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def db_session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.user_repository import UserRepository


class SQLAlchemyRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)

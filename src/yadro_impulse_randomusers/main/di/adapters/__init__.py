from dishka import Scope

from main.di.adapters.database import SQLAlchemyDatabaseProvider
from main.di.adapters.repositories import SQLAlchemyRepositoriesProvider
from main.di.adapters.transaction_manager import SQLAlchemyTransactionManagerProvider
from main.di.adapters.users_service import UserServiceProvider


class AdaptersProvider(
    SQLAlchemyDatabaseProvider,
    SQLAlchemyTransactionManagerProvider,
    SQLAlchemyRepositoriesProvider,
    UserServiceProvider,
):
    scope = Scope.APP

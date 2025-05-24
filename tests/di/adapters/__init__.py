from dishka import Scope

from main.di.adapters.database import SQLAlchemyDatabaseProvider as SQLAlchemyDatabaseProvider
from main.di.adapters.repositories import SQLAlchemyRepositoriesProvider as SQLAlchemyRepositoriesProvider
from main.di.adapters.transaction_manager import (
    SQLAlchemyTransactionManagerProvider as SQLAlchemyTransactionManagerProvider,
)
from main.di.adapters.users_service import UserServiceProvider as UserServiceProvider
from tests.di.adapters.database import MockDatabaseProvider
from tests.di.adapters.repositories import MockRepositoriesProvider
from tests.di.adapters.transaction_manager import MockTransactionManagerProvider
from tests.di.adapters.user_service import MockUserServiceProvider


class MockAdaptersProvider(
    MockDatabaseProvider,
    MockTransactionManagerProvider,
    MockRepositoriesProvider,
    MockUserServiceProvider,
):
    scope = Scope.APP

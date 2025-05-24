from unittest.mock import AsyncMock

from dishka import Provider, Scope, provide

from adapters.transaction_manager import TransactionManager


class MockTransactionManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def transaction_manager(self) -> TransactionManager:
        return AsyncMock()

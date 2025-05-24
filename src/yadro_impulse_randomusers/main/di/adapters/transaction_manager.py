from dishka import Provider, Scope, provide

from adapters.transaction_manager import TransactionManager


class SQLAlchemyTransactionManagerProvider(Provider):
    transaction_manager = provide(TransactionManager, scope=Scope.REQUEST)

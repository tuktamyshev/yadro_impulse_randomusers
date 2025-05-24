from dishka import Provider, Scope, provide

from adapters.user_service import UserService


class UserServiceProvider(Provider):
    users_service = provide(UserService, scope=Scope.REQUEST)

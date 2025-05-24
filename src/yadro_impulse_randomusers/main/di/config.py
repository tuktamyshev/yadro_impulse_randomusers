from dishka import Provider, Scope, from_context, provide

from config.app import AppConfig
from config.config import Config
from config.db import DatabaseConfig


class ConfigProvider(Provider):
    scope = Scope.APP

    config = from_context(provides=Config)

    @provide
    def app_config(self, config: Config) -> AppConfig:
        return config.app

    @provide
    def db_config(self, config: Config) -> DatabaseConfig:
        return config.db

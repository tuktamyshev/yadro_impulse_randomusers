from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from config.config import Config
from main.di.config import ConfigProvider
from tests.di.adapters import MockAdaptersProvider


def init_test_di(app: FastAPI) -> None:
    config = app.state.config

    container = test_container_factory(config=config)

    setup_dishka(container, app)


def test_container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        MockAdaptersProvider(),
        FastapiProvider(),
        context={Config: config},
    )

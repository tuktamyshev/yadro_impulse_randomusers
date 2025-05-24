from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from config.config import Config
from main.di.adapters import AdaptersProvider
from main.di.config import ConfigProvider


def init_web_di(app: FastAPI) -> None:
    config = app.state.config

    container = web_container_factory(config=config)

    setup_dishka(container, app)


def web_container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        AdaptersProvider(),
        FastapiProvider(),
        context={Config: config},
    )

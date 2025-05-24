from typing import AsyncGenerator
from uuid import uuid4

import pytest
from dishka import AsyncContainer
from fastapi import FastAPI
from fastapi.testclient import TestClient

from adapters.constants import Gender
from adapters.user_repository import UserReadDTO, UserRepository
from config.config import Config
from presentation import main_http_router
from tests.di import init_test_di


@pytest.fixture
def app() -> FastAPI:
    config = Config()
    app = FastAPI()
    app.state.config = config
    app.include_router(main_http_router)

    init_test_di(app)
    return app


@pytest.fixture
async def container(app: FastAPI) -> AsyncGenerator[AsyncContainer, ...]:
    container = app.state.dishka_container
    yield container
    await container.close()


@pytest.fixture
async def user_repo(container: AsyncContainer) -> UserRepository:
    return await container.get(UserRepository)


@pytest.fixture
async def fake_user() -> UserReadDTO:
    return UserReadDTO(
        uuid=uuid4(),
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="1234567890",
        address="New York",
        gender=Gender.male.value,
        photo_url="https://example.com/photo.jpg",
    )


@pytest.fixture
def client(app: FastAPI) -> [TestClient, ...]:
    with TestClient(app) as client:
        yield client

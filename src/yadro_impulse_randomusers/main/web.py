import sys
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

sys.path.append(str(Path(__file__).resolve().parent.parent))

from adapters.user_service import UserService
from config.config import Config
from main.di import init_web_di
from main.exception_handlers import init_exceptions_handlers
from main.logs import setup_logging
from presentation import main_http_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager[None]:
    async with app.state.dishka_container() as request_container:
        users_service = await request_container.get(UserService)
        await users_service.fetch_users_on_server_startup(1000)
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    config = Config()
    app = FastAPI(
        default_response_class=ORJSONResponse,
        title="Yadro Impulse Randomusers",
        docs_url="/docs",
        description="Yadro Impulse Randomusers",
        lifespan=lifespan,
    )

    app.state.config = config

    init_web_di(app)
    app.include_router(main_http_router)
    init_exceptions_handlers(app)
    setup_logging()

    return app


if __name__ == "__main__":
    uvicorn.run("web:create_app", port=8000, factory=True, reload=True)

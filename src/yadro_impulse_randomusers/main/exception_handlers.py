import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from starlette import status
from starlette.responses import Response

from adapters.exceptions import ApplicationException

logger = logging.getLogger("webserver")


def init_exceptions_handlers(app: FastAPI) -> None:
    # Handler for expected server errors
    @app.exception_handler(ApplicationException)
    @app.exception_handler(HTTPException)
    async def application_exception_handler(request: Request, exc: ApplicationException) -> Response:
        http_exc = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        )

        return await http_exception_handler(request, http_exc)

    # Handler for unexpected server errors
    @app.exception_handler(Exception)
    async def internal_server_error_handler(request: Request, exc: Exception) -> Response:
        logger.exception(f"{request.url}: {exc}")
        http_exc = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
        return await http_exception_handler(request, http_exc)

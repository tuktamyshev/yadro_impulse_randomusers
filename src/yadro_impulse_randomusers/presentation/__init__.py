from fastapi import APIRouter
from starlette import status

from presentation.dtos.exception import ApplicationExceptionSchema
from presentation.rest import router as user_router

__all__ = ["main_http_router"]

routers = [
    # rest
    user_router,
]

main_http_router = APIRouter(
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ApplicationExceptionSchema},
    },
)

for router in routers:
    main_http_router.include_router(router)

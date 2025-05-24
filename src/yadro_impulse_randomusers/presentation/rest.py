import os
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, Query
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from adapters.user_repository import UserRepository
from adapters.user_service import UserService
from config import BASE_DIR

router = APIRouter(
    route_class=DishkaRoute,
)
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "src", "yadro_impulse_randomusers", "presentation", "templates")
)


@router.get("/")
async def redirect_to_homepage() -> RedirectResponse:
    return RedirectResponse(url="/homepage")


@router.get("/homepage", response_class=HTMLResponse)
async def homepage(
    user_repository: FromDishka[UserRepository],
    request: Request,
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
) -> HTMLResponse:
    users = await user_repository.get_list(limit, offset)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "total": users.total,
            "users": users.items,
            "limit": limit,
            "offset": offset,
            "has_more": limit + offset < users.total,
        },
    )


@router.get("/homepage/random", response_class=HTMLResponse)
async def random_user(
    request: Request,
    user_repository: FromDishka[UserRepository],
) -> HTMLResponse:
    user = await user_repository.get_random_user()
    if not user:
        raise HTTPException(status_code=404, detail="Нет доступных пользователей")

    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})


@router.get("/homepage/{user_id}", response_class=HTMLResponse)
async def homepage_user_detail(
    user_repository: FromDishka[UserRepository],
    request: Request,
    user_id: UUID,
) -> HTMLResponse:
    user = await user_repository.get_by_uuid_or_none(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return templates.TemplateResponse(
        "user_detail.html",
        {
            "request": request,
            "user": user,
        },
    )


@router.get("/fetch_users")
async def fetch_users(
    user_service: FromDishka[UserService],
    count: int = Query(10, gt=0, le=100),
) -> RedirectResponse:
    await user_service.fetch_users(count)
    return RedirectResponse(url="/homepage", status_code=303)

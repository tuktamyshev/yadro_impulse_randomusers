from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.constants import Gender
from adapters.orm.user import UserORM


class UserReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    gender: Gender
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str
    photo_url: str


class UserListDTO(BaseModel):
    total: int
    items: list[UserReadDTO]


class CreateUserDTO(BaseModel):
    uuid: UUID
    created_at: datetime
    gender: Gender
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    address: str
    photo_url: str


@dataclass(frozen=True)
class UserRepository:
    session: AsyncSession
    model: UserORM = UserORM

    async def get_list(self, limit: int, offset: int) -> UserListDTO:
        query = (
            select(
                UserORM,
                func.count().over().label("total_count"),
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)

        rows = result.all()

        users_list = []
        total_count = 0
        for (
            user,
            count,
        ) in rows:
            users_list.append(UserReadDTO.model_validate(user))
            total_count = count

        return UserListDTO(items=users_list, total=total_count)

    async def create_users(self, users: list[CreateUserDTO]) -> None:
        orm_models = [self.model(**user.model_dump()) for user in users]
        self.session.add_all(orm_models)
        await self.session.flush()

    async def get_by_uuid_or_none(self, uuid: UUID) -> UserReadDTO | None:
        query = select(self.model).filter_by(uuid=uuid)

        res = await self.session.execute(query)
        orm_model = res.scalar_one_or_none()
        if orm_model:
            return UserReadDTO.model_validate(orm_model)

    async def count_users(self) -> int:
        count = await self.session.scalar(select(func.count()).select_from(UserORM))
        return count

    async def get_random_user(self) -> UserReadDTO | None:
        query = select(self.model).order_by(func.random()).limit(1)

        res = await self.session.execute(query)
        orm_model = res.scalar_one()
        if orm_model:
            return UserReadDTO.model_validate(orm_model)

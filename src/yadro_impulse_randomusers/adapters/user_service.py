import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import httpx

from adapters.constants import Gender
from adapters.transaction_manager import TransactionManager
from adapters.user_repository import CreateUserDTO, UserRepository

logger = logging.getLogger("user")


@dataclass(frozen=True)
class UserService:
    user_repository: UserRepository
    transaction_manager: TransactionManager

    async def fetch_users_on_server_startup(self, count: int) -> None:
        users_count = await self.user_repository.count_users()
        logger.debug(f"В БД {users_count} пользователей")
        if users_count < count:
            logger.debug(f"Будет загружено ещё {count - users_count} пользователей")
            await self.fetch_users(count - users_count)

    async def fetch_users(self, count: int) -> None:
        logger.debug(f"Запрос на загрузку {count} пользователей")
        url = f"https://randomuser.me/api/?results={count}&inc=gender,name,email,phone,picture,location"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            users_info = response.json()["results"]

        users_dto = []
        for user_info in users_info:
            users_dto.append(
                CreateUserDTO(
                    uuid=uuid4(),
                    created_at=datetime.now(UTC),
                    gender=self._parse_gener(user_info["gender"]),
                    first_name=user_info["name"]["first"],
                    last_name=user_info["name"]["last"],
                    email=user_info["email"],
                    phone_number=user_info["phone"],
                    address=self._parse_address(user_info["location"]),
                    photo_url=user_info["picture"]["large"],
                )
            )

        async with self.transaction_manager:
            await self.user_repository.create_users(users_dto)
        logger.debug(f"{count} пользователей загружено в БД")

    @staticmethod
    def _parse_address(location: dict) -> str:
        address = (
            f"{location['country']},"
            f" {location['state']},"
            f" {location['city']},"
            f" {location['street']['name']} {location['street']['number']}"
        )
        return address

    @staticmethod
    def _parse_gener(gender: str) -> Gender:
        if gender == "male":
            return Gender.male.value
        elif gender == "female":
            return Gender.female.value

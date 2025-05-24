from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from adapters.constants import Gender
from adapters.orm.base import BaseORM


class UserORM(BaseORM):
    gender: Mapped["Gender"]
    first_name: Mapped[str] = mapped_column(String(length=320))
    last_name: Mapped[str] = mapped_column(String(length=320))
    email: Mapped[str] = mapped_column(String(length=1024))
    phone_number: Mapped[str] = mapped_column(String(length=320))
    address: Mapped[str] = mapped_column(String(length=1024))
    photo_url: Mapped[str] = mapped_column(String(length=1024))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(uuid={self.uuid}, email={self.email!r})"

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import BASE_DIR
from config.app import AppConfig
from config.db import DatabaseConfig


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(f"{BASE_DIR}/env/.env.default", f"{BASE_DIR}/env/.env"),
        env_nested_delimiter="__",
    )

    app: AppConfig
    db: DatabaseConfig

from pydantic import BaseModel


class AppConfig(BaseModel):
    API_PORT: int

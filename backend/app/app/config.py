from typing import Any

from pydantic import AnyHttpUrl, validator
from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    API_STR: str
    PROJECT_NAME: str

    REDIS_URL: str
    CACHE_TTL: int


settings = Settings()

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(
        ..., validation_alias=AliasChoices("DATABASE_URL", "POSTGRES_URL")
    )
    redis_url: str = Field(
        ..., validation_alias=AliasChoices("REDIS_URL",)
    )
    secret_key: str = Field(
        ..., validation_alias=AliasChoices("SECRET_KEY",)
    )


settings = Settings()

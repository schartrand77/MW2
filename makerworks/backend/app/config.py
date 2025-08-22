from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+psycopg://makerworks:makerworks@postgres:5432/makerworks",
        validation_alias=AliasChoices("DATABASE_URL", "POSTGRES_URL"),
    )
    redis_url: str = Field(
        default="redis://redis:6379/0",
        validation_alias=AliasChoices("REDIS_URL",),
    )
    secret_key: str = Field(default="change-me", validation_alias=AliasChoices("SECRET_KEY",))


settings = Settings()

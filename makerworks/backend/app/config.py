from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://makerworks:makerworks@postgres:5432/makerworks"
    )
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-me"


settings = Settings()

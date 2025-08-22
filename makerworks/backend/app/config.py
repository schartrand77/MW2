from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://makerworks:makerworks@postgres:5432/makerworks"
    )
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-me"
    stripe_secret_key: str = "sk_test_123"
    stripe_webhook_secret: str = "whsec_test"
    frontend_url: str = "http://localhost:5173"
    amazon_associate_tag: str | None = None
    amazon_paapi_access_key: str | None = None
    amazon_paapi_secret_key: str | None = None


settings = Settings()

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
    sendgrid_api_key: str | None = Field(default=None, validation_alias=AliasChoices("SENDGRID_API_KEY",))
    twilio_account_sid: str | None = Field(default=None, validation_alias=AliasChoices("TWILIO_ACCOUNT_SID",))
    twilio_auth_token: str | None = Field(default=None, validation_alias=AliasChoices("TWILIO_AUTH_TOKEN",))
    twilio_from_number: str | None = Field(default=None, validation_alias=AliasChoices("TWILIO_FROM_NUMBER",))
    vapid_public_key: str | None = Field(default=None, validation_alias=AliasChoices("PUSH_VAPID_PUBLIC_KEY",))
    vapid_private_key: str | None = Field(default=None, validation_alias=AliasChoices("PUSH_VAPID_PRIVATE_KEY",))
    discord_bot_token: str | None = Field(default=None, validation_alias=AliasChoices("DISCORD_BOT_TOKEN",))
    discord_channel_id: str | None = Field(default=None, validation_alias=AliasChoices("DISCORD_CHANNEL_ID",))
    plugins_raw: str = Field(default="", validation_alias=AliasChoices("PLUGINS",))

    @property
    def plugins(self) -> list[str]:
        return [p.strip() for p in self.plugins_raw.split(",") if p.strip()]


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "INFO"


config = Config()

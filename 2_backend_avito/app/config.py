from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    database_url: str = (
        "postgresql://urlshortener:urlshortener@localhost:5432/urlshortener"
    )
    base_url: str = "http://localhost:8000"
    code_length: int = 6


settings = Settings()

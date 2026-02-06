"""Application configuration module."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    # Database settings (components)
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "urlshortener"
    database_password: str = "urlshortener"
    database_name: str = "urlshortener"

    # Application settings (components)
    base_url_scheme: str = "http"
    base_url_host: str = "localhost"
    base_url_port: int = 8000

    code_length: int = 6
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    _database_url: Optional[str] = Field(None, alias="DATABASE_URL")
    _base_url: Optional[str] = Field(None, alias="BASE_URL")

    @property
    def database_url(self) -> str:
        """Get database URL from full URL or build from components."""
        if self._database_url:
            return self._database_url
        return (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def base_url(self) -> str:
        """Get base URL from full URL or build from components."""
        if self._base_url:
            return self._base_url
        return (
            f"{self.base_url_scheme}://{self.base_url_host}:{self.base_url_port}"
        )


settings = Settings()

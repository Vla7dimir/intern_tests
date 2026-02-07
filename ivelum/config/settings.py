"""Application settings (host, port, Hacker News URL)."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Proxy server and upstream URL configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    host: str = Field(
        default="127.0.0.1",
        description="Host to bind the server.",
    )
    port: int = Field(
        default=8232,
        ge=1,
        le=65535,
        description="Port to bind the server.",
    )
    hn_base_url: str = Field(
        default="https://news.ycombinator.com",
        description="Base URL of Hacker News.",
    )
    request_timeout: float = Field(
        default=30.0,
        gt=0,
        le=300.0,
        description="Request timeout to upstream (seconds).",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )
    max_response_size: int = Field(
        default=10 * 1024 * 1024,  # 10MB
        gt=0,
        description="Maximum response size in bytes.",
    )

    @field_validator("hn_base_url")
    @classmethod
    def validate_hn_url(cls, v: str) -> str:
        """Validate HN base URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("hn_base_url must start with http:// or https://")
        return v.rstrip("/")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()


settings = Settings()

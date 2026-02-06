"""Application settings module."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    base_url: str = "http://localhost:8000"
    database_url: str = "sqlite:///./abtesting.db"
    log_level: str = "INFO"

    # Used by data migration (env BUTTON_COLOR_OPTIONS / PRICE_OPTIONS).
    # Format: "value1:weight1,value2:weight2,..."
    button_color_options: str = "#FF0000:33,#00FF00:33,#0000FF:34"
    price_options: str = "10:75,20:10,50:5,5:10"


settings = Settings()

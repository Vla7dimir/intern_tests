from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator

from app.utils import check_code, check_url


class CreateRequest(BaseModel):
    """Request schema for URL shortening."""

    url: str
    code: Optional[str] = Field(None, min_length=3, max_length=50)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format and accessibility."""
        if not check_url(v):
            raise ValueError("Invalid URL")
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate code format if provided."""
        if v is not None and not check_code(v):
            raise ValueError(
                "Code must be 3-50 alphanumeric characters, "
                "hyphens, or underscores"
            )
        return v


class CreateResponse(BaseModel):
    """Response schema for URL shortening."""

    short: str
    original: str
    code: str

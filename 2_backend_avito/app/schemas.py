from typing import Optional

from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    """Request schema for URL shortening."""

    url: str
    code: Optional[str] = Field(None, min_length=3, max_length=50)


class CreateResponse(BaseModel):
    """Response schema for URL shortening."""

    short: str
    original: str
    code: str

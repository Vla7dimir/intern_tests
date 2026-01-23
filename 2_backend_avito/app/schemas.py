from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    url: str
    code: str | None = Field(None, min_length=3, max_length=50)


class CreateResponse(BaseModel):
    short: str
    original: str
    code: str

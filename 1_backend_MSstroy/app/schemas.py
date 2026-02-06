from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class ItemIdRequest(BaseModel):
    """Request schema for item ID operations."""

    id: int = Field(..., gt=0, description="Item ID must be positive integer") 


class TreeStoreRequest(BaseModel):
    """Request schema for tree initialization."""

    items: List[Dict[str, object]] = Field(..., min_length=1, description="List of items")

    @field_validator("items")
    @classmethod
    def validate_items(cls, v: List[Dict[str, object]]) -> List[Dict[str, object]]:
        """Validate items structure."""
        if not v:
            raise ValueError("Items list cannot be empty")
        for item in v:
            if "id" not in item:
                raise ValueError("Each item must have 'id' field")
            if not isinstance(item["id"], int):
                raise ValueError("Item 'id' must be an integer")
            if item["id"] <= 0:
                raise ValueError("Item 'id' must be positive")
        return v


class TreeStoreResponse(BaseModel):
    """Response schema for tree operations."""

    result: Union[List[Dict[str, object]], Dict[str, object], None]

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class ItemIdRequest(BaseModel):
    """Request schema for item ID operations."""

    id: int  #


class TreeStoreRequest(BaseModel):
    """Request schema for tree initialization."""

    items: List[Dict[str, object]]


class TreeStoreResponse(BaseModel):
    """Response schema for tree operations."""

    result: Union[List[Dict[str, object]], Dict[str, object], None]

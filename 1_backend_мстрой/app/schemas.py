from typing import Any, Dict, List

from pydantic import BaseModel


class ItemIdRequest(BaseModel):
    id: Any


class TreeStoreRequest(BaseModel):
    items: List[Dict[str, Any]]


class TreeStoreResponse(BaseModel):
    result: List[Dict[str, Any]] | Dict[str, Any] | None

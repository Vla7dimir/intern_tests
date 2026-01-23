"""Pydantic schemas for API."""

from typing import Any, Dict, List

from pydantic import BaseModel


class ItemIdRequest(BaseModel):
    """Request with item id."""

    id: Any


class TreeStoreRequest(BaseModel):
    """Request to initialize tree."""

    items: List[Dict[str, Any]]


class TreeStoreResponse(BaseModel):
    """Response from tree operations."""

    result: List[Dict[str, Any]] | Dict[str, Any] | None

"""FastAPI application for TreeStore API.

This module provides REST API endpoints for tree structure operations.
Business logic is separated into service layer (app.service).
"""

import json
import threading
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException, Request, status

from app.exceptions import ItemNotFoundError
from app.logger import get_logger, setup_logging
from app.models import TreeStore
from app.schemas import ItemIdRequest, TreeStoreRequest, TreeStoreResponse
from app.service import TreeStoreService

setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="TreeStore API",
    version="1.0.0",
    description="REST API for tree structure operations with parent-child relationships",
)

_DATA_FILE = Path(__file__).parent / "data" / "default_items.json"
_lock = threading.Lock()


def _load_default_items() -> list[Dict[str, object]]:
    """Load default items from JSON file.

    Returns:
        List of default items.

    Raises:
        FileNotFoundError: If default items file not found.
        json.JSONDecodeError: If file contains invalid JSON.
    """
    try:
        with open(_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Default items file not found: {_DATA_FILE}, using empty list")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {_DATA_FILE}: {e}")
        raise ValueError(f"Invalid JSON in {_DATA_FILE}: {e}") from e


_default_items = _load_default_items()
_tree_store = TreeStore(_default_items)
_tree_service = TreeStoreService(_tree_store)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    logger.info(
        "Incoming request",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None,
        },
    )
    try:
        response = await call_next(request)
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
            },
        )
        return response
    except Exception as e:
        logger.error(
            "Request failed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "error": str(e),
            },
            exc_info=True,
        )
        raise


@app.post(
    "/api/v1/tree/init",
    response_model=TreeStoreResponse,
    tags=["Tree Management"],
    summary="Initialize tree",
    description="Initialize tree structure with new items. Replaces existing tree.",
    responses={
        200: {
            "description": "Tree initialized successfully",
            "content": {
                "application/json": {
                    "example": {
                        "result": {
                            "status": "initialized",
                            "items_count": 8,
                        }
                    }
                }
            },
        },
        400: {"description": "Invalid items structure"},
        500: {"description": "Internal server error"},
    },
)
def init_tree(request: TreeStoreRequest) -> TreeStoreResponse:
    """Initialize tree with new items.

    Args:
        request: TreeStoreRequest with items to initialize.

    Returns:
        TreeStoreResponse with initialization status and items count.

    Raises:
        HTTPException: If initialization fails (400/500).
    """
    logger.info("Initializing tree", extra={"items_count": len(request.items)})
    try:
        with _lock:
            global _tree_service
            result = _tree_service.initialize_tree(request.items)
            _tree_service = TreeStoreService(_tree_service.tree_store)
        logger.info("Tree initialized successfully", extra={"items_count": len(request.items)})
        return TreeStoreResponse(result=result)
    except ValueError as e:
        logger.warning("Invalid items structure", extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid items structure: {str(e)}",
        ) from e
    except Exception as e:
        logger.error("Failed to initialize tree", extra={"error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize tree",
        ) from e


@app.get(
    "/api/v1/tree/getAll",
    response_model=TreeStoreResponse,
    tags=["Tree Operations"],
    summary="Get all items",
    description="Retrieve all items from the tree structure",
    responses={
        200: {
            "description": "List of all items",
            "content": {
                "application/json": {
                    "example": {
                        "result": [
                            {"id": 1, "parent": "root"},
                            {"id": 2, "parent": 1, "type": "test"},
                        ]
                    }
                }
            },
        },
        500: {"description": "Internal server error"},
    },
)
def get_all() -> TreeStoreResponse:
    """Get all items from the tree.

    Returns:
        TreeStoreResponse with all items in the tree.

    Raises:
        HTTPException: If operation fails (500).
    """
    try:
        result = _tree_service.get_all_items()
        logger.debug("Retrieved all items", extra={"count": len(result)})
        return TreeStoreResponse(result=result)
    except Exception as e:
        logger.error("Failed to get all items", extra={"error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get all items",
        ) from e


@app.post(
    "/api/v1/tree/getItem",
    response_model=TreeStoreResponse,
    tags=["Tree Operations"],
    summary="Get item by ID",
    description="Retrieve a specific item from the tree by its ID",
    responses={
        200: {
            "description": "Item found",
            "content": {
                "application/json": {
                    "example": {"result": {"id": 1, "parent": "root"}}
                }
            },
        },
        404: {"description": "Item not found"},
        500: {"description": "Internal server error"},
    },
)
def get_item(request: ItemIdRequest) -> TreeStoreResponse:
    """Get item by ID.

    Args:
        request: ItemIdRequest with item ID.

    Returns:
        TreeStoreResponse with item data.

    Raises:
        HTTPException: If item not found (404) or operation fails (500).
    """
    logger.debug("Getting item by ID", extra={"item_id": request.id})
    try:
        result = _tree_service.get_item_by_id(request.id)
        logger.debug("Item found", extra={"item_id": request.id})
        return TreeStoreResponse(result=result)
    except ItemNotFoundError as e:
        logger.warning("Item not found", extra={"item_id": request.id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Failed to get item", extra={"item_id": request.id, "error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get item",
        ) from e


@app.post(
    "/api/v1/tree/getChildren",
    response_model=TreeStoreResponse,
    tags=["Tree Operations"],
    summary="Get children of an item",
    description="Retrieve all direct children of a specific item",
    responses={
        200: {
            "description": "List of children items",
            "content": {
                "application/json": {
                    "example": {
                        "result": [
                            {"id": 2, "parent": 1, "type": "test"},
                            {"id": 3, "parent": 1, "type": "test"},
                        ]
                    }
                }
            },
        },
        500: {"description": "Internal server error"},
    },
)
def get_children(request: ItemIdRequest) -> TreeStoreResponse:
    """Get children of an item.

    Args:
        request: ItemIdRequest with parent item ID.

    Returns:
        TreeStoreResponse with children items (empty list if no children).

    Raises:
        HTTPException: If operation fails (500).
    """
    logger.debug("Getting children", extra={"parent_id": request.id})
    try:
        result = _tree_service.get_children(request.id)
        logger.debug("Children retrieved", extra={"parent_id": request.id, "count": len(result)})
        return TreeStoreResponse(result=result)
    except Exception as e:
        logger.error("Failed to get children", extra={"parent_id": request.id, "error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get children",
        ) from e


@app.post(
    "/api/v1/tree/getAllParents",
    response_model=TreeStoreResponse,
    tags=["Tree Operations"],
    summary="Get all parents of an item",
    description="Retrieve all parent items from the given item up to root",
    responses={
        200: {
            "description": "List of parent items",
            "content": {
                "application/json": {
                    "example": {
                        "result": [
                            {"id": 4, "parent": 2, "type": "test"},
                            {"id": 2, "parent": 1, "type": "test"},
                            {"id": 1, "parent": "root"},
                        ]
                    }
                }
            },
        },
        500: {"description": "Internal server error"},
    },
)
def get_all_parents(request: ItemIdRequest) -> TreeStoreResponse:
    """Get all parents of an item up to root.

    Args:
        request: ItemIdRequest with item ID.

    Returns:
        TreeStoreResponse with parent items (empty list if item is root).

    Raises:
        HTTPException: If operation fails (500).
    """
    logger.debug("Getting all parents", extra={"item_id": request.id})
    try:
        result = _tree_service.get_all_parents(request.id)
        logger.debug("Parents retrieved", extra={"item_id": request.id, "count": len(result)})
        return TreeStoreResponse(result=result)
    except Exception as e:
        logger.error("Failed to get all parents", extra={"item_id": request.id, "error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get all parents",
        ) from e


@app.get(
    "/api/v1/health",
    tags=["Health"],
    summary="Health check",
    description="Check service health and availability",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "ok"}
                }
            },
        },
        503: {"description": "Service unavailable"},
    },
)
def health() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        Status dictionary indicating service health.

    Raises:
        HTTPException: If health check fails (503).
    """
    logger.debug("Health check requested")
    try:
        _tree_service.get_all_items()
        logger.debug("Health check passed")
        return {"status": "ok"}
    except Exception as e:
        logger.error("Health check failed", extra={"error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable",
        ) from e

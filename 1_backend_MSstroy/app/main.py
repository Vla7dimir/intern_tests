from typing import Dict, List

from fastapi import FastAPI, HTTPException, status

from app.models import ROOT_PARENT, TreeStore
from app.schemas import ItemIdRequest, TreeStoreResponse, TreeStoreRequest

app = FastAPI(title="TreeStore API", version="1.0.0")

DEFAULT_ITEMS: List[Dict[str, object]] = [
    {"id": 1, "parent": ROOT_PARENT},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None},
]

_tree_store = TreeStore(DEFAULT_ITEMS)


def _get_tree_store() -> TreeStore:
    """Get the current tree store instance."""
    return _tree_store


def _set_tree_store(store: TreeStore) -> None:
    """Set the tree store instance."""
    global _tree_store  # noqa: WPS420
    _tree_store = store


@app.post("/api/v1/tree/init", response_model=TreeStoreResponse)
def init_tree(request: TreeStoreRequest) -> TreeStoreResponse:
    """Initialize tree with new items.

    Args:
        request: TreeStoreRequest with items to initialize.

    Returns:
        TreeStoreResponse with initialization status.
    """
    new_store = TreeStore(request.items)
    _set_tree_store(new_store)
    return TreeStoreResponse(
        result={"status": "initialized", "items_count": len(request.items)},
    )


@app.get("/api/v1/tree/getAll", response_model=TreeStoreResponse)
def get_all() -> TreeStoreResponse:
    """Get all items from the tree.

    Returns:
        TreeStoreResponse with all items.
    """
    result = _get_tree_store().get_all()
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getItem", response_model=TreeStoreResponse)
def get_item(request: ItemIdRequest) -> TreeStoreResponse:
    """Get item by ID.

    Args:
        request: ItemIdRequest with item ID.

    Returns:
        TreeStoreResponse with item data.

    Raises:
        HTTPException: If item not found.
    """
    result = _get_tree_store().get_item(request.id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getChildren", response_model=TreeStoreResponse)
def get_children(request: ItemIdRequest) -> TreeStoreResponse:
    """Get children of an item.

    Args:
        request: ItemIdRequest with parent item ID.

    Returns:
        TreeStoreResponse with children items.
    """
    result = _get_tree_store().get_children(request.id)
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getAllParents", response_model=TreeStoreResponse)
def get_all_parents(request: ItemIdRequest) -> TreeStoreResponse:
    """Get all parents of an item up to root.

    Args:
        request: ItemIdRequest with item ID.

    Returns:
        TreeStoreResponse with parent items.
    """
    result = _get_tree_store().get_all_parents(request.id)
    return TreeStoreResponse(result=result)


@app.get("/api/v1/health")
def health() -> Dict[str, str]:
    """Health check endpoint.

    Returns:
        Status dictionary.
    """
    return {"status": "ok"}

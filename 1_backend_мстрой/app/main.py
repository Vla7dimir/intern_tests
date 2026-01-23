"""Main FastAPI application."""

from typing import Any

from fastapi import FastAPI, HTTPException, status

from app.config import config
from app.models import TreeStore
from app.schemas import ItemIdRequest, TreeStoreRequest, TreeStoreResponse

app = FastAPI(title="TreeStore API", version="1.0.0")

# Default items
default_items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None},
]

tree_store = TreeStore(default_items)


@app.post("/api/v1/tree/init", response_model=TreeStoreResponse)
def init_tree(request: TreeStoreRequest):
    """Initialize tree with new items."""
    global tree_store
    tree_store = TreeStore(request.items)
    return TreeStoreResponse(
        result={"status": "initialized", "items_count": len(request.items)}
    )


@app.get("/api/v1/tree/getAll", response_model=TreeStoreResponse)
def get_all():
    """Get all items."""
    result = tree_store.getAll()
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getItem", response_model=TreeStoreResponse)
def get_item(request: ItemIdRequest):
    """Get item by id."""
    result = tree_store.getItem(request.id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getChildren", response_model=TreeStoreResponse)
def get_children(request: ItemIdRequest):
    """Get children of item by id."""
    result = tree_store.getChildren(request.id)
    return TreeStoreResponse(result=result)


@app.post("/api/v1/tree/getAllParents", response_model=TreeStoreResponse)
def get_all_parents(request: ItemIdRequest):
    """Get all parents chain."""
    result = tree_store.getAllParents(request.id)
    return TreeStoreResponse(result=result)


@app.get("/api/v1/health")
def health():
    """Health check."""
    return {"status": "ok"}

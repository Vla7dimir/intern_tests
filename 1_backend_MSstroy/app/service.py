"""Business logic layer for TreeStore operations."""

from typing import Dict, List

from app.exceptions import ItemNotFoundError
from app.logger import get_logger
from app.models import TreeStore

logger = get_logger(__name__)


class TreeStoreService:
    """Service for TreeStore business logic."""

    def __init__(self, tree_store: TreeStore) -> None:
        """Initialize service with TreeStore instance.

        Args:
            tree_store: TreeStore instance to operate on.
        """
        self._tree_store = tree_store

    def initialize_tree(self, items: List[Dict[str, object]]) -> Dict[str, object]:
        """Initialize tree with new items.

        Args:
            items: List of items to initialize tree with.

        Returns:
            Dictionary with initialization status and items count.

        Raises:
            ValueError: If items structure is invalid.
        """
        logger.debug("Initializing tree", extra={"items_count": len(items)})
        self._tree_store = TreeStore(items)
        logger.info("Tree initialized", extra={"items_count": len(items)})
        return {"status": "initialized", "items_count": len(items)}

    def get_all_items(self) -> List[Dict[str, object]]:
        """Get all items from the tree.

        Returns:
            List of all items in the tree.
        """
        return self._tree_store.get_all()

    def get_item_by_id(self, item_id: int) -> Dict[str, object]:
        """Get item by ID.

        Args:
            item_id: ID of the item to retrieve.

        Returns:
            Item dictionary.

        Raises:
            ItemNotFoundError: If item with given ID not found.
        """
        result = self._tree_store.get_item(item_id)
        if result is None:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        return result

    def get_children(self, item_id: int) -> List[Dict[str, object]]:
        """Get all children of an item.

        Args:
            item_id: ID of the parent item.

        Returns:
            List of child items.
        """
        return self._tree_store.get_children(item_id)

    def get_all_parents(self, item_id: int) -> List[Dict[str, object]]:
        """Get all parent items up to root.

        Args:
            item_id: ID of the item to get parents for.

        Returns:
            List of parent items from direct parent to root.
        """
        return self._tree_store.get_all_parents(item_id)

    @property
    def tree_store(self) -> TreeStore:
        """Get current TreeStore instance."""
        return self._tree_store

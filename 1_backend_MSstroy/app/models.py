from typing import Dict, List, Optional

ROOT_PARENT = "root"
ROOT_ITEM_ID = 1


class TreeStore:
    """Tree structure storage with parent-child relationships."""

    def __init__(self, items: List[Dict[str, object]]) -> None:
        """Initialize TreeStore with items.

        Args:
            items: List of dictionaries with 'id' and 'parent' keys.

        Raises:
            ValueError: If items contain duplicate IDs or invalid structure.
        """
        self._items = items
        self._items_by_id: Dict[int, Dict[str, object]] = {}
        self._children_by_id: Dict[int, List[Dict[str, object]]] = {}
        self._parent_map: Dict[int, Optional[int]] = {}

        seen_ids = set()
        for item in items:
            item_id = item.get("id")
            if item_id is None:
                raise ValueError("Item must have 'id' field")
            if not isinstance(item_id, int):
                raise ValueError(f"Item ID must be integer, got {type(item_id)}")
            if item_id in seen_ids:
                raise ValueError(f"Duplicate item ID: {item_id}")
            seen_ids.add(item_id)

            self._items_by_id[item_id] = item

            parent = item.get("parent")
            if parent != ROOT_PARENT:
                if parent is not None and not isinstance(parent, int):
                    raise ValueError(f"Parent must be integer or 'root', got {type(parent)}")
                self._parent_map[item_id] = parent
                if parent not in self._children_by_id:
                    self._children_by_id[parent] = []
                self._children_by_id[parent].append(item)
            else:
                self._parent_map[item_id] = None

    def get_all(self) -> List[Dict[str, object]]:
        """Get all items in the store.

        Returns:
            List of all items.
        """
        return self._items

    def get_item(self, item_id: int) -> Optional[Dict[str, object]]:
        """Get item by ID.

        Args:
            item_id: ID of the item to retrieve.

        Returns:
            Item dictionary or None if not found.
        """
        return self._items_by_id.get(item_id)

    def get_children(self, item_id: int) -> List[Dict[str, object]]:
        """Get all children of an item.

        Args:
            item_id: ID of the parent item.

        Returns:
            List of child items.
        """
        return self._children_by_id.get(item_id, [])

    def _get_parent_id(self, item_id: int) -> Optional[int]:
        """Get parent ID for given item.

        Args:
            item_id: ID of the item.

        Returns:
            Parent ID or None if root item.
        """
        return self._parent_map.get(item_id)

    def _is_root_item(self, item_id: int) -> bool:
        """Check if item is root.

        Args:
            item_id: ID of the item to check.

        Returns:
            True if item is root, False otherwise.
        """
        parent = self._get_parent_id(item_id)
        return parent is None

    def _get_root_item(self) -> Optional[Dict[str, object]]:
        """Get root item.

        Returns:
            Root item dictionary or None if not found.
        """
        return self._items_by_id.get(ROOT_ITEM_ID)

    def get_all_parents(self, item_id: int) -> List[Dict[str, object]]:
        """Get all parent items up to the root.

        Args:
            item_id: ID of the item to get parents for.

        Returns:
            List of parent items from direct parent to root.
        """
        result = []
        current_id = item_id

        while current_id is not None:
            item = self._items_by_id.get(current_id)
            if item is None:
                break

            if current_id != item_id:
                result.append(item)

            parent = self._get_parent_id(current_id)
            if parent is None:
                root_item = self._get_root_item()
                if root_item:
                    result.append(root_item)
                break
            current_id = parent

        return result

from typing import Dict, List, Optional

ROOT_PARENT = "root"
ROOT_ITEM_ID = 1


class TreeStore:
    """Tree structure storage with parent-child relationships."""

    def __init__(self, items: List[Dict[str, object]]) -> None:
        """Initialize TreeStore with items.

        Args:
            items: List of dictionaries with 'id' and 'parent' keys.
        """
        self._items = items
        self._items_by_id: Dict[int, Dict[str, object]] = {}
        self._children_by_id: Dict[int, List[Dict[str, object]]] = {}
        self._parent_map: Dict[int, Optional[int]] = {}

        for item in items:
            item_id = item["id"]
            self._items_by_id[item_id] = item

            parent = item.get("parent")
            if parent != ROOT_PARENT:
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

            parent = self._parent_map.get(current_id)
            if parent is None:
                root_item = self._items_by_id.get(ROOT_ITEM_ID)
                if root_item:
                    result.append(root_item)
                break
            current_id = parent

        return result

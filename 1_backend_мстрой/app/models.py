"""TreeStore model for working with tree structures."""

from typing import Any, Dict, List


class TreeStore:
    """Fast tree structure with O(1) access to elements."""

    def __init__(self, items: List[Dict[str, Any]]):
        """Initialize TreeStore with items."""
        self._items = items
        self._items_by_id: Dict[Any, Dict[str, Any]] = {}
        self._children_by_id: Dict[Any, List[Dict[str, Any]]] = {}
        self._parent_map: Dict[Any, Any] = {}

        for item in items:
            item_id = item["id"]
            self._items_by_id[item_id] = item

            parent = item.get("parent")
            if parent != "root":
                self._parent_map[item_id] = parent
                if parent not in self._children_by_id:
                    self._children_by_id[parent] = []
                self._children_by_id[parent].append(item)
            else:
                self._parent_map[item_id] = None

    def getAll(self) -> List[Dict[str, Any]]:
        """Return all items."""
        return self._items

    def getItem(self, id: Any) -> Dict[str, Any] | None:
        """Get item by id (O(1))."""
        return self._items_by_id.get(id)

    def getChildren(self, id: Any) -> List[Dict[str, Any]]:
        """Get children of item by id (O(1))."""
        return self._children_by_id.get(id, [])

    def getAllParents(self, id: Any) -> List[Dict[str, Any]]:
        """Get all parents chain from item to root."""
        result = []
        current_id = id

        while current_id is not None:
            item = self._items_by_id.get(current_id)
            if item is None:
                break

            if current_id != id:
                result.append(item)

            parent = self._parent_map.get(current_id)
            if parent == "root":
                root_item = self._items_by_id.get(1)
                if root_item:
                    result.append(root_item)
                break
            current_id = parent

        return result

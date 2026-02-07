from typing import Dict, List

from app.models import ROOT_PARENT, TreeStore

ITEMS: List[Dict[str, object]] = [
    {"id": 1, "parent": ROOT_PARENT},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None},
]

tree_store = TreeStore(ITEMS)

if __name__ == "__main__":
    print("get_all():")
    print(tree_store.get_all())
    print()

    print("get_item(7):")
    print(tree_store.get_item(7))
    print()

    print("get_children(4):")
    print(tree_store.get_children(4))
    print()

    print("get_children(5):")
    print(tree_store.get_children(5))
    print()

    print("get_all_parents(7):")
    print(tree_store.get_all_parents(7))

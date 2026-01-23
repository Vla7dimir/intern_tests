"""Example usage of TreeStore."""

from app.models import TreeStore

items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None},
]

ts = TreeStore(items)

if __name__ == "__main__":
    print("getAll():")
    print(ts.getAll())
    print()

    print("getItem(7):")
    print(ts.getItem(7))
    print()

    print("getChildren(4):")
    print(ts.getChildren(4))
    print()

    print("getChildren(5):")
    print(ts.getChildren(5))
    print()

    print("getAllParents(7):")
    print(ts.getAllParents(7))

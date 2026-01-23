import pytest

from app.models import TreeStore


@pytest.fixture
def sample_items():
    return [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]


@pytest.fixture
def tree_store(sample_items):
    return TreeStore(sample_items)


def test_getAll(tree_store, sample_items):
    result = tree_store.getAll()
    assert result == sample_items
    assert len(result) == 8


def test_getItem(tree_store):
    result = tree_store.getItem(7)
    assert result == {"id": 7, "parent": 4, "type": None}

    result = tree_store.getItem(1)
    assert result == {"id": 1, "parent": "root"}

    result = tree_store.getItem(999)
    assert result is None


def test_getChildren(tree_store):
    result = tree_store.getChildren(4)
    assert len(result) == 2
    assert {"id": 7, "parent": 4, "type": None} in result
    assert {"id": 8, "parent": 4, "type": None} in result

    result = tree_store.getChildren(5)
    assert result == []

    result = tree_store.getChildren(2)
    assert len(result) == 3
    assert {"id": 4, "parent": 2, "type": "test"} in result
    assert {"id": 5, "parent": 2, "type": "test"} in result
    assert {"id": 6, "parent": 2, "type": "test"} in result


def test_getAllParents(tree_store):
    result = tree_store.getAllParents(7)
    assert len(result) == 3
    assert result[0] == {"id": 4, "parent": 2, "type": "test"}
    assert result[1] == {"id": 2, "parent": 1, "type": "test"}
    assert result[2] == {"id": 1, "parent": "root"}

    result = tree_store.getAllParents(1)
    assert result == []

    result = tree_store.getAllParents(4)
    assert len(result) == 2
    assert result[0] == {"id": 2, "parent": 1, "type": "test"}
    assert result[1] == {"id": 1, "parent": "root"}


def test_performance(tree_store):
    for _ in range(1000):
        tree_store.getItem(7)
        tree_store.getChildren(2)
        tree_store.getAllParents(7)

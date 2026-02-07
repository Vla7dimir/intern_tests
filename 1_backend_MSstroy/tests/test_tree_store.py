import pytest

from app.models import ROOT_PARENT, TreeStore


@pytest.fixture
def sample_items():
    """Fixture providing sample items for testing."""
    return [
        {"id": 1, "parent": ROOT_PARENT},
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
    """Fixture providing TreeStore instance for testing."""
    return TreeStore(sample_items)


def test_get_all(tree_store, sample_items):
    """Test get_all method."""
    result = tree_store.get_all()
    assert result == sample_items
    assert len(result) == 8


def test_get_item(tree_store):
    """Test get_item method."""
    result = tree_store.get_item(7)
    assert result == {"id": 7, "parent": 4, "type": None}

    result = tree_store.get_item(1)
    assert result == {"id": 1, "parent": ROOT_PARENT}

    result = tree_store.get_item(999)
    assert result is None


def test_get_children(tree_store):
    """Test get_children method."""
    result = tree_store.get_children(4)
    assert len(result) == 2
    assert {"id": 7, "parent": 4, "type": None} in result
    assert {"id": 8, "parent": 4, "type": None} in result

    result = tree_store.get_children(5)
    assert result == []

    result = tree_store.get_children(2)
    assert len(result) == 3
    assert {"id": 4, "parent": 2, "type": "test"} in result
    assert {"id": 5, "parent": 2, "type": "test"} in result
    assert {"id": 6, "parent": 2, "type": "test"} in result


def test_get_all_parents(tree_store):
    """Test get_all_parents method."""
    result = tree_store.get_all_parents(7)
    assert len(result) == 3
    assert result[0] == {"id": 4, "parent": 2, "type": "test"}
    assert result[1] == {"id": 2, "parent": 1, "type": "test"}
    assert result[2] == {"id": 1, "parent": ROOT_PARENT}

    result = tree_store.get_all_parents(1)
    assert result == []

    result = tree_store.get_all_parents(4)
    assert len(result) == 2
    assert result[0] == {"id": 2, "parent": 1, "type": "test"}
    assert result[1] == {"id": 1, "parent": ROOT_PARENT}


def test_performance(tree_store):
    """Test performance of tree operations."""
    for _ in range(1000):
        tree_store.get_item(7)
        tree_store.get_children(2)
        tree_store.get_all_parents(7)

"""Configuration for all tests."""

from typing import Any, Dict

import pytest

from pixelize import __author__


@pytest.fixture(autouse=True)
def _add_author(doctest_namespace: Dict[str, Any]) -> None:
    """Update doctest namespace."""
    doctest_namespace["author"] = __author__

"""Configuration for all tests."""

from pathlib import Path
from typing import Any, Dict

import pytest


@pytest.fixture()
def resources() -> Path:
    """Resolve path to test resources."""
    return Path(__file__).parent / "tests" / "resources"


@pytest.fixture(autouse=True)
def _configure_doctest(
    doctest_namespace: Dict[str, Any],
    resources: Path,
) -> None:
    """Update doctest namespace."""
    doctest_namespace["resources"] = resources

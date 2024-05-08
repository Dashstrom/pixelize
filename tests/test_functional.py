"""Module for perform functional test."""

import platform
from pathlib import Path

import pytest

from pixelize import pixelize


def test_functional(resources: Path) -> None:
    """Run test for check if file is generated at end."""
    pixelize(image=resources / "cat.bmp", height=32, border=True)


@pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="does not run on macos",
)
def test_functional_rembg(resources: Path) -> None:
    """Run test for check if rembg can be used."""
    pixelize(image=resources / "cat.bmp", height=32, border=True, rembg=True)

"""Module for perform functional test."""

from pathlib import Path

from pixelize import pixelize


def test_functional(resources: Path) -> None:
    """Run test for check if file is generated at end."""
    pixelize(image=resources / "cat.bmp", height=32, border=True, rembg=True)

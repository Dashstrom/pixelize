"""Main module."""

from .cli import entrypoint
from .core import (
    __author__,
    __email__,
    __license__,
    __maintainer__,
    __summary__,
    __version__,
)
from .pixelize import pixelize

__all__ = [
    "entrypoint",
    "__author__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__summary__",
    "__version__",
    "pixelize",
]

"""Core module."""

from importlib.metadata import Distribution

_DISTRIBUTION = Distribution.from_name(
    "pixelize",
)
_METADATA = _DISTRIBUTION.metadata

__author__ = _METADATA["Author"]
__license__ = _METADATA["License"]
__version__ = _METADATA["Version"]
__maintainer__ = _METADATA["Maintainer-email"]
__email__ = _METADATA["Maintainer"]
__summary__ = _METADATA["Summary"]
__issues__ = "https://github.com/Dashstrom/pixelize/issues"

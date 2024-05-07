"""Utils module."""

import re
from typing import Tuple

RE_BOX = re.compile(r"(\d+)x(\d+)\+(\d+)x(\d+)")

Box = Tuple[int, int, int, int]


def parse_box(box: str) -> Box:
    """Parse box as 100x100+150x150.

    Args:
        box: Text to parse on format like 100x100+150x150.

    Returns:
        A string with Hello + text.

    Raises:
        ValueError: If box is invalid.

    Examples:
        >>> parse_box("100x100+150x150")
        (100, 100, 150, 150)
        >>> parse_box("-100x100+150x150")
        Traceback (most recent call last):
        ValueError: Invalid box: "-100x100+150x150"
    """
    match = RE_BOX.fullmatch(box)
    if match is None:
        error_message = f"Invalid box: {box!r}"
        raise ValueError(error_message)
    return tuple(int(value) for value in match.groups())  # type: ignore[return-value]

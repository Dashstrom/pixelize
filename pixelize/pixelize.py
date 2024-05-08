"""Module for pixelize images."""

import pathlib
from pathlib import Path, PurePath
from typing import IO, Optional, Union

import numpy as np
import numpy.typing as npt
from PIL import Image

from pixelize.utils import Box

BLACK = np.array((0, 0, 0, 255))
TRANSPARENT = np.array((0, 0, 0, 0))
COLOR_REDUCTION = 5
DEFAULT_SIZE = 32
DEFAULT_SCALE = 2
ALPHA_MIN = 190
ALPHA_MAX = 190

BufferOrPath = Union[str, pathlib.PurePath, IO[bytes]]


def pixelize(  # noqa: C901, PLR0912, PLR0913, PLR0915
    image: Union[Image.Image, BufferOrPath],
    *,
    output: Optional[BufferOrPath] = None,
    rembg: Optional[bool] = None,
    inner: Optional[bool] = None,
    color_reduction: Optional[int] = None,
    alpha_min: Optional[int] = None,
    alpha_max: Optional[int] = None,
    margin: Optional[int] = None,
    border: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: Optional[int] = None,
    crop: Optional[Box] = None,
) -> Image.Image:
    """Turn Image into pixel art."""
    if not isinstance(image, Image.Image):
        image = Image.open(image)  # type: ignore[arg-type]
    frame: npt.NDArray[np.uint8] = np.array(image.convert("RGBA"))

    # Recompute variables
    if margin is None:
        margin = 0
    if border:
        margin += 1
    if scale is None:
        scale = DEFAULT_SCALE
    if color_reduction is None:
        color_reduction = COLOR_REDUCTION
    if alpha_min is None:
        alpha_min = ALPHA_MIN
    if alpha_max is None:
        alpha_max = ALPHA_MAX

    # Optional remove of background
    if rembg:
        from rembg import remove

        frame = remove(
            frame,
            post_process_mask=True,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=20,
            alpha_matting_erode_size=60,
        ).copy()

    # Remove alpha pixel
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b, a = frame[y, x, :].astype(int)
            if a < alpha_min:
                frame[y, x] = TRANSPARENT
            if a >= alpha_max:
                frame[y, x, 3] = 255

    # Load array as image
    im = Image.fromarray(frame)

    # Optional remove of image
    if inner:
        im = im.crop(im.getbbox())
    iw, ih = im.size
    if width is None:
        if height is None:
            w, h = 32, 32
        else:
            w, h = int(height * (iw / ih)), height
    elif height is None:
        w, h = width, int(width * (ih / iw))
    else:
        w, h = width, height
    w2 = w - (margin << 1)
    h2 = h - (margin << 1)

    # Resize image to requested size
    base_im = im.resize((w2, h2), Image.Resampling.NEAREST)

    # Paste in in blank image
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    im.paste(base_im, ((w - w2) // 2, (h - h2) // 2))

    frame = np.array(im)

    # Color reductions
    if color_reduction > 0:
        factor_reduction = 1 << color_reduction
        frame[:, :, :3] = (
            frame[:, :, :3] // factor_reduction * factor_reduction
        ).astype(np.uint8)

    # Preprocessing
    for y in range(h):
        for x in range(w):
            r, g, b, a = frame[y, x, :].astype(int)
            # Makes transparent pixels that are almost transparent
            if a < 64:  # noqa: PLR2004
                frame[y, x] = TRANSPARENT
            # Turn gray pixel into black one
            elif (
                border
                and abs(r - g) + abs(g - b) + abs(b - r) < 64  # noqa: PLR2004
                and np.linalg.norm(BLACK[:3] - frame[y, x, :3]) < 64  # noqa: PLR2004
            ):
                frame[y, x] = BLACK
            # Remove the transparency of pixels that have a little
            if a >= ALPHA_MAX:
                frame[y, x, 3] = 255

    if border:
        # Add black border
        for y in range(h):
            for x in range(w):
                pix = frame[y, x, :]
                if pix[3] == 0 and (
                    (
                        x + 1 < w
                        and frame[y, x + 1, 3] != 0
                        and np.any(frame[y, x + 1] != BLACK)
                    )
                    or (
                        x - 1 >= 0
                        and frame[y, x - 1, 3] != 0
                        and np.any(frame[y, x - 1] != BLACK)
                    )
                    or (
                        y + 1 < h
                        and frame[y + 1, x, 3] != 0
                        and np.any(frame[y + 1, x] != BLACK)
                    )
                    or (
                        y - 1 >= 0
                        and frame[y - 1, x, 3] != 0
                        and np.any(frame[y - 1, x] != BLACK)
                    )
                ):
                    frame[y, x, :] = BLACK

    # Scale the pixels
    im = Image.fromarray(frame)
    im = im.resize(
        (int(w * scale), int(h * scale)),
        Image.Resampling.NEAREST,
    )
    if crop is not None:
        im = im.crop(crop)
    im = im.convert("P", palette=Image.ADAPTIVE, colors=256)
    if output is not None:
        if isinstance(output, (PurePath, str)):
            path = Path(output)
            path.parent.mkdir(parents=True, exist_ok=True)
            im.save(path, optimize=True)
        else:
            im.save(output, optimize=True)
    return im

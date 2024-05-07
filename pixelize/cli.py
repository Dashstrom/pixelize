"""Module for command line interface."""

import argparse
import logging
import sys
from pathlib import Path
from typing import NoReturn, Optional, Sequence

from pixelize.core import __issues__, __summary__, __version__
from pixelize.pixelize import pixelize
from pixelize.utils import parse_box

LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
logger = logging.getLogger(__name__)


class HelpArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        """Handle error from argparse.ArgumentParser."""
        self.print_help(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def get_parser() -> argparse.ArgumentParser:
    """Prepare ArgumentParser."""
    parser = HelpArgumentParser(
        prog="pixelize",
        description=__summary__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s, version {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="verbose mode, enable INFO and DEBUG messages.",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="File or directory to pixelize",
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="Output dir.",
        required=False,
        default="pixelized",
    )
    parser.add_argument("--width", type=int, help="Width.", required=False)
    parser.add_argument("--height", type=int, help="Height.", required=False)
    parser.add_argument(
        "-s", "--scale", type=int, help="Scale.", required=False
    )
    parser.add_argument(
        "-c", "--crop", type=str, help="Crop the final image.", required=False
    )
    parser.add_argument(
        "--color-reduction",
        type=int,
        help="Reduce color in image.",
        required=False,
    )
    parser.add_argument(
        "--rembg",
        action="store_true",
        help="Remove background.",
    )
    parser.add_argument(
        "--inner",
        action="store_true",
        help="Inner.",
    )
    parser.add_argument(
        "--border",
        action="store_true",
        help="Border.",
    )
    parser.add_argument(
        "--alpha-min",
        type=int,
        help="Minimal alpha pixel before being erased",
        required=False,
    )
    parser.add_argument(
        "--alpha-max",
        type=int,
        help="Maximal alpha pixel before being opaque",
        required=False,
    )
    parser.add_argument(
        "--margin", type=int, help="Margin border.", required=False
    )
    return parser


def setup_logging(verbose: Optional[bool] = None) -> None:
    """Do setup logging."""
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    )


def entrypoint(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for command line interface."""
    try:
        parser = get_parser()
        args = parser.parse_args(argv)
        setup_logging(args.verbose)
        for file in args.input:
            path = Path(file)
            new_name = path.with_suffix(".pix.png")
            output = Path(args.output_dir) / new_name.name
            pixelize(
                image=path,
                output=output,
                inner=args.inner,
                color_reduction=args.color_reduction,
                alpha_min=args.alpha_min,
                alpha_max=args.alpha_max,
                margin=args.margin,
                border=args.border,
                width=args.width,
                height=args.height,
                scale=args.scale,
                crop=parse_box(args.crop) if args.crop else None,
            )
    except Exception as err:  # NoQA: BLE001
        logger.critical("Unexpected error", exc_info=err)
        logger.critical("Please, report this error to %s.", __issues__)
        sys.exit(1)

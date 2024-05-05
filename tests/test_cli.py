"""Test for command line interface."""

import contextlib
import io
import os
import subprocess
import sys

import pytest

from pixelize import entrypoint


def test_cli_version() -> None:
    """Test if the command line interface is installed correctly."""
    name = "pixelize"
    env = os.environ.get("VIRTUAL_ENV", "")
    if env:
        if os.name == "nt":
            exe = f"{env}\\\\Scripts\\\\{name}.cmd"
            if not os.path.exists(exe):  # noqa: PTH110
                exe = f"{env}\\\\Scripts\\\\{name}.exe"
        else:
            exe = f"{env}/bin/{name}"
    else:
        exe = name
    out = subprocess.check_output((exe, "--version"), text=True, shell=False)
    assert "version" in out
    out = subprocess.check_output(
        (
            sys.executable,
            "-m",
            "pixelize",
            "--version",
        ),
        text=True,
        shell=False,
    )
    assert "version" in out
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout), pytest.raises(SystemExit):
        entrypoint(("--version",))
    assert "version" in stdout.getvalue()


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import pixelize.__main__  # NoQA: F401


def test_hello() -> None:
    """Test command hello."""
    name = "A super secret name"
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        entrypoint(("hello", "--name", name))
    assert name in stdout.getvalue()

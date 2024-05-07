.. role:: bash(code)
  :language: bash

********
Pixelize
********

.. image:: https://github.com/Dashstrom/pixelize/actions/workflows/docs.yml/badge.svg
  :target: https://github.com/Dashstrom/pixelize/actions/workflows/docs.yml
  :alt: CI : Docs

.. image:: https://github.com/Dashstrom/pixelize/actions/workflows/lint.yml/badge.svg
  :target: https://github.com/Dashstrom/pixelize/actions/workflows/lint.yml
  :alt: CI : Lint

.. image:: https://github.com/Dashstrom/pixelize/actions/workflows/tests.yml/badge.svg
  :target: https://github.com/Dashstrom/pixelize/actions/workflows/tests.yml
  :alt: CI : Tests

.. image:: https://img.shields.io/pypi/v/pixelize.svg
  :target: https://pypi.org/project/pixelize
  :alt: PyPI : pixelize

.. image:: https://img.shields.io/pypi/pyversions/pixelize.svg
  :target: https://pypi.org/project/pixelize
  :alt: Python : versions

.. image:: https://img.shields.io/badge/Discord-Pixelize-5865F2?style=flat&logo=discord&logoColor=white
  :target: https://dsc.gg/dashstrom
  :alt: Discord

.. image:: https://img.shields.io/badge/license-MIT-green.svg
  :target: https://github.com/Dashstrom/pixelize/blob/main/LICENSE
  :alt: License : MIT

Description
###########

Turn images into pixel arts.

Installation
############

You can install :bash:`pixelize` via `pip <https://pypi.org/project/pip/>`_
from `PyPI <https://pypi.org/project>`_

..  code-block:: bash

  pip install pipx
  pipx ensurepath
  pipx install pixelize

You can also install gpu support for rembg dependency using:

..  code-block:: bash

  pipx inject pixelize rembg[gpu]

Usage
#####

..  code-block:: bash

  pixelize --version
  pixelize --help

..  code-block:: bash

  pixelize \
    -i ./docs/examples/car.jpg \
    --height 128 \
    --crop 0x80+136x216 \
    --scale 2 \
    --color-reduction 4 \
    --output-dir ./docs/examples/pixelized

..  code-block:: bash

  pixelize \
    -i ./docs/examples/cat.bmp \
    --height 32 \
    --border \
    --output-dir ./docs/examples/pixelized

Development
###########

Contributing
************

Contributions are very welcome. Tests can be run with :bash:`poe check`, please
ensure the coverage at least stays the same before you submit a pull request.

Setup
*****

You need to install `Poetry <https://python-poetry.org/docs/#installation>`_
and `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
for work with this project.

..  code-block:: bash

  git clone https://github.com/Dashstrom/pixelize
  cd pixelize
  poetry install --all-extras
  poetry run poe setup
  poetry shell

Poe
********

Poe is available for help you to run tasks.

..  code-block:: text

  test           Run test suite.
  lint           Run linters : ruff linter, ruff formatter and mypy.
  format         Run linters in fix mode.
  check          Run all checks : lint, test and docs.
  cov            Run coverage for generate report and html.
  open-cov       Open html coverage report in webbrowser.
  docs           Build documentation.
  open-docs      Open documentation in webbrowser.
  setup          Setup pre-commit.
  pre-commit     Run pre-commit.
  clean          Clean cache files

Skip commit verification
************************

If the linting is not successful, you can't commit.
For forcing the commit you can use the next command :

..  code-block:: bash

  git commit --no-verify -m 'MESSAGE'

Commit with commitizen
**********************

To respect commit conventions, this repository uses
`Commitizen <https://github.com/commitizen-tools/commitizen?tab=readme-ov-file>`_.

..  code-block:: bash

  cz commit

How to add dependency
*********************

..  code-block:: bash

  poetry add 'PACKAGE'

Ignore illegitimate warnings
****************************

To ignore illegitimate warnings you can add :

- **# noqa: ERROR_CODE** on the same line for ruff.
- **# type: ignore[ERROR_CODE]** on the same line for mypy.
- **# pragma: no cover** on the same line to ignore line for coverage.
- **# doctest: +SKIP** on the same line for doctest.

Uninstall
#########

..  code-block:: bash

  pip uninstall pixelize

License
#######

This work is licensed under `MIT <https://github.com/Dashstrom/pixelize/-/raw/main/LICENSE>`_.

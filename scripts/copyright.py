#!/usr/bin/python3
# Copyright 2023 Krzysztof Wiśniewski <argmaster.world@gmail.com>
#
# This file is part of MSTS.
#
#
# MSTS is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# MSTS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MSTS. If not, see <http://www.gnu.org/licenses/>.


"""Script for fixing missing copyright notices in project files."""

from __future__ import annotations

import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import lru_cache
from itertools import repeat
from pathlib import Path
from typing import Iterable, Optional

SCRIPTS_DIR: Path = Path(__file__).parent


try:
    import click
    import jellyfish
    import jinja2
    import tomlkit

except ImportError as __exc:
    print(
        f"Dependencies are missing ({__exc}), make sure you are running in virtual "
        + "environment!"
    )
    print("poetry shell")
    print("poetry install")
    raise SystemExit(1) from __exc


@click.command()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help=(
        "Changes verbosity, when not used, verbosity is  warning, with every `v` "
        + "verbosity goes utp, `-vv` means debug."
    ),
)
@click.option("-s", "--comment-symbol", help="Symbol used to indicate comment.")
@click.option(
    "-d", "--directory", help="Path to directory to search.", type=Path, multiple=True
)
@click.option(
    "-g", "--glob", help="File glob used to search directories.", multiple=True
)
@click.option(
    "-a",
    "--author",
    type=int,
    help=(
        "Index of author from authors list in pyproject.toml which should be used. "
        + "By default its first one."
    ),
    default=0,
)
@click.option(
    "-l",
    "--license",
    "license_",
    help="Name of license file to use.",
    default="LGPL3.md.jinja2",
)
@click.option(
    "-p",
    "--pool",
    help="Size of thread pool used for file IO.",
    default=4,
    type=int,
)
def main(  # pylint: disable=too-many-arguments
    verbose: int,
    comment_symbol: str,
    directory: list[Path],
    glob: list[str],
    author: int,
    license_: str,
    pool: int,
) -> int:  # pylint: enable=too-many-arguments
    """Add Copyright notices to all files selected by given glob in specified
    directories.

    Use -d/--directory and -g/--glob multiple times to specify more directories and
    globs to use at once.
    """
    configure_logging(verbose)

    note = render_note(comment_symbol, author, license_)
    logging.debug("Rendered copyright note, %r characters.", len(note))

    def _() -> Iterable[Path]:
        for dir_path in directory:
            dir_path = dir_path.resolve()

            for file_glob in glob:
                logging.debug("Walking %r", (dir_path / file_glob).as_posix())

                for file_path in dir_path.rglob(file_glob):
                    yield file_path

    with ThreadPoolExecutor(max_workers=pool) as executor:
        executor.map(handle_file, _(), repeat(note))

    return 1


def configure_logging(verbose: int) -> None:
    """Configure default logger."""
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    if verbose == 0:
        root_logger.setLevel(logging.WARNING)
    elif verbose == 1:
        root_logger.setLevel(logging.INFO)
    else:
        root_logger.setLevel(logging.DEBUG)

    normal_stream_handler: logging.Handler = logging.StreamHandler(stream=sys.stderr)

    normal_stream_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s [%(levelname)-5.5s] %(message)s",
            datefmt="%y.%m.%d %H:%M:%S",
        )
    )

    root_logger.addHandler(normal_stream_handler)
    logging.debug("Configured logger with level %r", verbose)


def render_note(comment_symbol: str, author_index: int, license_: str) -> str:
    """Render license note from template `LICENSE_NOTE.md.jinja2`."""
    templates_dir = SCRIPTS_DIR / "templates"
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir),
        autoescape=jinja2.select_autoescape(),
    )
    template = env.get_template(license_)
    logging.debug(
        "Loaded template object %r from %r", license_, templates_dir.as_posix()
    )

    package_name = pyproject().get("tool", {}).get("poetry", {}).get("name", "unknown")
    repository = pyproject().get("tool", {}).get("poetry", {}).get("repository", "#")
    author = (
        pyproject().get("tool", {}).get("poetry", {}).get("authors", [])[author_index]
    )
    logging.info("Using %r license for %r", license_, author)

    render = template.render(
        current_year=datetime.now().year,
        author_name=author,
        package_name=package_name,
        repository=repository,
    ).strip()

    def _() -> Iterable[str]:
        for line in render.split("\n"):
            yield f"{comment_symbol} {line}"

    return str.join("\n", _())


@lru_cache(1)
def pyproject() -> tomlkit.TOMLDocument:
    """Load `pyproject.toml` file content from current working directory."""
    pyproject_path = Path.cwd() / "pyproject.toml"
    text_content = pyproject_path.read_text()
    content = tomlkit.loads(text_content)

    logging.debug(
        "Loaded %r chars from %r.", len(text_content), pyproject_path.as_posix()
    )
    return content


def handle_file(file_path: Path, note: str) -> int:
    """Check if file needs copyright update and apply it."""
    try:
        _handle_file(file_path, note)

    except Exception as exc:
        logging.exception(exc)
        raise

    return 0


def _handle_file(file_path: Path, note: str) -> int:
    note_size = len(note)
    content = file_path.read_text()
    logging.debug("Inspecting file %r", file_path.as_posix())

    shebang: Optional[str]
    if content.startswith("#!"):
        # Remove shebang line from content and store it.
        shebang, *rest = content.split("\n")
        content = str.join("\n", rest)
    else:
        shebang = None

    file_beginning = content[:note_size]
    distance = jellyfish.levenshtein_distance(note, file_beginning)
    ratio = 1.0 - (distance / note_size)

    logging.debug("Ratio %r for %r", ratio, file_path.as_posix())

    if ratio > 0.8:
        # License was found, mostly matching, maybe author has changed or sth.
        return 0

    if shebang is None:
        new_file_content = f"{note}\n\n\n{content}"
    else:
        new_file_content = f"{shebang}\n{note}\n\n\n{content}"

    tempfile = file_path.with_suffix(".temp")
    tempfile.write_text(new_file_content)
    os.rename(tempfile, file_path)
    logging.warning("Updated %r", file_path.as_posix())

    return 1


if __name__ == "__main__":
    raise SystemExit(main())  # pylint: disable=no-value-for-parameter

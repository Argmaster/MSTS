"""Build MSTS wheel distribution."""

from __future__ import annotations

import logging
import subprocess


def run(cmd: str) -> bool:
    """Run command with subprocess, return True on failure, False on success."""
    try:
        completed_process = subprocess.run(cmd, check=True, shell=True)

        if completed_process.returncode != 0:
            return True

    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        logging.exception(exc)
        return False

    return True


def main() -> None:
    """Build MSTS wheel."""

    run("npx webpack --config webpack.config.js --mode production")
    run("poetry build --format=wheel")

    raise SystemExit(0)


if __name__ == "__main__":
    main()

# Copyright 2023 Krzysztof Wiśniewski <argmaster.world@gmail.com>
#
# This file is part of MSTS.
# https://github.com/Argmaster/MSTS
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


"""This module declares command line interface of MSTS."""

from __future__ import annotations

import click

import msts
from msts.logging.log import configure_logger


@click.group()
@click.option(
    "-v",
    "--verbose",
    default=0,
    count=True,
    help="Control verbosity of logging, by default critical only, use "
    "-v, -vv, -vvv to gradually increase it.",
)
@click.option(
    "--rich",
    "--no-rich",
    is_flag=True,
    default=True,
    help="Toggle in-console log coloring using ",
)
@click.version_option(msts.__version__, "-V", "--version", prog_name="cssfinder")
def cli(verbose: int, rich: bool) -> None:
    """Minecraft Status Tracking Server command line interface."""
    configure_logger(verbosity=verbose, logger_name="msts", use_rich=rich)

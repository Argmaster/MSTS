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


"""Entry point of Minecraft Status Tracking Server package."""


from __future__ import annotations

from msts.cli import cli
from msts.server import server

__all__ = ["server", "cli"]

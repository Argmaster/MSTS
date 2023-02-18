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


"""this module contains a variety of tools that do not fit anywhere else, but are needed
in the project."""

from __future__ import annotations

import re
from hashlib import sha1
from random import random
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from typing_extensions import Self


class HexSHA1(str):
    """Hexadecimal representation of SHA1."""

    REGEX: ClassVar[re.Pattern] = re.compile(r"^([a-fA-F0-9]){40}$")

    def __init__(self, string: str) -> None:
        if self.REGEX.match(string) is None:
            raise ValueError(f"{string!r} is not a valid hex representation of SHA1")

        super().__init__()

    @classmethod
    def random(cls, seed: Optional[float] = None) -> Self:
        """Create random SHA-128."""
        if seed is None:
            seed = random()

        algorithm = sha1(str(seed).encode("utf-8"))
        hexdigest = algorithm.hexdigest()

        return cls(hexdigest)

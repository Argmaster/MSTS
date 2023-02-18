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


"""This module contains container class holding runtime configuration of MST server."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import tomlkit
from pydantic import BaseModel, Field

from msts.utility import HexSHA1

if TYPE_CHECKING:
    from typing_extensions import Self


class Config(BaseModel):
    CONFIG_ENV_VAR_NAME: ClassVar[str] = "MSTS_CONFIG_PATH"

    java_executable: str = Field(default="java")

    class User:
        """Simplified representation of user data used in configuration file."""

        name: str = Field(default=HexSHA1.random())
        password: str = Field(default=HexSHA1.random())

    admin: User = Field(default_factory=User)

    @classmethod
    def create(cls) -> Self:
        """Factory method used to create config. It will automatically find
        configuration file if one exists, otherwise new one will be created with default
        values and ConfigNotPresent warning will be reported.

        Returns
        -------
        Self
            Instance of configuration class.
        """

        path_override = os.environ.get(cls.CONFIG_ENV_VAR_NAME)

        if path_override is not None:
            path_to_config = Path(path_override)
        else:
            path_to_config = Path.cwd() / "msts.toml"

        if path_to_config.exists():
            with path_to_config.open(encoding="utf-8") as file:
                content = tomlkit.load(file)
            config = cls(**content)

        else:
            config = cls()
            with path_to_config.open("w", encoding="utf-8") as file:
                # .dict() will not convert all fields to serializable
                content = json.loads(config.json())
                tomlkit.dump(content, file)

        return config

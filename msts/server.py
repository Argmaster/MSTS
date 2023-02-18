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


"""This module is a root of server implementation."""


from __future__ import annotations

from pathlib import Path

import jinja2
from fastapi import Depends, FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

from msts.config import Config

TEMPLATES_DIR: Path = Path(__file__).parent / "templates"
STATIC_FILES_DIR: Path = Path(__file__).parent / "static"


config = Config.create()

server = FastAPI()
environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR.as_posix()),
    autoescape=jinja2.select_autoescape(),
    enable_async=True,
)

server.mount(
    "/static", StaticFiles(directory=STATIC_FILES_DIR.as_posix()), name="static"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@server.get("/")
async def login() -> HTMLResponse:
    """Login page."""
    template = environment.get_template("login.html.jinja2")
    content = await template.render_async()

    return HTMLResponse(
        content=content,
        status_code=status.HTTP_200_OK,
    )


@server.get("/monitor/")
async def monitor(token: str = Depends(oauth2_scheme)) -> HTMLResponse:
    """Resource monitor page."""
    return HTMLResponse(content=token, status_code=status.HTTP_501_NOT_IMPLEMENTED)

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

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import jinja2
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from msts.config import Config

TEMPLATES_DIR: Path = Path(__file__).parent / "templates"
STATIC_FILES_DIR: Path = Path(__file__).parent / "static"


config = Config.create()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
server = FastAPI()

server.mount(
    "/static", StaticFiles(directory=STATIC_FILES_DIR.as_posix()), name="static"
)

environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR.as_posix()),
    autoescape=jinja2.select_autoescape(),
    enable_async=True,
)


@server.get("/")
async def login() -> HTMLResponse:
    """Login page."""
    template = environment.get_template("login.html.jinja2")
    content = await template.render_async()

    return HTMLResponse(
        content=content,
        status_code=status.HTTP_200_OK,
    )


class TokenDataIn(BaseModel):
    """Token data acquired from token stored on client side."""

    username: str | None = None


async def is_authenticated(token: str = Depends(oauth2_scheme)) -> bool:
    """Check if user is authenticated."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            config.token_auth.secret_key,
            algorithms=[config.token_auth.algorithm],
        )
        username: Optional[str] = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenDataIn(username=username)

    except JWTError as exc:
        raise credentials_exception from exc

    if token_data.username != config.admin.name:
        raise credentials_exception

    return True


class TokenOut(BaseModel):
    """Token model returned from `/token` endpoint."""

    access_token: str
    token_type: str


@server.post("/token", response_model=TokenOut)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """Acquire authentication token for session."""

    if not check_credentials(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.token_auth.expire_minutes)
    access_token = create_access_token(
        data={"sub": config.admin.name}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def check_credentials(username: str, password: str) -> bool:
    """Check if credentials are valid admin credentials."""
    return username == config.admin.name and password == config.admin.password


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create access token for session."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.token_auth.secret_key, algorithm=config.token_auth.algorithm
    )
    return encoded_jwt


@server.get("/menu")
async def monitor(
    resp: bool = Depends(is_authenticated),
) -> HTMLResponse:
    """Resource monitor page."""
    return HTMLResponse(content=str(resp), status_code=status.HTTP_200_OK)

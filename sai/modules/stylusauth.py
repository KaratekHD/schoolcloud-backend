# Sai - Karatek School Cloud
# Copyright (C) 2022 KaratekHD.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import os
import subprocess

from fastapi import Depends, Request
from pydantic import BaseModel

from sai import app, STYLUSAUTH_NODE, STYLUSAUTH_PATH, STYLUSAUTH_DATABASE, LOGGER
from sai.utils.authentication import JWTBearer, get_userinfo
from secrets import token_urlsafe

__MOD_NAME__ = "stylusauth"


class Token(BaseModel):
    username: str
    token: str


def add_user(username, mail="dummy@karatek.net", displayname="NoName"):
    token = token_urlsafe(25)
    os.chdir(STYLUSAUTH_PATH)
    subprocess.run(f"{STYLUSAUTH_NODE} dbUtil.js --db {STYLUSAUTH_DATABASE} rmuser {username}".split(" "))
    subprocess.run(f"{STYLUSAUTH_NODE} dbUtil.js --db {STYLUSAUTH_DATABASE} adduser {username} {token} {mail} {displayname}".split(" "))
    LOGGER.info(f"Added user {username} to the Stylusauth database.")
    return Token(username=username, token=token)


@app.get(f"/{__MOD_NAME__}/get_token/", dependencies=[Depends(JWTBearer())], response_model=Token)
async def token(request: Request):
    userinfo = get_userinfo(request)
    LOGGER.debug(userinfo)
    username = userinfo["preferred_username"]
    email = userinfo["email"]
    stylusauth_token = add_user(username, email, userinfo["given_name"])
    return stylusauth_token

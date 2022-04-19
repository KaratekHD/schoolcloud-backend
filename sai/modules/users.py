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

from fastapi import Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from sai import app
from sai.utils.authentication import JWTBearer, get_userinfo, generate_token

__MOD_NAME__ = "users"

basic = HTTPBasic()

class User(BaseModel):
    sub: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    locale: str
    email: str


@app.get(f"/{__MOD_NAME__}/userinfo", dependencies=[Depends(JWTBearer())], response_model=User)
async def userinfo(request: Request):
    return User.parse_obj(get_userinfo(request))


@app.get(f"/{__MOD_NAME__}/token")
async def token(credentials: HTTPBasicCredentials = Depends(basic)):
    return generate_token(credentials.username, credentials.password)
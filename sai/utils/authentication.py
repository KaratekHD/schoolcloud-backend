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

from fastapi import Header, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from sai import keycloak_openid
from keycloak.exceptions import KeycloakAuthenticationError


def decode(token: str):
    userinfo = keycloak_openid.userinfo(token)
    return userinfo

def get_userinfo(request: Request):
    auth = request.headers["authorization"]
    token = auth.split(" ")[1]
    userinfo = decode(token)
    return userinfo



class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if not "authorization" in request.headers:
            raise HTTPException(status_code=401, detail="Unauthorized.")
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        payload = False
        if jwtoken is not None:
            try:
                payload = decode(jwtoken)
            except KeycloakAuthenticationError:
                isTokenValid = False
            if payload:
                isTokenValid = True
        return isTokenValid


def generate_token(username, password):
    token = keycloak_openid.token(username, password)
    return token
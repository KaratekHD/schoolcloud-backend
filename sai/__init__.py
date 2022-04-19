# Sai - Karatek School Cloud
# Copyright (C) 2021 openSUSE contributors.
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

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from keycloak import KeycloakOpenID
import configparser

LOGGER = logging.getLogger(__name__)
# TODO: Change the logformat so that it fits uvicorn
LOGFORMAT = "[%(asctime)s | %(levelname)s] %(message)s"
DEBUG = True
if DEBUG:
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.DEBUG)
else:
    logging.basicConfig(
        format=LOGFORMAT,
        level=logging.INFO)

NO_LOAD = []
LOAD = []

config = configparser.ConfigParser()
config.read("config.ini")
KEYCLOAK_SERVER = config["KEYCLOAK"]["SERVER"]
KEYCLOAK_CLIENT = config["KEYCLOAK"]["CLIENT_ID"]
KEYCLOAK_REALM = config["KEYCLOAK"]["REALM"]
STYLUSAUTH_DATABASE = config["STYLUSAUTH"]["DATABASE"]
STYLUSAUTH_PATH = config["STYLUSAUTH"]["PATH"]
STYLUSAUTH_NODE = config["STYLUSAUTH"]["NODE"]

# Initialize app
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_SERVER, client_id=KEYCLOAK_CLIENT, realm_name=KEYCLOAK_REALM)
app = FastAPI()
app.logger = LOGGER
origins = [
    "http://localhost:8080",
    "http://meteor:8080",
    "https://yourkara.tech"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


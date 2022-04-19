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

import uvicorn
import importlib
from sai.modules import ALL_MODULES
from sai import app, LOGGER

IMPORTED = {}

def main():
	for module_name in ALL_MODULES:
		imported_module = importlib.import_module("sai.modules." + module_name)
		if not hasattr(imported_module, "__mod_name__"):
			imported_module.__mod_name__ = imported_module.__name__
		LOGGER.debug("Loaded Module {}".format(imported_module.__mod_name__))
		if not imported_module.__mod_name__.lower() in IMPORTED:
			IMPORTED[imported_module.__mod_name__.lower()] = imported_module
		else:
			raise Exception("Can't have two modules with the same name! Please change one") # NO_TWO_MODULES
	
@app.get("/")
async def root():
	return {"version": "1.0"}

main()

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)

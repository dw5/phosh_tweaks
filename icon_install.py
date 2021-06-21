#!/usr/bin/python3

#Phosh_look GPL3
#Copyright (C) 2019-2021 David Hamner

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
import os

script_path = os.path.dirname(os.path.realpath(__file__))
path = f"{script_path}/phosh_look.py"
install_path = f"/home/purism/.local/share/applications/phosh_look.desktop"

icon_file = f"""[Desktop Entry]
Name=Phosh Look
Type=Application
Icon=preferences-color
Exec={path}
Categories=Utility;"""

with open(install_path, "w+") as fh:
    fh.write(icon_file)

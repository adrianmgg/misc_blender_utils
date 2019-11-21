# Copyright (C) 2019 Adrian Guerra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

import pkgutil
from misc_utils_amgg import registration

bl_info = {
    "name": "Misc. Utils",
    "author": "Adrian Guerra",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": ""
}

num_imports = 0
__path__ = pkgutil.extend_path(__path__, __name__)
for module_loader, name, ispkg in pkgutil.walk_packages(path=__path__, prefix=f'{__name__}.'):
    __import__(name)
    num_imports += 1
print(f'{bl_info["name"]} imported {num_imports} classes.')


def register():
    registration.register_all()


def unregister():
    registration.unregister_all()

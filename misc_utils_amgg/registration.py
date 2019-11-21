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

from typing import Type, List

import bpy

classes_to_register: List[Type] = []


def _fix_property_inheritance(cls):
    # give properties of superclasses to class
    annotations = {}
    for a in reversed(cls.mro()):
        if '__annotations__' in dir(a):
            for k, v in a.__annotations__.items():
                # copy annotation if it is a property definition
                if isinstance(v, tuple) and len(v) == 2 and v[0].__module__ == 'bpy.props':
                    annotations[k] = v
    if len(annotations) > 0:
        annotations.update(cls.__annotations__)
        cls.__annotations__ = annotations


def register_class(cls: Type):
    _fix_property_inheritance(cls)
    classes_to_register.append(cls)
    return cls


def register_all():
    for cls in classes_to_register:
        bpy.utils.register_class(cls)


def unregister_all():
    for cls in classes_to_register:
        bpy.utils.unregister_class(cls)

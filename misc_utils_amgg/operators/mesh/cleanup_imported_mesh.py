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


import bpy
import bmesh

from misc_utils_amgg.registration import register_class


@register_class
class CleanUpImportedMesh(bpy.types.Operator):
    # TODO description
    bl_idname = 'mesh.cleanup_imported_mesh'
    bl_label = 'Clean Up Imported Mesh'
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT') and (context.active_object.type == 'MESH')

    def execute(self, context: bpy.types.Context):



        return {'FINISHED'}

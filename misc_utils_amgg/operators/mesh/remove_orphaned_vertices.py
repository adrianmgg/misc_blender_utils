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
from typing import cast

import bpy
import bmesh
from mathutils.kdtree import KDTree

from misc_utils_amgg.registration import register_class


@register_class
class RemoveOrphanedVertices(bpy.types.Operator):
    bl_idname = 'mesh.remove_orphaned_vertices'
    bl_label = 'Remove Orphaned Vertices'
    bl_options = {'UNDO', 'REGISTER'}
    bl_description = 'Remove vertices which are not part of any edges or faces'

    unselected: bpy.props.BoolProperty(
        name='Unselected',
        default=False
    )

    @classmethod
    def poll(cls, context):
        if context.mode != 'EDIT_MESH':
            return False
        if context.edit_object is None:
            return False
        return True

    # TODO factor multi-edit code out of this and others & into a common base class
    def execute(self, context: bpy.types.Context):
        vert: bmesh.types.BMVert

        meshes_edited = 0
        total_verts_removed = 0
        # multi edit
        for target_object in context.selected_objects:
            if target_object.type != 'MESH':
                continue

            # setup bmesh
            mesh = cast(bpy.types.Mesh, target_object.data)
            bm = bmesh.from_edit_mesh(mesh)

            for vert in bm.verts:
                if self.unselected or vert.select:
                    if len(vert.link_edges) == 0:
                        bm.verts.remove(vert)
                        total_verts_removed += 1

            # update mesh
            bmesh.update_edit_mesh(mesh, True)

        report = f'Removed {total_verts_removed} vertices'
        if meshes_edited > 1:
            report += f' across {meshes_edited} meshes'
        self.report({'INFO'}, report)

        return {'FINISHED'}

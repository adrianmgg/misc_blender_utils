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
class RemoveBackfacingDoubles(bpy.types.Operator):
    # TODO describe
    bl_idname = 'mesh.remove_backfacing_doubles'
    bl_label = 'Remove Backfacing Doubles'
    bl_options = {'UNDO', 'REGISTER'}

    unselected: bpy.props.BoolProperty(
        name='Unselected',
        default=False
    )

    merge_distance: bpy.props.FloatProperty(
        name='Merge Distance',
        default=0.0001,
        min=0,
        precision=6,
        unit='LENGTH'
    )

    @classmethod
    def poll(cls, context):
        if context.mode != 'EDIT_MESH':
            return False
        if context.edit_object is None:
            return False
        return True

    def execute(self, context: bpy.types.Context):
        face: bmesh.types.BMFace
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

            # setup kdtree
            kd = KDTree(len(bm.verts))
            for i, vert in enumerate(bm.verts):
                if vert.select:
                    kd.insert(vert.co, i)
            kd.balance()

            for face in bm.faces:
                face.tag = False

            for face in bm.faces:
                if face.tag:
                    continue
                close_face_sets = []
                for vert in face.verts:
                    close_verts = kd.find_range(vert.co, self.merge_distance)
                    if len(close_verts) < 2:
                        break
                    # set of all faces which include a vert in close_verts (excluding current vert)
                    # and which have the same number of verts as the current face
                    close_face_sets.append(set.union(
                        *[
                            {f for f in bm.verts[i].link_faces if len(face.verts) == len(f.verts) and f != face}
                            for _, i, _ in close_verts if i != vert.index
                        ]
                    ))
                else:  # didn't break
                    # faces that had a vert close to each vert of current face
                    close_faces = set.intersection(*close_face_sets)

                    for f in close_faces:
                        f.tag = True

            for face in bm.faces:
                face.select_set(face.tag)

            # update mesh
            bmesh.update_edit_mesh(mesh, True)

        report = f'Removed {total_verts_removed} vertices'
        if meshes_edited > 1:
            report += f' across {meshes_edited} meshes'
        self.report({'INFO'}, report)

        return {'FINISHED'}

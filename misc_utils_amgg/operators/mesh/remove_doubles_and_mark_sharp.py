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
class RemoveDoublesAndMarkSharp(bpy.types.Operator):
    """Marks boundary edges as sharp, then removes doubles (merges vertices by distance)"""
    bl_idname = 'mesh.remove_doubles_and_mark_sharp'
    bl_label = 'Remove Doubles and Mark Sharp'
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
        meshes_edited = 0
        verts_removed = 0
        # multi edit
        for target_object in context.selected_objects:
            if target_object.type != 'MESH':
                continue

            # get object to edit & convert it to a bmesh object
            # target_object = context.edit_object
            mesh = target_object.data
            bm = bmesh.from_edit_mesh(mesh)

            # tag all relevant edges which are boundaries *before* removing doubles
            for edge in bm.edges:
                edge.tag = False
                if self.unselected or edge.select:
                    if edge.is_boundary:
                        edge.tag = True

            if self.unselected:
                remove_doubles_verts = bm.verts
            else:
                remove_doubles_verts = [vert for vert in bm.verts if vert.select]

            num_verts_before_remove_doubles = len(bm.verts)
            bmesh.ops.remove_doubles(
                bm,
                verts=remove_doubles_verts,
                dist=self.merge_distance
            )
            verts_removed += num_verts_before_remove_doubles - len(bm.verts)
            meshes_edited += 1

            # mark edges that used to be boundaries but now aren't as sharp
            for edge in bm.edges:
                if edge.tag and not edge.is_boundary:
                    edge.smooth = False

            bm.select_flush_mode()

            bmesh.update_edit_mesh(mesh, True)

            if not mesh.has_custom_normals:
                mesh.use_auto_smooth = True

        report = f'Removed {verts_removed} vertices'
        if meshes_edited > 1:
            report += f' across {meshes_edited} meshes'
        self.report({'INFO'}, report)

        return {'FINISHED'}

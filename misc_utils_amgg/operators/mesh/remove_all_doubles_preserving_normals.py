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
from misc_utils_amgg.util.context_managers import withbmesh


# TODO refactor this to work in edit mode and to only operate on selected vertices - will probably require reimplementing the data transfer modifier
@register_class
class RemoveAllDoublesPreservingNormals(bpy.types.Operator):
    # TODO write docstring
    bl_idname = 'mesh.remove_all_doubles_preserving_normals'
    bl_label = 'Remove all Doubles Preserving Normals'
    bl_options = {'UNDO', 'REGISTER'}
    
    merge_distance: bpy.props.FloatProperty(
        name='Merge Distance',
        default=0.0001,
        min=0,
        precision=6,
        unit='LENGTH'
    )
    
    @classmethod
    def poll(cls, context):
        if context.mode != 'OBJECT':
            return False
        return True
    
    def execute(self, context: bpy.types.Context):
        # remember active object to restore later
        active = bpy.context.view_layer.objects.active

        targets = [x for x in bpy.context.selected_objects if x.type == 'MESH']
        modifiers_to_apply = []

        for obj in targets:
            # create duplicate object containing duplicate data & link it to scene
            obj_copy = obj.copy()
            obj_copy.data = obj.data.copy()
            bpy.context.collection.objects.link(obj_copy)  # idk whether this is actually necessary

            # add data transfer modifier
            modifier = obj.modifiers.new(name='Data Transfer', type='DATA_TRANSFER')
            # move modifer to top of modifier stack
            for _ in range(obj.modifiers.find(modifier.name)):
                bpy.ops.object.modifier_move_up({'active_object': obj}, modifier=modifier.name)  # FIXME can this be done without an operator?
            # setup modifier
            modifier.object = obj_copy
            modifier.use_loop_data = True
            modifier.data_types_loops = {'CUSTOM_NORMAL'}
            modifier.loop_mapping = 'TOPOLOGY'

            with withbmesh() as mesh:
                mesh.from_mesh(obj.data)
                bmesh.ops.remove_doubles(mesh, verts=mesh.verts, dist=self.merge_distance)  # TODO make this an option when this gets ported to an operator
                mesh.to_mesh(obj.data)

            bpy.ops.object.modifier_apply({'active_object': obj}, apply_as='DATA', modifier=modifier.name)

            bpy.data.objects.remove(obj_copy)

        return {'FINISHED'}

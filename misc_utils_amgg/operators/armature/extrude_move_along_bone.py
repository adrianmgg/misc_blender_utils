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


import typing

import bpy
from mathutils import Vector

from misc_utils_amgg.registration import register_class


@register_class
class ExtrudeMoveOrientToParentBone(bpy.types.Operator):
    bl_idname = 'armature.extrude_move_orient_to_parent_bone'
    bl_label = 'Extrude Along Bone'

    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        if context.mode != 'EDIT_ARMATURE':
            return False
        # if len(context.selected_editable_bones) < 1:
        #     return False
        return True

    def execute(self, context: 'bpy.types.Context'):
        bpy.ops.armature.extrude()

        for bone in context.edit_object.data.edit_bones:
            if bone.select_tail:
                if bone.parent is not None:
                    parent_vector = (Vector(bone.parent.tail) - Vector(bone.parent.head)).normalized()
                    bone.tail = Vector(bone.head) + parent_vector * 1e-6
                else:  # bone.parent is None
                    bone.tail = Vector(bone.head) + Vector(0, 0, 1)
                print(bone.head, bone.tail)

        original_pivot_point = context.scene.tool_settings.transform_pivot_point
        context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        bpy.ops.transform.translate('INVOKE_DEFAULT', orient_type='NORMAL', constraint_axis=(False, True, False))
        context.scene.tool_settings.transform_pivot_point = original_pivot_point
        return {'FINISHED'}

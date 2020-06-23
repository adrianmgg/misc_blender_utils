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

from misc_utils_amgg.registration import register_class


@register_class
class RemoveUnusedMaterialSlots(bpy.types.Operator):
    bl_idname = 'mesh.remove_unused_material_slots'
    bl_label = 'Remove Unused Material Slots'
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        # is there at least one object selected?
        if len(context.selected_objects) < 1:
            return False
        # is at least one of the selected objects a mesh?
        if not max((obj.type == 'MESH' for obj in context.selected_objects)):
            return False
        return True

    # https://blenderartists.org/t/removing-specific-material-slots/540802/2
    # https://blenderartists.org/t/delete-from-a-bpy-collection/550197/4
    def execute(self, context: bpy.types.Context):
        num_material_slots_removed = 0

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            used_material_slots = set((poly.material_index for poly in obj.data.polygons))

            for i in reversed(range(len(obj.material_slots))):
                if i not in used_material_slots:
                    obj.data.materials.pop(index=i)
                    num_material_slots_removed += 1

        self.report({'INFO'}, f'Removed {num_material_slots_removed} material slots.')

        return {'FINISHED'}

from contextlib import contextmanager

import bpy
import bmesh


@contextmanager
def withbmesh():  # TODO give this a better name
    try:
        bm = bmesh.new()
        yield bm
    finally:
        bm.free()

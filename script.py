import bpy

terrain = bpy.context.active_object
if terrain is None:
    raise Exception("No active object")

# Decimate (reduce vertices)
dec = terrain.modifiers.new(name="Decimate", type='DECIMATE')
dec.ratio = 0.1
bpy.ops.object.modifier_apply(modifier=dec.name)

# Scale to max. 20cm
dims = terrain.dimensions
max_dim = max(dims.x, dims.y)
scale_factor = 0.20 / max_dim
terrain.scale = (scale_factor, scale_factor, scale_factor)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Reduce 0 level
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')

mesh = terrain.data
verts_to_delete = [v for v in mesh.vertices if (terrain.matrix_world @ v.co).z <= 0.0001]

for v in verts_to_delete:
    v.select = True

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')

# Calculate dim
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.context.view_layer.update()

dims = terrain.dimensions
terrain.location.x = dims.x / -2.0
terrain.location.y = dims.y / -2.0

# New min level
verts_global = [terrain.matrix_world @ v.co for v in terrain.data.vertices]
min_z = min(v.z for v in verts_global)
terrain.location.z -= min_z

# Extrude and flatten bottom
verts_global = [terrain.matrix_world @ v.co for v in terrain.data.vertices]
min_z = min(v.z for v in verts_global)
max_z = max(v.z for v in verts_global)
height = max_z - min_z
diff = (height / 2) + 0.005

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value": (0, 0, -diff)}
)

# 0 extrude level
min_z = min((terrain.matrix_world @ v.co).z for v in terrain.data.vertices)
terrain.location.z -= min_z

bpy.ops.transform.resize(value=(1, 1, 0))
bpy.ops.object.mode_set(mode='OBJECT')

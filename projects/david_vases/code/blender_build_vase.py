import bpy
import bmesh
import math
import os
from mathutils import Vector

OUT_DIR = r"D:\Session1\dhg508-workspace\projects\david_vases\code\virtual_gallery"
OUT_GLB = os.path.join(OUT_DIR, "vase.glb")
SPIN_STEPS = 128

# ---------- 清场（只清我们自己的） ----------
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')

coll_name = "DavidVases"
coll = bpy.data.collections.get(coll_name)
if coll is None:
    coll = bpy.data.collections.new(coll_name)
    bpy.context.scene.collection.children.link(coll)

# 删除旧对象
for ob in list(coll.objects):
    bpy.data.objects.remove(ob, do_unlink=True)

def link(ob):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)

def smooth(ob):
    for p in ob.data.polygons:
        p.use_smooth = True

# ---------- 1. 瓶身：旋转成型 ----------
profile = [
    (0.0000, 0.000),
    (0.0875, 0.000),
    (0.0875, 0.020),
    (0.0780, 0.028),
    (0.0800, 0.060),
    (0.0860, 0.110),
    (0.0920, 0.170),
    (0.0960, 0.230),
    (0.0975, 0.290),
    (0.0960, 0.340),
    (0.0900, 0.390),
    (0.0800, 0.430),
    (0.0680, 0.465),
    (0.0580, 0.495),
    (0.0530, 0.520),
    (0.0540, 0.545),
    (0.0620, 0.575),
    (0.0700, 0.600),
    (0.0735, 0.618),
    (0.0700, 0.630),
    (0.0620, 0.638),
]

bm = bmesh.new()
prev = None
first = None
for (r, z) in profile:
    v = bm.verts.new((r, 0.0, z))
    if prev is not None:
        bm.edges.new((prev, v))
    else:
        first = v
    prev = v

geom = bm.verts[:] + bm.edges[:]
bmesh.ops.spin(
    bm, geom=geom, cent=(0, 0, 0), axis=(0, 0, 1), dvec=(0, 0, 0),
    angle=2 * math.pi, steps=SPIN_STEPS, use_merge=True
)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

mesh = bpy.data.meshes.new("DavidVaseMesh")
bm.to_mesh(mesh)
bm.free()
body = bpy.data.objects.new("DavidVase", mesh)
link(body)
smooth(body)

# ---------- 2. 象首耳 + 瓷环 ----------
parts = [body]

def add_head(sign):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24, ring_count=16, radius=1.0,
        location=(sign * 0.062, 0.0, 0.552)
    )
    ob = bpy.context.object
    ob.scale = (0.020, 0.024, 0.030)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    smooth(ob)
    parts.append(ob)
    return ob

def add_trunk(sign):
    pts = [
        (0.068, 0.0, 0.548),
        (0.082, 0.0, 0.532),
        (0.088, 0.0, 0.512),
        (0.086, 0.0, 0.492),
        (0.082, 0.0, 0.480),
    ]
    cu = bpy.data.curves.new("trunk", 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = 0.0065
    cu.bevel_resolution = 6
    cu.resolution_u = 12
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(pts) - 1)
    for i, (x, y, z) in enumerate(pts):
        bp = sp.bezier_points[i]
        bp.co = (sign * x, y, z)
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new("trunk", cu)
    link(ob)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target='MESH')
    ob = bpy.context.object
    smooth(ob)
    parts.append(ob)
    return ob

def add_ring(sign):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.018, minor_radius=0.0035,
        major_segments=40, minor_segments=12,
        location=(sign * 0.081, 0.0, 0.462),
        rotation=(math.pi / 2, 0.0, 0.0)
    )
    ob = bpy.context.object
    smooth(ob)
    parts.append(ob)
    return ob

for s in (1, -1):
    add_head(s)
    add_trunk(s)
    add_ring(s)

# ---------- 3. 材质：白瓷 ----------
mat = bpy.data.materials.get("PorcelainWhite")
if mat is None:
    mat = bpy.data.materials.new("PorcelainWhite")
mat.use_nodes = True
mat.use_backface_culling = False
nt = mat.node_tree
bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
if bsdf is not None:
    def setval(name, val):
        if name in bsdf.inputs:
            bsdf.inputs[name].default_value = val
    setval("Base Color", (0.93, 0.94, 0.945, 1.0))
    setval("Metallic", 0.0)
    setval("Roughness", 0.14)
    setval("IOR", 1.5)
    setval("Coat Weight", 1.0)
    setval("Coat Roughness", 0.03)
    setval("Subsurface Weight", 0.03)

for ob in parts:
    ob.data.materials.clear()
    ob.data.materials.append(mat)

# ---------- 4. 合并为一个对象 ----------
bpy.ops.object.select_all(action='DESELECT')
for ob in parts:
    ob.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
vase = bpy.context.object
vase.name = "DavidVase"
vase.data.name = "DavidVaseMesh"

# 落地：底面在 z=0
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
vase.location = (0, 0, vase.dimensions.z / 2.0)

bpy.ops.object.select_all(action='DESELECT')
vase.select_set(True)
bpy.context.view_layer.objects.active = vase

# ---------- 5. 导出 GLB ----------
os.makedirs(OUT_DIR, exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=OUT_GLB,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)

print("OK: vase built and exported ->", OUT_GLB)
print("尺寸 (m):", tuple(round(v, 4) for v in vase.dimensions))

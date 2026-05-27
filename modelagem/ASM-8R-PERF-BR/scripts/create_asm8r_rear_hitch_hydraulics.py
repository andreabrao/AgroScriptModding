"""Create ASM-8R-PERF-BR rear hitch, hydraulics, SCVs, PTO and drawbar base.

Run inside Blender:
  Scripting > Open this file > Run Script

This is an editable high-poly starting point for Production Pass 05:
- rear 3-point hitch Cat 4N/3 visual base
- lower links, top link, stabilizers and lift cylinders
- rear SCV block with 5 quick couplers and hoses
- PTO shaft and guard
- oscillating drawbar
- animation/attacher empties
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_REAR_HITCH_HYDRAULICS"

MATERIALS = {
    "mat_hp_hitch_cast": (0.18, 0.19, 0.19, 1.0, 0.76, 0.58),
    "mat_hp_hydraulic_body": (0.12, 0.13, 0.14, 1.0, 0.80, 0.45),
    "mat_hp_chrome_rod": (0.78, 0.78, 0.74, 1.0, 0.95, 0.22),
    "mat_hp_rubber_hose": (0.018, 0.018, 0.016, 1.0, 0.0, 0.86),
    "mat_hp_quick_coupler": (0.58, 0.58, 0.54, 1.0, 0.88, 0.35),
    "mat_hp_pin_bolt": (0.68, 0.66, 0.60, 1.0, 0.90, 0.34),
    "mat_hp_pto_dark": (0.05, 0.052, 0.048, 1.0, 0.65, 0.62),
    "mat_hp_guide_red": (0.78, 0.03, 0.02, 1.0, 0.0, 0.50),
}


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def ensure_collection(name, parent=None):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)

    parent_collection = parent or bpy.context.scene.collection
    if collection.name not in parent_collection.children.keys():
        parent_collection.children.link(collection)

    return collection


def create_materials():
    for name, (r, g, b, a, metallic, roughness) in MATERIALS.items():
        material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        material.diffuse_color = (r, g, b, a)
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (r, g, b, a)
            bsdf.inputs["Metallic"].default_value = metallic
            bsdf.inputs["Roughness"].default_value = roughness


def mat(name):
    return bpy.data.materials[name]


def link_to(collection, obj):
    for current in obj.users_collection:
        current.objects.unlink(obj)
    collection.objects.link(obj)


def shade(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth()
    except RuntimeError:
        pass
    obj.select_set(False)
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def add_bevel(obj, width=0.025, segments=2):
    bevel = obj.modifiers.new("hp_bevel", "BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.affect = "EDGES"
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def cube_obj(name, location, scale, material_name, collection, rotation=(0.0, 0.0, 0.0), bevel=0.025):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    if bevel:
        add_bevel(obj, bevel, 2)
    return obj


def cylinder_obj(name, location, radius, depth, material_name, collection, axis="Z", vertices=48, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    if axis == "X":
        obj.rotation_euler[1] += math.radians(90)
    elif axis == "Y":
        obj.rotation_euler[0] += math.radians(90)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    shade(obj)
    return obj


def torus_obj(name, location, major_radius, minor_radius, material_name, collection, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=48,
        minor_segments=12,
        major_radius=major_radius,
        minor_radius=minor_radius,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    shade(obj)
    return obj


def pipe_between(name, start, end, radius, material_name, collection, vertices=24):
    sx, sy, sz = start
    ex, ey, ez = end
    dx, dy, dz = ex - sx, ey - sy, ez - sz
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length <= 0.0001:
        return None

    center = ((sx + ex) / 2, (sy + ey) / 2, (sz + ez) / 2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=center)
    obj = bpy.context.object
    obj.name = name

    import mathutils

    direction = mathutils.Vector((dx / length, dy / length, dz / length))
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    shade(obj)
    return obj


def empty_obj(name, location, collection, size=0.24):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = size
    obj.location = location
    collection.objects.link(obj)
    return obj


def add_hitch_frame(collection):
    cube_obj("hp_rear_hitch_main_support", (0.0, -2.58, 0.98), (1.30, 0.28, 0.78), "mat_hp_hitch_cast", collection, bevel=0.040)
    cube_obj("hp_rear_hitch_top_tower", (0.0, -2.72, 1.42), (0.54, 0.22, 0.58), "mat_hp_hitch_cast", collection, bevel=0.035)
    cube_obj("hp_rear_hitch_crossbar_lower", (0.0, -2.86, 0.66), (1.45, 0.18, 0.20), "mat_hp_hitch_cast", collection, bevel=0.025)
    cube_obj("hp_rear_hitch_side_plate_l", (-0.72, -2.68, 0.92), (0.12, 0.46, 0.70), "mat_hp_hitch_cast", collection, bevel=0.025)
    cube_obj("hp_rear_hitch_side_plate_r", (0.72, -2.68, 0.92), (0.12, 0.46, 0.70), "mat_hp_hitch_cast", collection, bevel=0.025)

    for x, side in [(-0.48, "l"), (0.48, "r")]:
        cylinder_obj(f"hp_lower_link_mount_pin_{side}", (x, -2.80, 0.62), 0.055, 0.22, "mat_hp_pin_bolt", collection, axis="X", vertices=28)
        empty_obj(f"empty_rear_lower_link_{side}_pivot", (x, -2.80, 0.62), collection)

    empty_obj("empty_top_link_pivot", (0.0, -2.84, 1.42), collection)
    empty_obj("empty_attacher_rear_3pt", (0.0, -3.46, 0.92), collection, size=0.34)


def add_lower_links_and_toplink(collection):
    for x, side in [(-0.48, "l"), (0.48, "r")]:
        link = cube_obj(
            f"hp_rear_lower_link_{side}",
            (x, -3.25, 0.58),
            (0.16, 1.08, 0.12),
            "mat_hp_hitch_cast",
            collection,
            rotation=(0.0, 0.0, math.radians(0)),
            bevel=0.025,
        )
        link["asm_pivot"] = f"empty_rear_lower_link_{side}_pivot"
        torus_obj(f"hp_rear_lower_link_eye_outer_{side}", (x, -3.84, 0.58), 0.105, 0.026, "mat_hp_hitch_cast", collection, rotation=(math.radians(90), 0, 0))
        cylinder_obj(f"hp_rear_lower_link_pin_outer_{side}", (x, -3.84, 0.58), 0.040, 0.22, "mat_hp_pin_bolt", collection, axis="X", vertices=24)
        cube_obj(f"hp_rear_lower_link_lock_clip_{side}", (x, -3.96, 0.66), (0.11, 0.035, 0.07), "mat_hp_pin_bolt", collection, bevel=0.006)

        pipe_between(f"hp_stabilizer_link_{side}", (x * 1.22, -2.70, 0.82), (x, -3.52, 0.64), 0.035, "mat_hp_hitch_cast", collection, vertices=20)

    pipe_between("hp_top_link_body_threaded", (0.0, -2.88, 1.42), (0.0, -3.66, 1.14), 0.055, "mat_hp_hitch_cast", collection, vertices=28)
    torus_obj("hp_top_link_eye_front", (0.0, -2.88, 1.42), 0.105, 0.026, "mat_hp_hitch_cast", collection, rotation=(math.radians(90), 0, 0))
    torus_obj("hp_top_link_eye_rear", (0.0, -3.66, 1.14), 0.105, 0.026, "mat_hp_hitch_cast", collection, rotation=(math.radians(90), 0, 0))

    for index in range(8):
        y = -3.00 - index * 0.075
        torus_obj(f"hp_top_link_thread_ring_{index + 1:02d}", (0.0, y, 1.38 - index * 0.026), 0.060, 0.004, "mat_hp_pin_bolt", collection, rotation=(math.radians(90), 0, 0))


def add_hydraulic_cylinders(collection):
    for x, side in [(-0.62, "l"), (0.62, "r")]:
        cylinder_obj(f"hp_hitch_cylinder_body_{side}", (x, -2.86, 1.02), 0.060, 0.50, "mat_hp_hydraulic_body", collection, axis="Y", vertices=32)
        cylinder_obj(f"hp_hitch_cylinder_rod_{side}", (x, -3.18, 0.84), 0.034, 0.58, "mat_hp_chrome_rod", collection, axis="Y", vertices=32)
        torus_obj(f"hp_hitch_cylinder_base_eye_{side}", (x, -2.60, 1.10), 0.070, 0.018, "mat_hp_hydraulic_body", collection, rotation=(math.radians(90), 0, 0))
        torus_obj(f"hp_hitch_cylinder_rod_eye_{side}", (x, -3.46, 0.72), 0.064, 0.016, "mat_hp_hydraulic_body", collection, rotation=(math.radians(90), 0, 0))
        empty_obj(f"empty_hitch_cylinder_{side}_base", (x, -2.60, 1.10), collection)
        empty_obj(f"empty_hitch_cylinder_{side}_rod", (x, -3.46, 0.72), collection)


def add_scvs_and_hoses(collection):
    cube_obj("hp_rear_scv_block_5_outputs", (0.70, -2.72, 1.28), (0.36, 0.20, 0.56), "mat_hp_hitch_cast", collection, bevel=0.025)
    colors_z = [1.06, 1.16, 1.26, 1.36, 1.46]

    for index, z in enumerate(colors_z, start=1):
        cylinder_obj(f"hp_scv_quick_coupler_{index:02d}", (0.48, -2.86, z), 0.045, 0.085, "mat_hp_quick_coupler", collection, axis="Y", vertices=28)
        torus_obj(f"hp_scv_cap_{index:02d}", (0.47, -2.91, z), 0.050, 0.008, "mat_hp_rubber_hose", collection, rotation=(math.radians(90), 0, 0))
        pipe_between(
            f"hp_hydraulic_hose_{index:02d}",
            (0.80, -2.64, z),
            (0.38 + index * 0.03, -3.22, 0.86 + index * 0.035),
            0.018,
            "mat_hp_rubber_hose",
            collection,
            vertices=16,
        )

    empty_obj("empty_hydraulic_connector_rear", (0.46, -2.92, 1.26), collection)


def add_pto_and_drawbar(collection):
    cylinder_obj("hp_rear_pto_shaft_splined_base", (0.0, -2.98, 0.76), 0.085, 0.28, "mat_hp_pto_dark", collection, axis="Y", vertices=40)
    cylinder_obj("hp_rear_pto_guard", (0.0, -2.88, 0.78), 0.155, 0.16, "mat_hp_hitch_cast", collection, axis="Y", vertices=48)
    for index in range(12):
        angle = math.tau * index / 12
        x = math.cos(angle) * 0.080
        z = 0.76 + math.sin(angle) * 0.080
        cube_obj(f"hp_pto_spline_{index + 1:02d}", (x, -3.14, z), (0.012, 0.13, 0.025), "mat_hp_pin_bolt", collection, rotation=(0.0, 0.0, angle), bevel=0.002)

    cube_obj("hp_drawbar_support_box", (0.0, -2.86, 0.38), (0.54, 0.30, 0.22), "mat_hp_hitch_cast", collection, bevel=0.025)
    cube_obj("hp_drawbar_oscillating", (0.0, -3.42, 0.34), (0.22, 1.12, 0.12), "mat_hp_hitch_cast", collection, bevel=0.020)
    cylinder_obj("hp_drawbar_rear_pin", (0.0, -4.02, 0.36), 0.050, 0.24, "mat_hp_pin_bolt", collection, axis="X", vertices=28)
    torus_obj("hp_drawbar_hole_ring", (0.0, -4.02, 0.36), 0.085, 0.020, "mat_hp_hitch_cast", collection, rotation=(math.radians(90), 0, 0))

    empty_obj("empty_pto_rotation_pivot", (0.0, -3.04, 0.76), collection)
    empty_obj("empty_power_takeoff_rear", (0.0, -3.18, 0.76), collection)
    empty_obj("empty_drawbar_pivot", (0.0, -2.92, 0.34), collection)
    empty_obj("empty_attacher_drawbar", (0.0, -4.06, 0.36), collection, size=0.32)


def add_bolts_and_pins(collection):
    bolt_points = [
        (-0.58, -2.52, 1.18),
        (0.58, -2.52, 1.18),
        (-0.58, -2.52, 0.82),
        (0.58, -2.52, 0.82),
        (-0.36, -2.92, 1.42),
        (0.36, -2.92, 1.42),
    ]
    for index, point in enumerate(bolt_points, start=1):
        cylinder_obj(f"hp_rear_hitch_mount_bolt_{index:02d}", point, 0.035, 0.045, "mat_hp_pin_bolt", collection, axis="Y", vertices=20)


def add_guides_and_labels(collection):
    cube_obj("guide_rear_hitch_centerline", (0.0, -3.10, 0.08), (0.04, 1.90, 0.04), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_lower_link_width", (0.0, -3.42, 0.12), (1.10, 0.04, 0.04), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_pto_height", (0.0, -3.05, 0.76), (0.70, 0.035, 0.035), "mat_hp_guide_red", collection, bevel=0.0)

    labels = [
        ("label_cat4n3_hitch", (0.0, -3.26, 1.74), "Cat 4N/3 rear hitch"),
        ("label_scv_5_outputs", (0.92, -2.95, 1.62), "5 rear SCVs"),
        ("label_pto_drawbar", (0.0, -4.05, 0.70), "PTO + oscillating drawbar"),
    ]
    for name, location, text in labels:
        curve = bpy.data.curves.new(name, "FONT")
        curve.body = text
        curve.size = 0.105
        curve.align_x = "CENTER"
        obj = bpy.data.objects.new(name, curve)
        obj.location = location
        obj.rotation_euler[0] = math.radians(70)
        obj.data.materials.append(mat("mat_hp_guide_red"))
        collection.objects.link(obj)


def setup_scene():
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.render.engine = "CYCLES"

    camera_data = bpy.data.cameras.new("camera_rear_hitch_review")
    camera = bpy.data.objects.new("camera_rear_hitch_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (3.0, -6.2, 2.2)
    camera.rotation_euler = (math.radians(67), 0, math.radians(28))
    bpy.context.scene.camera = camera

    sun_data = bpy.data.lights.new("sun_rear_hitch_key", "SUN")
    sun = bpy.data.objects.new("sun_rear_hitch_key", sun_data)
    sun.rotation_euler = (math.radians(48), 0, math.radians(32))
    bpy.context.scene.collection.objects.link(sun)


def main():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    hitch_col = ensure_collection("01_rear_hitch_cat4n3", root)
    hydraulic_col = ensure_collection("02_hydraulic_cylinders_and_hoses", root)
    scv_col = ensure_collection("03_rear_scvs_quick_couplers", root)
    pto_col = ensure_collection("04_pto_drawbar_attachers", root)
    guide_col = ensure_collection("05_guides_and_labels", root)

    add_hitch_frame(hitch_col)
    add_lower_links_and_toplink(hitch_col)
    add_bolts_and_pins(hitch_col)
    add_hydraulic_cylinders(hydraulic_col)
    add_scvs_and_hoses(scv_col)
    add_pto_and_drawbar(pto_col)
    add_guides_and_labels(guide_col)
    setup_scene()

    print("ASM-8R-PERF-BR rear hitch/hydraulics base created.")
    print("Save as ASM_8R_PERF_BR_highpoly_rear_hitch_v001.blend")


if __name__ == "__main__":
    main()

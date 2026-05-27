"""Create ASM-8R-PERF-BR chassis, ILS and e23 transmission high-poly base.

Run inside Blender:
  Scripting > Open this file > Run Script

This creates an editable mechanical base for Production Pass 03:
- monoblock chassis
- e23 transmission case
- front ILS independent suspension parts
- differential, hubs, knuckles, links and driveshafts
- animation pivots as empties
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_CHASSIS_ILS_TRANSMISSION"

FRONT_AXLE_Y = 1.525
REAR_AXLE_Y = -1.525

MATERIALS = {
    "mat_hp_chassis_dark_metal": (0.12, 0.14, 0.15, 1.0, 0.72, 0.52),
    "mat_hp_cast_transmission": (0.32, 0.33, 0.32, 1.0, 0.75, 0.66),
    "mat_hp_hydraulic_body": (0.18, 0.19, 0.20, 1.0, 0.85, 0.42),
    "mat_hp_chrome_rod": (0.78, 0.78, 0.74, 1.0, 0.95, 0.22),
    "mat_hp_bolt_metal": (0.68, 0.66, 0.60, 1.0, 0.90, 0.34),
    "mat_hp_grease_dark": (0.03, 0.03, 0.028, 1.0, 0.30, 0.82),
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


def add_bevel(obj, width=0.035, segments=2):
    bevel = obj.modifiers.new("hp_bevel", "BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.affect = "EDGES"
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def cube_obj(name, location, scale, material_name, collection, rotation=(0.0, 0.0, 0.0), bevel=0.035):
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


def cylinder_obj(name, location, radius, depth, material_name, collection, axis="Z", vertices=64, rotation=(0.0, 0.0, 0.0)):
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


def empty_obj(name, location, collection, size=0.28):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = size
    obj.location = location
    collection.objects.link(obj)
    return obj


def add_bolt_ring(prefix, center, radius, count, face_axis, collection):
    cx, cy, cz = center
    for index in range(count):
        angle = math.tau * index / count
        if face_axis == "Y":
            x = cx + math.cos(angle) * radius
            z = cz + math.sin(angle) * radius
            location = (x, cy, z)
            axis = "Y"
        else:
            y = cy + math.cos(angle) * radius
            z = cz + math.sin(angle) * radius
            location = (cx, y, z)
            axis = "X"

        cylinder_obj(
            f"hp_{prefix}_bolt_{index + 1:02d}",
            location,
            0.028,
            0.055,
            "mat_hp_bolt_metal",
            collection,
            axis=axis,
            vertices=18,
        )


def add_rib_series(prefix, y_start, y_end, x, z, count, collection, side):
    span = y_end - y_start
    for index in range(count):
        y = y_start + span * (index / max(count - 1, 1))
        rib = cube_obj(
            f"hp_{prefix}_rib_{side}_{index + 1:02d}",
            (x, y, z),
            (0.055, 0.045, 0.42),
            "mat_hp_cast_transmission",
            collection,
            bevel=0.015,
        )
        rib["asm_note"] = "Casting rib placeholder for high-poly refinement."


def add_chassis(collection):
    cube_obj("hp_chassis_left_longeron", (-0.42, 0.0, 0.82), (0.18, 5.35, 0.34), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_chassis_right_longeron", (0.42, 0.0, 0.82), (0.18, 5.35, 0.34), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_chassis_front_crossmember", (0.0, 2.48, 0.86), (1.18, 0.24, 0.38), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_chassis_center_crossmember", (0.0, 0.42, 0.86), (1.10, 0.22, 0.34), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_chassis_rear_crossmember", (0.0, -2.36, 0.86), (1.16, 0.28, 0.40), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_engine_mount_left", (-0.54, 1.15, 1.04), (0.18, 0.55, 0.18), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_engine_mount_right", (0.54, 1.15, 1.04), (0.18, 0.55, 0.18), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_front_weight_mount_plate", (0.0, 2.86, 0.82), (1.22, 0.18, 0.42), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_cab_mount_left_rear", (-0.58, -1.66, 1.12), (0.22, 0.28, 0.20), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_cab_mount_right_rear", (0.58, -1.66, 1.12), (0.22, 0.28, 0.20), "mat_hp_chassis_dark_metal", collection)
    cube_obj("hp_ils_mount_bridge", (0.0, 1.54, 0.96), (1.22, 0.28, 0.34), "mat_hp_chassis_dark_metal", collection)

    for x in (-0.58, 0.58):
        for y in (2.48, 0.42, -2.36):
            add_bolt_ring(f"chassis_mount_{side_name(x)}_{int((y + 3) * 100)}", (x, y, 1.06), 0.065, 6, "Y", collection)


def add_transmission(collection):
    cube_obj("hp_e23_transmission_main_case", (0.0, -0.55, 1.12), (1.18, 1.44, 0.78), "mat_hp_cast_transmission", collection, bevel=0.060)
    cube_obj("hp_e23_upper_hump", (0.0, -0.40, 1.58), (0.88, 0.94, 0.36), "mat_hp_cast_transmission", collection, bevel=0.050)
    cube_obj("hp_e23_rear_flange", (0.0, -1.32, 1.08), (0.96, 0.16, 0.62), "mat_hp_cast_transmission", collection, bevel=0.035)
    cube_obj("hp_e23_front_flange_engine_side", (0.0, 0.22, 1.08), (0.98, 0.16, 0.58), "mat_hp_cast_transmission", collection, bevel=0.035)
    cube_obj("hp_e23_left_side_cover", (-0.63, -0.55, 1.12), (0.10, 0.96, 0.58), "mat_hp_cast_transmission", collection, bevel=0.025)
    cube_obj("hp_e23_right_side_cover", (0.63, -0.55, 1.12), (0.10, 0.96, 0.58), "mat_hp_cast_transmission", collection, bevel=0.025)
    cylinder_obj("hp_e23_front_driveshaft_output", (0.0, 0.22, 0.70), 0.115, 0.34, "mat_hp_cast_transmission", collection, axis="Y", vertices=48)
    cylinder_obj("hp_rear_differential_case", (0.0, REAR_AXLE_Y, 0.98), 0.42, 0.88, "mat_hp_cast_transmission", collection, axis="X", vertices=72)

    add_rib_series("e23_case", -1.05, 0.06, -0.70, 1.20, 7, collection, "l")
    add_rib_series("e23_case", -1.05, 0.06, 0.70, 1.20, 7, collection, "r")
    add_bolt_ring("e23_left_cover", (-0.69, -0.55, 1.12), 0.30, 14, "X", collection)
    add_bolt_ring("e23_right_cover", (0.69, -0.55, 1.12), 0.30, 14, "X", collection)


def add_ils(collection):
    cube_obj("hp_ils_subframe_crossmember", (0.0, FRONT_AXLE_Y, 0.86), (1.30, 0.32, 0.32), "mat_hp_chassis_dark_metal", collection)
    cylinder_obj("hp_front_differential_case", (0.0, FRONT_AXLE_Y, 0.75), 0.34, 0.72, "mat_hp_cast_transmission", collection, axis="X", vertices=72)
    cylinder_obj("hp_front_driveshaft", (0.0, 0.82, 0.72), 0.045, 1.18, "mat_hp_hub_dark_metal" if "mat_hp_hub_dark_metal" in bpy.data.materials else "mat_hp_chassis_dark_metal", collection, axis="Y", vertices=24)

    for sign, side in [(-1, "l"), (1, "r")]:
        x_inner = sign * 0.38
        x_outer = sign * 0.88
        x_hub = sign * 0.98

        upper = cube_obj(
            f"hp_ils_upper_arm_{side}",
            (sign * 0.62, FRONT_AXLE_Y - 0.02, 0.99),
            (0.78, 0.12, 0.09),
            "mat_hp_cast_transmission",
            collection,
            rotation=(0.0, 0.0, math.radians(sign * -6)),
            bevel=0.020,
        )
        upper["asm_pivot"] = f"empty_ils_upper_arm_{side}_pivot"

        lower = cube_obj(
            f"hp_ils_lower_arm_{side}",
            (sign * 0.64, FRONT_AXLE_Y - 0.02, 0.56),
            (0.86, 0.14, 0.11),
            "mat_hp_cast_transmission",
            collection,
            rotation=(0.0, 0.0, math.radians(sign * -5)),
            bevel=0.022,
        )
        lower["asm_pivot"] = f"empty_ils_lower_arm_{side}_pivot"

        cylinder_obj(f"hp_front_halfshaft_{side}", (sign * 0.48, FRONT_AXLE_Y, 0.75), 0.040, 0.82, "mat_hp_chassis_dark_metal", collection, axis="X", vertices=24)
        cylinder_obj(f"hp_ils_cylinder_body_{side}", (x_inner, FRONT_AXLE_Y - 0.38, 0.92), 0.060, 0.52, "mat_hp_hydraulic_body", collection, axis="Y", vertices=32)
        cylinder_obj(f"hp_ils_cylinder_rod_{side}", (x_outer, FRONT_AXLE_Y - 0.26, 0.78), 0.035, 0.48, "mat_hp_chrome_rod", collection, axis="Y", vertices=32)
        cube_obj(f"hp_steering_knuckle_{side}", (x_hub, FRONT_AXLE_Y, 0.75), (0.20, 0.26, 0.54), "mat_hp_cast_transmission", collection, bevel=0.025)
        cylinder_obj(f"hp_front_hub_{side}", (x_hub, FRONT_AXLE_Y, 0.75), 0.25, 0.28, "mat_hp_cast_transmission", collection, axis="X", vertices=64)
        cylinder_obj(f"hp_steering_link_{side}", (sign * 0.54, FRONT_AXLE_Y - 0.42, 0.86), 0.030, 0.78, "mat_hp_chassis_dark_metal", collection, axis="X", vertices=20)

        empty_obj(f"empty_ils_upper_arm_{side}_pivot", (x_inner, FRONT_AXLE_Y - 0.02, 0.99), collection)
        empty_obj(f"empty_ils_lower_arm_{side}_pivot", (x_inner, FRONT_AXLE_Y - 0.02, 0.56), collection)
        empty_obj(f"empty_steering_knuckle_{side}_pivot", (x_hub, FRONT_AXLE_Y, 0.75), collection)
        empty_obj(f"empty_ils_cylinder_body_{side}_mount", (x_inner, FRONT_AXLE_Y - 0.64, 0.96), collection, size=0.20)
        empty_obj(f"empty_ils_cylinder_rod_{side}_mount", (x_outer, FRONT_AXLE_Y - 0.04, 0.74), collection, size=0.20)

    empty_obj("empty_front_diff_input_pivot", (0.0, FRONT_AXLE_Y - 0.34, 0.75), collection)
    empty_obj("empty_front_driveshaft_pivot", (0.0, 0.82, 0.72), collection)


def add_guides(collection):
    cube_obj("guide_wheelbase_3_050m", (0.0, 0.0, 0.05), (0.05, 3.050, 0.05), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_chassis_length_5_350m", (0.0, 0.0, 0.10), (0.08, 5.350, 0.05), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_front_axle_line", (0.0, FRONT_AXLE_Y, 0.13), (2.30, 0.035, 0.035), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_rear_axle_line", (0.0, REAR_AXLE_Y, 0.13), (2.55, 0.035, 0.035), "mat_hp_guide_red", collection, bevel=0.0)


def add_labels(collection):
    labels = [
        ("label_chassis", (0.0, 0.55, 1.32), "Monoblock chassis"),
        ("label_e23", (0.0, -0.55, 1.95), "e23 transmission case"),
        ("label_ils", (0.0, 1.78, 1.42), "ILS independent front axle"),
    ]
    for name, location, text in labels:
        curve = bpy.data.curves.new(name, "FONT")
        curve.body = text
        curve.size = 0.12
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

    camera_data = bpy.data.cameras.new("camera_chassis_ils_review")
    camera = bpy.data.objects.new("camera_chassis_ils_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (3.7, -5.3, 2.8)
    camera.rotation_euler = (math.radians(62), 0, math.radians(34))
    bpy.context.scene.camera = camera

    sun_data = bpy.data.lights.new("sun_chassis_key", "SUN")
    sun = bpy.data.objects.new("sun_chassis_key", sun_data)
    sun.rotation_euler = (math.radians(48), 0, math.radians(35))
    bpy.context.scene.collection.objects.link(sun)


def side_name(x):
    return "l" if x < 0 else "r"


def main():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    chassis_col = ensure_collection("01_chassis_monoblock", root)
    transmission_col = ensure_collection("02_e23_transmission_case", root)
    ils_col = ensure_collection("03_ils_front_axle_animation_parts", root)
    guide_col = ensure_collection("04_guides_and_labels", root)

    add_chassis(chassis_col)
    add_transmission(transmission_col)
    add_ils(ils_col)
    add_guides(guide_col)
    add_labels(guide_col)
    setup_scene()

    print("ASM-8R-PERF-BR chassis/ILS/transmission high-poly base created.")
    print("Save as ASM_8R_PERF_BR_highpoly_chassis_ils_v001.blend")


if __name__ == "__main__":
    main()

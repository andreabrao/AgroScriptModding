"""Create a proportional ASM-8R-PERF-BR blockout scene in Blender.

Run inside Blender:
  Scripting > Open this file > Run Script

The scene is a technical blockout, not a finished mesh.
It creates separate objects for body, cab, wheels, ILS, hitch, weights,
ASM exhaust and auxiliary lights.
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_BLOCKOUT"


MATERIALS = {
    "mat_blockout_jd_green": (0.02, 0.30, 0.07, 1.0),
    "mat_blockout_jd_yellow": (0.95, 0.70, 0.05, 1.0),
    "mat_blockout_dark_metal": (0.12, 0.14, 0.15, 1.0),
    "mat_blockout_cast_metal": (0.34, 0.35, 0.35, 1.0),
    "mat_blockout_rubber": (0.015, 0.014, 0.013, 1.0),
    "mat_blockout_glass": (0.12, 0.26, 0.30, 0.42),
    "mat_blockout_led": (0.80, 0.92, 1.0, 1.0),
    "mat_blockout_inox": (0.72, 0.70, 0.66, 1.0),
    "mat_blockout_weight": (0.08, 0.08, 0.07, 1.0),
    "mat_blockout_red": (0.70, 0.04, 0.03, 1.0),
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
    for name, color in MATERIALS.items():
        material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        material.diffuse_color = color
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = 0.55
            bsdf.inputs["Metallic"].default_value = 0.0
            if "metal" in name or "inox" in name or "weight" in name:
                bsdf.inputs["Metallic"].default_value = 0.75
            if "glass" in name:
                bsdf.inputs["Alpha"].default_value = color[3]
                material.blend_method = "BLEND"
            if "led" in name:
                bsdf.inputs["Emission Color"].default_value = color
                bsdf.inputs["Emission Strength"].default_value = 0.8


def mat(name):
    return bpy.data.materials[name]


def link_to(collection, obj):
    for current in obj.users_collection:
        current.objects.unlink(obj)
    collection.objects.link(obj)


def cube_obj(name, location, scale, material_name, collection):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    return obj


def cylinder_obj(name, location, radius, depth, material_name, collection, axis="X", vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name

    if axis == "X":
        obj.rotation_euler[1] = math.radians(90)
    elif axis == "Y":
        obj.rotation_euler[0] = math.radians(90)

    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    return obj


def empty_obj(name, location, collection, display_size=0.35):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = display_size
    obj.location = location
    collection.objects.link(obj)
    return obj


def bevel_modifier(obj, width=0.04, segments=2):
    modifier = obj.modifiers.new("blockout_bevel", "BEVEL")
    modifier.width = width
    modifier.segments = segments
    modifier.affect = "EDGES"
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def add_body(collections):
    col = collections["blockout"]
    cube_obj("lp_chassis_main_blockout", (0, 0.0, 0.86), (1.05, 5.35, 0.42), "mat_blockout_dark_metal", col)
    cube_obj("lp_transmission_e23_blockout", (0, -0.72, 1.08), (1.18, 1.55, 0.72), "mat_blockout_cast_metal", col)
    cube_obj("lp_hood_8r_blockout", (0, 1.34, 1.72), (1.42, 2.55, 0.92), "mat_blockout_jd_green", col)
    cube_obj("lp_front_grille_blockout", (0, 2.78, 1.65), (1.36, 0.18, 0.90), "mat_blockout_dark_metal", col)
    cube_obj("lp_side_panel_l_blockout", (-0.76, 1.34, 1.68), (0.08, 2.35, 0.68), "mat_blockout_jd_green", col)
    cube_obj("lp_side_panel_r_blockout", (0.76, 1.34, 1.68), (0.08, 2.35, 0.68), "mat_blockout_jd_green", col)

    cab = cube_obj("lp_cab_shell_blockout", (0, -1.12, 2.28), (1.72, 1.62, 1.80), "mat_blockout_jd_green", col)
    bevel_modifier(cab, 0.06, 2)
    cube_obj("lp_cab_glass_front_blockout", (0, -0.26, 2.34), (1.45, 0.08, 1.18), "mat_blockout_glass", col)
    cube_obj("lp_cab_glass_rear_blockout", (0, -1.98, 2.34), (1.45, 0.08, 1.18), "mat_blockout_glass", col)
    cube_obj("lp_cab_glass_l_blockout", (-0.91, -1.12, 2.34), (0.08, 1.34, 1.12), "mat_blockout_glass", col)
    cube_obj("lp_cab_glass_r_blockout", (0.91, -1.12, 2.34), (0.08, 1.34, 1.12), "mat_blockout_glass", col)
    cube_obj("lp_roof_blockout", (0, -1.12, 3.28), (1.92, 1.88, 0.22), "mat_blockout_jd_green", col)

    for x in (-0.82, 0.82):
        cube_obj(f"lp_rear_fender_{side_name(x)}_blockout", (x, -1.72, 1.78), (0.28, 1.55, 0.30), "mat_blockout_jd_green", col)
        cube_obj(f"lp_front_fender_{side_name(x)}_blockout", (x, 1.68, 1.25), (0.24, 0.85, 0.22), "mat_blockout_jd_green", col)


def add_wheels(collections):
    col = collections["wheels"]
    rear_y = -1.525
    front_y = 1.525

    rear_positions = [
        (-1.43, rear_y, 1.04, "rear_l_outer"),
        (-0.96, rear_y, 1.04, "rear_l_inner"),
        (0.96, rear_y, 1.04, "rear_r_inner"),
        (1.43, rear_y, 1.04, "rear_r_outer"),
    ]
    for x, y, z, label in rear_positions:
        cylinder_obj(f"lp_tire_{label}_800_70r38_blockout", (x, y, z), 1.04, 0.42, "mat_blockout_rubber", col)
        cylinder_obj(f"lp_rim_{label}_blockout", (x, y, z), 0.58, 0.45, "mat_blockout_jd_yellow", col, vertices=48)
        cylinder_obj(f"lp_cast_weight_{label}_blockout", (x, y, z), 0.42, 0.08, "mat_blockout_weight", col, vertices=40)

    for x, label in [(-0.92, "front_l"), (0.92, "front_r")]:
        cylinder_obj(f"lp_tire_{label}_blockout", (x, front_y, 0.78), 0.78, 0.36, "mat_blockout_rubber", col)
        cylinder_obj(f"lp_rim_{label}_blockout", (x, front_y, 0.78), 0.42, 0.38, "mat_blockout_jd_yellow", col, vertices=48)
        cylinder_obj(f"empty_wheel_axis_{label}", (x, front_y, 0.78), 0.035, 1.95, "mat_blockout_red", col, vertices=16)


def add_ils(collections):
    col = collections["ils"]
    for x, side in [(-0.55, "l"), (0.55, "r")]:
        cube_obj(f"lp_ils_upper_arm_{side}_blockout", (x, 1.47, 0.98), (0.13, 1.05, 0.09), "mat_blockout_cast_metal", col)
        cube_obj(f"lp_ils_lower_arm_{side}_blockout", (x, 1.47, 0.62), (0.15, 1.15, 0.10), "mat_blockout_cast_metal", col)
        cylinder_obj(f"lp_ils_cylinder_{side}_blockout", (x, 1.16, 0.92), 0.055, 0.78, "mat_blockout_cast_metal", col, axis="Y", vertices=24)
        cube_obj(f"lp_ils_hub_carrier_{side}_blockout", (x * 1.55, 1.525, 0.78), (0.20, 0.32, 0.48), "mat_blockout_cast_metal", col)
        empty_obj(f"empty_ils_upper_arm_{side}_pivot", (x, 0.96, 0.98), col)
        empty_obj(f"empty_ils_lower_arm_{side}_pivot", (x, 0.92, 0.62), col)


def add_rear_hitch(collections):
    col = collections["hitch"]
    cube_obj("lp_rear_hitch_crossbar_blockout", (0, -3.08, 0.82), (1.35, 0.16, 0.16), "mat_blockout_cast_metal", col)
    for x, side in [(-0.45, "l"), (0.45, "r")]:
        cube_obj(f"lp_rear_lower_link_{side}_blockout", (x, -3.12, 0.58), (0.13, 1.05, 0.10), "mat_blockout_cast_metal", col)
        cylinder_obj(f"lp_hitch_cylinder_{side}_blockout", (x, -2.74, 0.96), 0.05, 0.78, "mat_blockout_cast_metal", col, axis="Y", vertices=24)
        empty_obj(f"empty_rear_hitch_{side}_pivot", (x, -2.58, 0.72), col)

    cube_obj("lp_top_link_blockout", (0, -2.92, 1.18), (0.12, 0.82, 0.10), "mat_blockout_cast_metal", col)
    cube_obj("lp_drawbar_oscillating_blockout", (0, -3.18, 0.36), (0.24, 1.10, 0.10), "mat_blockout_weight", col)
    cube_obj("lp_rear_scv_block_5_outputs_blockout", (0.62, -2.54, 1.20), (0.34, 0.18, 0.42), "mat_blockout_dark_metal", col)

    for index in range(5):
        z = 1.03 + index * 0.085
        cylinder_obj(f"lp_scv_quick_coupler_{index + 1}_blockout", (0.43, -2.66, z), 0.035, 0.08, "mat_blockout_cast_metal", col, axis="Y", vertices=16)


def add_weights_and_customs(collections):
    weights = collections["weights"]
    customs = collections["customs"]

    cube_obj("lp_front_weight_carrier_blockout", (0, 3.06, 0.82), (1.25, 0.22, 0.36), "mat_blockout_weight", weights)

    start_x = -0.55
    for index in range(22):
        row = index // 11
        col = index % 11
        x = start_x + col * 0.11
        y = 3.23 + row * 0.16
        cube_obj(f"lp_front_weight_50kg_{index + 1:02d}_blockout", (x, y, 0.88), (0.095, 0.13, 0.52), "mat_blockout_weight", weights)

    cylinder_obj("lp_asm_direct_exhaust_inox_blockout", (0.66, 1.04, 2.55), 0.095, 1.35, "mat_blockout_inox", customs, axis="Z", vertices=32)
    cylinder_obj("lp_asm_exhaust_tip_blockout", (0.66, 1.04, 3.30), 0.115, 0.20, "mat_blockout_inox", customs, axis="Z", vertices=32)
    cube_obj("lp_asm_roof_led_bar_blockout", (0, -0.28, 3.43), (1.28, 0.08, 0.08), "mat_blockout_led", customs)

    for x in (-0.36, 0.36):
        cylinder_obj(f"lp_asm_grille_aux_light_{side_name(x)}_blockout", (x, 2.89, 1.67), 0.12, 0.08, "mat_blockout_led", customs, axis="Y", vertices=32)


def add_interior(collections):
    col = collections["interior"]
    cube_obj("lp_active_seat_ii_base_blockout", (-0.20, -1.25, 1.72), (0.52, 0.48, 0.22), "mat_blockout_dark_metal", col)
    cube_obj("lp_active_seat_ii_back_blockout", (-0.20, -1.44, 2.05), (0.52, 0.12, 0.66), "mat_blockout_dark_metal", col)
    cube_obj("lp_commandarm_console_blockout", (0.46, -1.16, 1.82), (0.34, 0.72, 0.26), "mat_blockout_dark_metal", col)
    cube_obj("lp_g5_display_blockout", (0.48, -0.80, 2.08), (0.34, 0.06, 0.22), "mat_blockout_led", col)
    cylinder_obj("lp_steering_wheel_blockout", (0, -0.56, 1.94), 0.20, 0.04, "mat_blockout_dark_metal", col, axis="Y", vertices=40)
    empty_obj("empty_active_seat_rotation_pivot", (-0.20, -1.25, 1.62), col)
    empty_obj("empty_steering_column_pivot", (0, -0.62, 1.84), col)


def add_lights(collections):
    col = collections["lights"]
    light_points = [
        ("front_headlight_l", -0.42, 2.90, 1.84),
        ("front_headlight_r", 0.42, 2.90, 1.84),
        ("waist_light_l", -0.88, 0.62, 2.12),
        ("waist_light_r", 0.88, 0.62, 2.12),
        ("rear_work_light_l", -0.80, -2.12, 2.22),
        ("rear_work_light_r", 0.80, -2.12, 2.22),
    ]
    for name, x, y, z in light_points:
        cube_obj(f"lp_{name}_blockout", (x, y, z), (0.18, 0.06, 0.10), "mat_blockout_led", col)


def add_ground_and_measuring(collections):
    col = collections["guides"]
    cube_obj("guide_total_length_6_636m", (0, 0, 0.015), (0.06, 6.636, 0.03), "mat_blockout_red", col)
    cube_obj("guide_wheelbase_3_050m", (0.12, 0, 0.045), (0.05, 3.050, 0.04), "mat_blockout_led", col)
    cube_obj("guide_ground_plane", (0, 0, -0.015), (4.20, 7.20, 0.02), "mat_blockout_dark_metal", col)


def side_name(x):
    return "l" if x < 0 else "r"


def setup_scene():
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.render.engine = "CYCLES"

    camera_data = bpy.data.cameras.new("camera_blockout_review")
    camera = bpy.data.objects.new("camera_blockout_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (5.2, -6.8, 3.4)
    camera.rotation_euler = (math.radians(62), 0, math.radians(39))
    bpy.context.scene.camera = camera

    light_data = bpy.data.lights.new("sun_blockout_key", "SUN")
    light = bpy.data.objects.new("sun_blockout_key", light_data)
    light.location = (0, 0, 5)
    light.rotation_euler = (math.radians(45), math.radians(0), math.radians(35))
    bpy.context.scene.collection.objects.link(light)


def main():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    collections = {
        "blockout": ensure_collection("01_blockout_main_shapes", root),
        "wheels": ensure_collection("02_wheels_tires_dual_br", root),
        "ils": ensure_collection("03_ils_front_axle_animation_parts", root),
        "hitch": ensure_collection("04_rear_hitch_hydraulics", root),
        "weights": ensure_collection("05_weights_ballast_br", root),
        "customs": ensure_collection("06_asm_performance_customs", root),
        "interior": ensure_collection("07_cab_interior_commandview", root),
        "lights": ensure_collection("08_lights_factory_and_asm", root),
        "guides": ensure_collection("09_scale_guides", root),
    }

    add_body(collections)
    add_wheels(collections)
    add_ils(collections)
    add_rear_hitch(collections)
    add_weights_and_customs(collections)
    add_interior(collections)
    add_lights(collections)
    add_ground_and_measuring(collections)
    setup_scene()

    print("ASM-8R-PERF-BR blockout created. Save as ASM_8R_PERF_BR_blockout_v001.blend")


if __name__ == "__main__":
    main()

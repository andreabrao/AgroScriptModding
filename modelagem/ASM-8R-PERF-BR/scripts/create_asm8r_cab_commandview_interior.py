"""Create ASM-8R-PERF-BR CommandView cab and interior high-poly base.

Run inside Blender:
  Scripting > Open this file > Run Script

This is an editable high-poly starting point for Production Pass 06:
- cab shell, pillars, doors, glass and mirrors
- ActiveSeat II visual base with rotation pivot
- CommandARM console, joystick, buttons and G5 display
- steering wheel, column, dashboard, pedals and interior camera reference
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_CAB_COMMANDVIEW_INTERIOR"

MATERIALS = {
    "mat_hp_cab_green": (0.02, 0.30, 0.07, 1.0, 0.18, 0.42),
    "mat_hp_cab_glass": (0.16, 0.32, 0.36, 0.42, 0.0, 0.12),
    "mat_hp_interior_dark_plastic": (0.035, 0.037, 0.038, 1.0, 0.0, 0.58),
    "mat_hp_seat_fabric": (0.07, 0.075, 0.070, 1.0, 0.0, 0.80),
    "mat_hp_rubber_floor": (0.018, 0.018, 0.016, 1.0, 0.0, 0.88),
    "mat_hp_screen_g5": (0.02, 0.12, 0.16, 1.0, 0.0, 0.22),
    "mat_hp_bolt_metal": (0.68, 0.66, 0.60, 1.0, 0.86, 0.35),
    "mat_hp_led_soft": (0.80, 0.92, 1.0, 1.0, 0.0, 0.20),
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
            if "screen" in name or "led" in name:
                if "Emission Color" in bsdf.inputs:
                    bsdf.inputs["Emission Color"].default_value = (r, g, b, a)
                if "Emission Strength" in bsdf.inputs:
                    bsdf.inputs["Emission Strength"].default_value = 0.6
        if "glass" in name:
            material.blend_method = "BLEND"
            material.use_screen_refraction = True


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
        major_segments=72,
        minor_segments=16,
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


def add_cab_shell(collection):
    cube_obj("hp_cab_floor_pan", (0.0, -1.12, 1.45), (1.72, 1.58, 0.16), "mat_hp_interior_dark_plastic", collection, bevel=0.020)
    cube_obj("hp_cab_roof_green", (0.0, -1.12, 3.28), (1.94, 1.90, 0.22), "mat_hp_cab_green", collection, bevel=0.050)
    cube_obj("hp_cab_rear_frame", (0.0, -2.02, 2.38), (1.76, 0.12, 1.64), "mat_hp_cab_green", collection, bevel=0.025)
    cube_obj("hp_cab_front_header", (0.0, -0.22, 3.02), (1.68, 0.12, 0.22), "mat_hp_cab_green", collection, bevel=0.020)
    cube_obj("hp_cab_rear_header", (0.0, -2.02, 3.02), (1.68, 0.12, 0.22), "mat_hp_cab_green", collection, bevel=0.020)

    pillar_positions = [
        ("a_l", -0.86, -0.32),
        ("a_r", 0.86, -0.32),
        ("b_l", -0.90, -1.15),
        ("b_r", 0.90, -1.15),
        ("c_l", -0.82, -1.98),
        ("c_r", 0.82, -1.98),
    ]
    for name, x, y in pillar_positions:
        cube_obj(f"hp_cab_pillar_{name}", (x, y, 2.34), (0.10, 0.10, 1.68), "mat_hp_cab_green", collection, bevel=0.020)

    cube_obj("hp_cab_front_glass", (0.0, -0.26, 2.36), (1.42, 0.045, 1.20), "mat_hp_cab_glass", collection, bevel=0.012)
    cube_obj("hp_cab_rear_glass", (0.0, -2.08, 2.34), (1.42, 0.045, 1.16), "mat_hp_cab_glass", collection, bevel=0.012)
    cube_obj("hp_cab_door_l", (-0.94, -1.12, 2.35), (0.08, 1.25, 1.42), "mat_hp_cab_green", collection, bevel=0.018)
    cube_obj("hp_cab_door_r", (0.94, -1.12, 2.35), (0.08, 1.25, 1.42), "mat_hp_cab_green", collection, bevel=0.018)
    cube_obj("hp_cab_glass_door_l", (-0.985, -1.12, 2.42), (0.035, 1.00, 1.02), "mat_hp_cab_glass", collection, bevel=0.010)
    cube_obj("hp_cab_glass_door_r", (0.985, -1.12, 2.42), (0.035, 1.00, 1.02), "mat_hp_cab_glass", collection, bevel=0.010)

    for x, side in [(-1, "l"), (1, "r")]:
        cube_obj(f"hp_door_hinge_upper_{side}", (x * 0.99, -0.54, 2.82), (0.055, 0.12, 0.10), "mat_hp_bolt_metal", collection, bevel=0.006)
        cube_obj(f"hp_door_hinge_lower_{side}", (x * 0.99, -0.54, 2.02), (0.055, 0.12, 0.10), "mat_hp_bolt_metal", collection, bevel=0.006)
        cube_obj(f"hp_door_handle_{side}", (x * 1.02, -1.20, 2.28), (0.040, 0.20, 0.06), "mat_hp_bolt_metal", collection, bevel=0.006)
        empty_obj(f"empty_door_{side}_hinge_pivot", (x * 0.99, -0.54, 2.42), collection)

    pipe_between("hp_windshield_wiper_arm", (-0.42, -0.295, 1.86), (0.22, -0.295, 2.16), 0.012, "mat_hp_bolt_metal", collection, vertices=12)
    cube_obj("hp_windshield_wiper_blade", (0.26, -0.30, 2.17), (0.42, 0.018, 0.035), "mat_hp_rubber_floor", collection, rotation=(0.0, 0.0, math.radians(16)), bevel=0.004)

    for x, side in [(-1, "l"), (1, "r")]:
        pipe_between(f"hp_mirror_arm_{side}", (x * 0.88, -0.48, 2.62), (x * 1.28, -0.30, 2.58), 0.018, "mat_hp_bolt_metal", collection, vertices=16)
        cube_obj(f"hp_side_mirror_{side}", (x * 1.34, -0.26, 2.58), (0.06, 0.28, 0.22), "mat_hp_cab_glass", collection, bevel=0.010)


def add_active_seat(collection):
    cube_obj("hp_active_seat_suspension_base", (-0.18, -1.20, 1.58), (0.46, 0.46, 0.16), "mat_hp_bolt_metal", collection, bevel=0.018)
    pipe_between("hp_active_seat_scissor_l_a", (-0.36, -1.38, 1.62), (0.00, -1.02, 1.78), 0.018, "mat_hp_bolt_metal", collection, vertices=12)
    pipe_between("hp_active_seat_scissor_l_b", (-0.36, -1.02, 1.62), (0.00, -1.38, 1.78), 0.018, "mat_hp_bolt_metal", collection, vertices=12)
    cube_obj("hp_active_seat_cushion", (-0.18, -1.20, 1.82), (0.58, 0.56, 0.18), "mat_hp_seat_fabric", collection, bevel=0.040)
    cube_obj("hp_active_seat_backrest", (-0.18, -1.44, 2.16), (0.58, 0.14, 0.70), "mat_hp_seat_fabric", collection, bevel=0.045)
    cube_obj("hp_active_seat_headrest", (-0.18, -1.50, 2.62), (0.42, 0.12, 0.18), "mat_hp_seat_fabric", collection, bevel=0.030)
    cube_obj("hp_active_seat_left_armrest", (-0.56, -1.18, 2.02), (0.12, 0.50, 0.10), "mat_hp_interior_dark_plastic", collection, bevel=0.020)
    cube_obj("hp_active_seat_right_armrest", (0.18, -1.18, 2.02), (0.12, 0.50, 0.10), "mat_hp_interior_dark_plastic", collection, bevel=0.020)

    for index, x in enumerate((-0.40, -0.28, -0.16, -0.04), start=1):
        cube_obj(f"hp_active_seat_stitch_line_{index}", (x, -1.48, 2.18), (0.010, 0.018, 0.58), "mat_hp_bolt_metal", collection, bevel=0.002)

    empty_obj("empty_active_seat_rotation_pivot", (-0.18, -1.20, 1.62), collection, size=0.28)


def add_commandarm_and_display(collection):
    cube_obj("hp_commandarm_base_console", (0.46, -1.12, 1.76), (0.34, 0.76, 0.22), "mat_hp_interior_dark_plastic", collection, bevel=0.030)
    cube_obj("hp_commandarm_armrest_pad", (0.44, -1.18, 1.98), (0.38, 0.56, 0.12), "mat_hp_seat_fabric", collection, bevel=0.030)
    cylinder_obj("hp_commandarm_joystick_stem", (0.42, -0.90, 2.12), 0.026, 0.18, "mat_hp_bolt_metal", collection, axis="Z", vertices=20)
    cube_obj("hp_commandarm_joystick_grip", (0.42, -0.90, 2.24), (0.12, 0.10, 0.16), "mat_hp_interior_dark_plastic", collection, bevel=0.030)
    cylinder_obj("hp_commandarm_encoder_knob", (0.56, -1.02, 2.08), 0.060, 0.04, "mat_hp_bolt_metal", collection, axis="Z", vertices=28)

    for row in range(3):
        for col in range(4):
            cube_obj(
                f"hp_commandarm_button_r{row + 1}_c{col + 1}",
                (0.34 + col * 0.055, -1.32 + row * 0.075, 2.075),
                (0.038, 0.030, 0.014),
                "mat_hp_bolt_metal",
                collection,
                bevel=0.004,
            )

    cube_obj("hp_g5_display_mount_arm", (0.50, -0.76, 2.04), (0.08, 0.28, 0.06), "mat_hp_bolt_metal", collection, bevel=0.010)
    cube_obj("hp_g5_display_frame", (0.50, -0.58, 2.16), (0.46, 0.055, 0.30), "mat_hp_interior_dark_plastic", collection, bevel=0.020)
    cube_obj("hp_g5_display_screen", (0.50, -0.615, 2.16), (0.38, 0.014, 0.22), "mat_hp_screen_g5", collection, bevel=0.006)
    empty_obj("empty_g5_display_mount", (0.50, -0.76, 2.06), collection, size=0.20)


def add_steering_dashboard_pedals(collection):
    cube_obj("hp_dashboard_upper", (0.0, -0.48, 2.02), (0.82, 0.22, 0.24), "mat_hp_interior_dark_plastic", collection, bevel=0.030)
    cube_obj("hp_dashboard_instrument_screen", (0.0, -0.61, 2.08), (0.34, 0.025, 0.16), "mat_hp_screen_g5", collection, bevel=0.006)
    pipe_between("hp_steering_column_telescopic", (0.0, -0.58, 1.82), (0.0, -0.66, 2.02), 0.040, "mat_hp_bolt_metal", collection, vertices=24)
    torus_obj("hp_steering_wheel_ring", (0.0, -0.72, 2.08), 0.205, 0.020, "mat_hp_interior_dark_plastic", collection, rotation=(math.radians(90), 0, 0))
    cylinder_obj("hp_steering_wheel_hub", (0.0, -0.72, 2.08), 0.055, 0.050, "mat_hp_interior_dark_plastic", collection, axis="Y", vertices=28)

    for angle in (0, 120, 240):
        rad = math.radians(angle)
        pipe_between(
            f"hp_steering_wheel_spoke_{angle}",
            (0.0, -0.72, 2.08),
            (math.cos(rad) * 0.17, -0.72, 2.08 + math.sin(rad) * 0.17),
            0.010,
            "mat_hp_bolt_metal",
            collection,
            vertices=10,
        )

    cube_obj("hp_floor_mat_rubber", (0.0, -0.92, 1.535), (1.18, 0.92, 0.030), "mat_hp_rubber_floor", collection, bevel=0.010)
    cube_obj("hp_pedal_accelerator", (0.24, -0.48, 1.66), (0.12, 0.20, 0.045), "mat_hp_rubber_floor", collection, rotation=(math.radians(-18), 0, 0), bevel=0.008)
    cube_obj("hp_pedal_brake_left", (-0.10, -0.48, 1.66), (0.12, 0.18, 0.045), "mat_hp_rubber_floor", collection, rotation=(math.radians(-18), 0, 0), bevel=0.008)
    cube_obj("hp_pedal_brake_right", (0.04, -0.48, 1.66), (0.12, 0.18, 0.045), "mat_hp_rubber_floor", collection, rotation=(math.radians(-18), 0, 0), bevel=0.008)

    for index, x in enumerate((-0.32, -0.16, 0.16, 0.32), start=1):
        cube_obj(f"hp_dashboard_vent_{index}", (x, -0.62, 2.20), (0.10, 0.020, 0.045), "mat_hp_bolt_metal", collection, bevel=0.004)

    empty_obj("empty_steering_wheel_pivot", (0.0, -0.72, 2.08), collection, size=0.22)
    empty_obj("empty_steering_column_tilt_pivot", (0.0, -0.58, 1.82), collection, size=0.22)
    empty_obj("empty_interior_camera_reference", (-0.16, -1.03, 2.22), collection, size=0.30)


def add_roof_controls_and_lights(collection):
    cube_obj("hp_roof_console_inner", (0.0, -0.88, 3.08), (0.72, 0.42, 0.10), "mat_hp_interior_dark_plastic", collection, bevel=0.020)
    cube_obj("hp_roof_dome_light", (0.0, -0.70, 3.02), (0.22, 0.08, 0.035), "mat_hp_led_soft", collection, bevel=0.006)
    for index, x in enumerate((-0.24, -0.12, 0.12, 0.24), start=1):
        cube_obj(f"hp_roof_button_{index}", (x, -0.96, 3.02), (0.055, 0.035, 0.018), "mat_hp_bolt_metal", collection, bevel=0.004)


def add_guides_and_labels(collection):
    cube_obj("guide_cab_width_1_90m", (0.0, -2.35, 1.40), (1.90, 0.035, 0.035), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_cab_height", (1.08, -1.12, 2.38), (0.035, 0.035, 1.86), "mat_hp_guide_red", collection, bevel=0.0)
    labels = [
        ("label_commandview_cab", (0.0, -2.36, 3.26), "CommandView III cab"),
        ("label_active_seat", (-0.54, -1.54, 2.74), "ActiveSeat II"),
        ("label_commandarm_g5", (0.70, -0.82, 2.50), "CommandARM + G5"),
        ("label_camera_ref", (-0.38, -0.88, 2.36), "Interior camera ref"),
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

    camera_data = bpy.data.cameras.new("camera_cab_interior_review")
    camera = bpy.data.objects.new("camera_cab_interior_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (3.2, -4.6, 3.0)
    camera.rotation_euler = (math.radians(62), 0, math.radians(36))
    bpy.context.scene.camera = camera

    sun_data = bpy.data.lights.new("sun_cab_key", "SUN")
    sun = bpy.data.objects.new("sun_cab_key", sun_data)
    sun.rotation_euler = (math.radians(48), 0, math.radians(32))
    bpy.context.scene.collection.objects.link(sun)


def main():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    shell_col = ensure_collection("01_cab_shell_glass_doors", root)
    seat_col = ensure_collection("02_active_seat_ii", root)
    command_col = ensure_collection("03_commandarm_g5_controls", root)
    steering_col = ensure_collection("04_steering_dashboard_pedals", root)
    roof_col = ensure_collection("05_roof_controls_lights", root)
    guide_col = ensure_collection("06_guides_and_labels", root)

    add_cab_shell(shell_col)
    add_active_seat(seat_col)
    add_commandarm_and_display(command_col)
    add_steering_dashboard_pedals(steering_col)
    add_roof_controls_and_lights(roof_col)
    add_guides_and_labels(guide_col)
    setup_scene()

    print("ASM-8R-PERF-BR CommandView cab/interior base created.")
    print("Save as ASM_8R_PERF_BR_highpoly_cab_interior_v001.blend")


if __name__ == "__main__":
    main()

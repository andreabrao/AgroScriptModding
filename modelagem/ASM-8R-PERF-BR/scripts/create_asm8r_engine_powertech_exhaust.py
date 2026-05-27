"""Create ASM-8R-PERF-BR PowerTech 9.0 L engine and ASM exhaust base.

Run inside Blender:
  Scripting > Open this file > Run Script

This is an editable high-poly starting point for Production Pass 04:
- 6-cylinder PowerTech-style engine block
- head, valve cover, oil pan and casting ribs
- common rail, injectors and injector lines
- turbo-aftercooler system
- radiator, fan, belts and hoses
- ASM stainless direct exhaust with smoke pivot
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_ENGINE_POWERTECH_EXHAUST"

MATERIALS = {
    "mat_hp_engine_cast": (0.34, 0.35, 0.34, 1.0, 0.70, 0.62),
    "mat_hp_engine_dark": (0.08, 0.075, 0.065, 1.0, 0.55, 0.76),
    "mat_hp_common_rail": (0.62, 0.60, 0.54, 1.0, 0.88, 0.35),
    "mat_hp_stainless_exhaust": (0.74, 0.72, 0.68, 1.0, 0.92, 0.30),
    "mat_hp_rubber_hose": (0.018, 0.018, 0.016, 1.0, 0.0, 0.86),
    "mat_hp_radiator_core": (0.04, 0.045, 0.045, 1.0, 0.50, 0.70),
    "mat_hp_bolt_metal": (0.68, 0.66, 0.60, 1.0, 0.90, 0.34),
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

    direction = (dx / length, dy / length, dz / length)
    quat = direction_to_quaternion(direction)
    obj.rotation_euler = quat.to_euler()
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    shade(obj)
    return obj


def direction_to_quaternion(direction):
    # Blender cylinder local axis is Z before transform.
    import mathutils

    vector = mathutils.Vector(direction)
    return vector.to_track_quat("Z", "Y")


def empty_obj(name, location, collection, size=0.25):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = size
    obj.location = location
    collection.objects.link(obj)
    return obj


def add_bolts_on_box(prefix, x, y, z_values, collection):
    for row, z in enumerate(z_values):
        for index, y_offset in enumerate((-0.56, -0.28, 0.0, 0.28, 0.56)):
            cylinder_obj(
                f"hp_{prefix}_bolt_r{row + 1}_{index + 1}",
                (x, y + y_offset, z),
                0.018,
                0.040,
                "mat_hp_bolt_metal",
                collection,
                axis="X",
                vertices=16,
            )


def add_engine_block(collection):
    cube_obj("hp_powertech_9l_engine_block", (0.0, 0.88, 1.22), (0.92, 1.46, 0.72), "mat_hp_engine_cast", collection, bevel=0.045)
    cube_obj("hp_powertech_9l_cylinder_head", (0.0, 0.88, 1.68), (0.86, 1.34, 0.24), "mat_hp_engine_cast", collection, bevel=0.035)
    cube_obj("hp_powertech_9l_valve_cover", (0.0, 0.88, 1.86), (0.72, 1.20, 0.18), "mat_hp_engine_dark", collection, bevel=0.030)
    cube_obj("hp_powertech_9l_oil_pan", (0.0, 0.88, 0.78), (0.78, 1.24, 0.26), "mat_hp_engine_dark", collection, bevel=0.035)
    cube_obj("hp_engine_front_flange", (0.0, 1.68, 1.18), (0.86, 0.12, 0.58), "mat_hp_engine_cast", collection, bevel=0.025)
    cube_obj("hp_engine_rear_flange_transmission", (0.0, 0.07, 1.18), (0.90, 0.12, 0.62), "mat_hp_engine_cast", collection, bevel=0.025)

    for index in range(6):
        y = 0.30 + index * 0.23
        cube_obj(f"hp_engine_casting_rib_left_{index + 1}", (-0.49, y, 1.25), (0.055, 0.045, 0.60), "mat_hp_engine_cast", collection, bevel=0.012)
        cube_obj(f"hp_engine_casting_rib_right_{index + 1}", (0.49, y, 1.25), (0.055, 0.045, 0.60), "mat_hp_engine_cast", collection, bevel=0.012)
        cylinder_obj(f"hp_cylinder_port_marker_{index + 1}", (-0.53, y, 1.48), 0.045, 0.035, "mat_hp_engine_dark", collection, axis="X", vertices=24)

    add_bolts_on_box("engine_left_side_cover", -0.54, 0.88, (1.02, 1.42), collection)
    add_bolts_on_box("engine_right_side_cover", 0.54, 0.88, (1.02, 1.42), collection)
    empty_obj("empty_engine_mount_front", (0.0, 1.58, 0.86), collection)
    empty_obj("empty_engine_mount_rear", (0.0, 0.14, 0.86), collection)


def add_common_rail(collection):
    cylinder_obj("hp_common_rail_tube", (-0.58, 0.88, 1.72), 0.028, 1.20, "mat_hp_common_rail", collection, axis="Y", vertices=24)
    cube_obj("hp_common_rail_bracket_front", (-0.58, 1.38, 1.66), (0.06, 0.05, 0.16), "mat_hp_common_rail", collection, bevel=0.010)
    cube_obj("hp_common_rail_bracket_rear", (-0.58, 0.38, 1.66), (0.06, 0.05, 0.16), "mat_hp_common_rail", collection, bevel=0.010)

    for index in range(6):
        y = 0.30 + index * 0.23
        cylinder_obj(f"hp_injector_{index + 1:02d}", (-0.34, y, 1.75), 0.026, 0.12, "mat_hp_common_rail", collection, axis="Z", vertices=20)
        pipe_between(
            f"hp_injector_line_{index + 1:02d}",
            (-0.56, y, 1.72),
            (-0.36, y, 1.77),
            0.010,
            "mat_hp_common_rail",
            collection,
            vertices=12,
        )


def add_turbo_aftercooler(collection):
    torus_obj("hp_turbo_cold_housing", (0.62, 0.58, 1.58), 0.145, 0.045, "mat_hp_common_rail", collection, rotation=(math.radians(90), 0, 0))
    torus_obj("hp_turbo_hot_housing", (0.62, 0.42, 1.52), 0.135, 0.048, "mat_hp_engine_dark", collection, rotation=(math.radians(90), 0, 0))
    cylinder_obj("hp_turbo_center_core", (0.62, 0.50, 1.55), 0.065, 0.18, "mat_hp_engine_dark", collection, axis="Y", vertices=32)
    empty_obj("empty_turbo_center_pivot", (0.62, 0.50, 1.55), collection)

    cube_obj("hp_exhaust_manifold_6cyl", (0.52, 0.88, 1.47), (0.14, 1.20, 0.16), "mat_hp_engine_dark", collection, bevel=0.020)
    for index in range(6):
        y = 0.30 + index * 0.23
        pipe_between(f"hp_exhaust_runner_{index + 1:02d}", (0.44, y, 1.46), (0.56, y, 1.48), 0.020, "mat_hp_engine_dark", collection, vertices=14)

    cube_obj("hp_aftercooler_box", (0.0, 2.02, 1.42), (1.02, 0.16, 0.68), "mat_hp_radiator_core", collection, bevel=0.018)
    cube_obj("hp_radiator_core_front", (0.0, 2.20, 1.38), (1.08, 0.14, 0.82), "mat_hp_radiator_core", collection, bevel=0.018)
    for index in range(9):
        x = -0.44 + index * 0.11
        cube_obj(f"hp_radiator_vertical_fin_{index + 1:02d}", (x, 2.285, 1.38), (0.012, 0.025, 0.76), "mat_hp_bolt_metal", collection, bevel=0.002)

    pipe_between("hp_turbo_to_aftercooler_pipe", (0.62, 0.58, 1.58), (0.40, 1.98, 1.66), 0.045, "mat_hp_common_rail", collection, vertices=24)
    pipe_between("hp_aftercooler_to_intake_pipe", (-0.34, 2.00, 1.56), (-0.48, 1.10, 1.58), 0.050, "mat_hp_common_rail", collection, vertices=24)
    cube_obj("hp_intake_manifold", (-0.46, 0.88, 1.54), (0.14, 1.16, 0.16), "mat_hp_engine_cast", collection, bevel=0.018)

    for name, location in [
        ("hp_clamp_turbo_pipe", (0.54, 1.02, 1.61)),
        ("hp_clamp_aftercooler_in", (0.40, 1.90, 1.65)),
        ("hp_clamp_aftercooler_out", (-0.34, 1.90, 1.56)),
    ]:
        torus_obj(name, location, 0.052, 0.006, "mat_hp_bolt_metal", collection, rotation=(math.radians(90), 0, 0))


def add_cooling_front(collection):
    cylinder_obj("hp_fan_pulley_center", (0.0, 1.76, 1.32), 0.12, 0.08, "mat_hp_bolt_metal", collection, axis="Y", vertices=40)
    empty_obj("empty_fan_rotation_pivot", (0.0, 1.76, 1.32), collection)
    for index in range(8):
        angle = math.tau * index / 8
        x = math.cos(angle) * 0.18
        z = 1.32 + math.sin(angle) * 0.18
        blade = cube_obj(
            f"hp_fan_blade_{index + 1:02d}",
            (x * 0.5, 1.72, z),
            (0.08, 0.035, 0.30),
            "mat_hp_engine_dark",
            collection,
            rotation=(0.0, 0.0, angle),
            bevel=0.010,
        )
        blade["asm_pivot"] = "empty_fan_rotation_pivot"

    cylinder_obj("hp_crank_pulley", (0.0, 1.70, 0.98), 0.13, 0.06, "mat_hp_engine_dark", collection, axis="Y", vertices=40)
    cylinder_obj("hp_upper_pulley", (-0.20, 1.70, 1.62), 0.08, 0.05, "mat_hp_engine_dark", collection, axis="Y", vertices=32)
    pipe_between("hp_belt_left_run", (-0.20, 1.70, 1.62), (0.0, 1.70, 0.98), 0.018, "mat_hp_rubber_hose", collection, vertices=12)
    pipe_between("hp_belt_right_run", (0.20, 1.70, 1.62), (0.0, 1.70, 0.98), 0.018, "mat_hp_rubber_hose", collection, vertices=12)
    pipe_between("hp_upper_radiator_hose", (-0.36, 1.84, 1.70), (-0.44, 1.22, 1.64), 0.038, "mat_hp_rubber_hose", collection, vertices=20)
    pipe_between("hp_lower_radiator_hose", (0.34, 1.88, 1.04), (0.42, 1.18, 0.96), 0.045, "mat_hp_rubber_hose", collection, vertices=20)


def add_asm_exhaust(collection):
    pipe_between("hp_asm_exhaust_downpipe_from_turbo", (0.66, 0.42, 1.54), (0.72, 0.78, 1.92), 0.055, "mat_hp_stainless_exhaust", collection, vertices=32)
    cylinder_obj("hp_asm_direct_exhaust_vertical_inox", (0.72, 0.92, 2.55), 0.085, 1.30, "mat_hp_stainless_exhaust", collection, axis="Z", vertices=48)
    cylinder_obj("hp_asm_exhaust_tip_chamfer_base", (0.72, 0.92, 3.23), 0.105, 0.18, "mat_hp_stainless_exhaust", collection, axis="Z", vertices=48)
    cube_obj("hp_asm_exhaust_chamfer_cut_marker", (0.72, 0.92, 3.34), (0.24, 0.04, 0.08), "mat_hp_engine_dark", collection, rotation=(math.radians(0), math.radians(0), math.radians(18)), bevel=0.004)
    torus_obj("hp_asm_exhaust_lower_clamp", (0.72, 0.92, 2.02), 0.090, 0.008, "mat_hp_bolt_metal", collection)
    torus_obj("hp_asm_exhaust_upper_clamp", (0.72, 0.92, 2.86), 0.090, 0.008, "mat_hp_bolt_metal", collection)
    cube_obj("hp_asm_exhaust_support_bracket_lower", (0.62, 0.92, 2.02), (0.18, 0.045, 0.08), "mat_hp_bolt_metal", collection, bevel=0.008)
    cube_obj("hp_asm_exhaust_support_bracket_upper", (0.62, 0.92, 2.86), (0.18, 0.045, 0.08), "mat_hp_bolt_metal", collection, bevel=0.008)
    empty_obj("empty_exhaust_smoke_pivot", (0.72, 0.92, 3.38), collection, size=0.22)

    for index, z in enumerate((2.18, 2.46, 2.74), start=1):
        torus_obj(f"hp_asm_exhaust_weld_bead_{index}", (0.72, 0.92, z), 0.086, 0.004, "mat_hp_engine_dark", collection)


def add_guides(collection):
    cube_obj("guide_engine_envelope_length", (0.0, 0.92, 0.35), (0.06, 1.92, 0.04), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_engine_centerline", (0.0, 0.92, 1.36), (0.035, 1.92, 0.035), "mat_hp_guide_red", collection, bevel=0.0)
    cube_obj("guide_exhaust_height_asm", (0.72, 0.92, 1.95), (0.04, 0.04, 2.86), "mat_hp_guide_red", collection, bevel=0.0)

    labels = [
        ("label_powertech_9l", (0.0, 0.42, 2.12), "PowerTech 9.0 L - 6 cyl"),
        ("label_common_rail", (-0.74, 0.84, 1.96), "Common Rail"),
        ("label_turbo_aftercooler", (0.46, 1.70, 2.02), "Turbo-Aftercooler"),
        ("label_asm_exhaust", (0.92, 0.92, 3.38), "ASM direct inox exhaust"),
    ]
    for name, location, text in labels:
        curve = bpy.data.curves.new(name, "FONT")
        curve.body = text
        curve.size = 0.11
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

    camera_data = bpy.data.cameras.new("camera_engine_review")
    camera = bpy.data.objects.new("camera_engine_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (3.5, -3.4, 2.8)
    camera.rotation_euler = (math.radians(63), 0, math.radians(42))
    bpy.context.scene.camera = camera

    sun_data = bpy.data.lights.new("sun_engine_key", "SUN")
    sun = bpy.data.objects.new("sun_engine_key", sun_data)
    sun.rotation_euler = (math.radians(48), 0, math.radians(36))
    bpy.context.scene.collection.objects.link(sun)


def main():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    block_col = ensure_collection("01_powertech_9l_block_head", root)
    fuel_col = ensure_collection("02_common_rail_injection", root)
    turbo_col = ensure_collection("03_turbo_aftercooler_radiator", root)
    exhaust_col = ensure_collection("04_asm_direct_exhaust", root)
    guide_col = ensure_collection("05_guides_and_labels", root)

    add_engine_block(block_col)
    add_common_rail(fuel_col)
    add_turbo_aftercooler(turbo_col)
    add_cooling_front(turbo_col)
    add_asm_exhaust(exhaust_col)
    add_guides(guide_col)
    setup_scene()

    print("ASM-8R-PERF-BR PowerTech engine and ASM exhaust base created.")
    print("Save as ASM_8R_PERF_BR_highpoly_engine_v001.blend")


if __name__ == "__main__":
    main()

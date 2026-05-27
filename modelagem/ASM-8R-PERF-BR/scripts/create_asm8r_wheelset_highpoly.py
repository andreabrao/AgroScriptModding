"""Create the ASM-8R-PERF-BR high-poly wheelset base in Blender.

Run inside Blender:
  Scripting > Open this file > Run Script

This script creates a procedural high-poly starting point for:
- rear 800/70R38 dual tires
- front wide tires
- yellow rims
- hubs, bolts, rear cast weights and dual spacers

It is intentionally procedural and editable. It is not the final game-ready mesh.
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_WHEELSET_HIGHPOLY"

REAR_RADIUS = 1.0425
REAR_WIDTH = 0.800
REAR_RIM_RADIUS = 0.585
FRONT_RADIUS = 0.820
FRONT_WIDTH = 0.650
FRONT_RIM_RADIUS = 0.455

REAR_Y = -1.525
FRONT_Y = 1.525
REAR_Z = REAR_RADIUS
FRONT_Z = FRONT_RADIUS

MATERIALS = {
    "mat_hp_tire_rubber": (0.015, 0.014, 0.012, 1.0, 0.0, 0.84),
    "mat_hp_rim_jd_yellow": (0.95, 0.70, 0.05, 1.0, 0.18, 0.42),
    "mat_hp_hub_dark_metal": (0.18, 0.18, 0.17, 1.0, 0.70, 0.50),
    "mat_hp_cast_weight": (0.08, 0.08, 0.075, 1.0, 0.82, 0.76),
    "mat_hp_bolt_metal": (0.72, 0.70, 0.64, 1.0, 0.86, 0.36),
    "mat_hp_guide_red": (0.80, 0.04, 0.03, 1.0, 0.0, 0.50),
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


def shade_and_weight(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth()
    except RuntimeError:
        pass
    obj.select_set(False)
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def add_bevel(obj, width, segments):
    bevel = obj.modifiers.new("hp_bevel", "BEVEL")
    bevel.width = width
    bevel.segments = segments
    bevel.affect = "EDGES"
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def torus_obj(name, location, tire_radius, tire_width, material_name, collection):
    minor_radius = tire_width * 0.34
    major_radius = max(tire_radius - minor_radius, 0.10)
    bpy.ops.mesh.primitive_torus_add(
        major_segments=144,
        minor_segments=24,
        major_radius=major_radius,
        minor_radius=minor_radius,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler[1] = math.radians(90)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    shade_and_weight(obj)
    return obj


def cylinder_obj(name, location, radius, depth, material_name, collection, axis="X", vertices=96):
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
    shade_and_weight(obj)
    return obj


def cube_obj(name, location, scale, material_name, collection, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    add_bevel(obj, min(scale) * 0.18, 2)
    return obj


def empty_obj(name, location, collection, size=0.32):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = size
    obj.location = location
    collection.objects.link(obj)
    return obj


def create_tread_lugs(prefix, center, tire_radius, tire_width, count, collection, mirrored=False):
    cx, cy, cz = center
    tread_radius = tire_radius + 0.035
    lug_height = tire_radius * 0.070
    lug_depth = tire_radius * 0.090
    lug_width = tire_width * 0.46
    center_gap = tire_width * 0.075

    for index in range(count):
        angle = (math.tau / count) * index
        radial_y = math.cos(angle)
        radial_z = math.sin(angle)
        y = cy + radial_y * tread_radius
        z = cz + radial_z * tread_radius
        x_offset = (center_gap + lug_width * 0.52)
        slant = math.radians(24 if (index + (1 if mirrored else 0)) % 2 == 0 else -24)

        for side, sign in [("inner", -1), ("outer", 1)]:
            x = cx + sign * x_offset
            rotation = (angle, 0.0, sign * slant)
            lug = cube_obj(
                f"hp_{prefix}_tread_{side}_{index + 1:02d}",
                (x, y, z),
                (lug_width, lug_depth, lug_height),
                "mat_hp_tire_rubber",
                collection,
                rotation=rotation,
            )
            lug["asm_note"] = "Tread lug for high-poly bake. Refine shape before final."


def create_sidewall_ribs(prefix, center, tire_radius, tire_width, count, collection):
    cx, cy, cz = center
    for face, x in [("left", cx - tire_width * 0.52), ("right", cx + tire_width * 0.52)]:
        for index in range(count):
            angle = (math.tau / count) * index
            y = cy + math.cos(angle) * (tire_radius * 0.82)
            z = cz + math.sin(angle) * (tire_radius * 0.82)
            rib = cube_obj(
                f"hp_{prefix}_sidewall_rib_{face}_{index + 1:02d}",
                (x, y, z),
                (0.030, tire_radius * 0.060, tire_radius * 0.018),
                "mat_hp_tire_rubber",
                collection,
                rotation=(angle, 0.0, 0.0),
            )
            rib["asm_note"] = "Sidewall rib placeholder. Replace with lettering/detail sculpt."


def create_bolts(prefix, center, radius, face_x, count, collection):
    _, cy, cz = center
    for index in range(count):
        angle = (math.tau / count) * index
        y = cy + math.cos(angle) * radius
        z = cz + math.sin(angle) * radius
        bolt = cylinder_obj(
            f"hp_{prefix}_bolt_{index + 1:02d}",
            (face_x, y, z),
            0.035,
            0.045,
            "mat_hp_bolt_metal",
            collection,
            axis="X",
            vertices=20,
        )
        bolt.rotation_euler[0] = angle


def create_rim(prefix, center, rim_radius, width, collection, heavy_rear=False):
    cx, cy, cz = center
    cylinder_obj(f"hp_{prefix}_rim_outer_yellow", center, rim_radius, width * 0.58, "mat_hp_rim_jd_yellow", collection, vertices=128)
    cylinder_obj(f"hp_{prefix}_rim_inner_shadow", center, rim_radius * 0.72, width * 0.62, "mat_hp_hub_dark_metal", collection, vertices=96)
    cylinder_obj(f"hp_{prefix}_hub_center", center, rim_radius * 0.30, width * 0.72, "mat_hp_hub_dark_metal", collection, vertices=64)

    face_x = cx + width * 0.36
    create_bolts(prefix, center, rim_radius * 0.46, face_x, 10 if heavy_rear else 8, collection)

    if heavy_rear:
        cylinder_obj(
            f"hp_{prefix}_cast_weight_disc_outer",
            (cx + width * 0.46, cy, cz),
            rim_radius * 0.64,
            0.12,
            "mat_hp_cast_weight",
            collection,
            vertices=96,
        )
        cylinder_obj(
            f"hp_{prefix}_cast_weight_disc_inner",
            (cx - width * 0.46, cy, cz),
            rim_radius * 0.58,
            0.10,
            "mat_hp_cast_weight",
            collection,
            vertices=96,
        )


def create_wheel(prefix, center, tire_radius, tire_width, rim_radius, collection, lug_count, rear=False, mirrored=False):
    tire = torus_obj(f"hp_{prefix}_tire", center, tire_radius, tire_width, "mat_hp_tire_rubber", collection)
    tire["asm_size"] = "800/70R38" if rear else "650/60R34 visual reference"
    tire["asm_role"] = "rear dual Performance BR" if rear else "front wide ILS"

    create_tread_lugs(prefix, center, tire_radius, tire_width, lug_count, collection, mirrored=mirrored)
    create_sidewall_ribs(prefix, center, tire_radius, tire_width, 28 if rear else 22, collection)
    create_rim(prefix, center, rim_radius, tire_width, collection, heavy_rear=rear)
    empty_obj(f"empty_{prefix}_wheel_axis", center, collection)


def create_dual_spacers(collection):
    for side, sign in [("l", -1), ("r", 1)]:
        x = sign * 1.195
        cylinder_obj(
            f"hp_rear_dual_spacer_{side}",
            (x, REAR_Y, REAR_Z),
            REAR_RIM_RADIUS * 0.36,
            0.42,
            "mat_hp_hub_dark_metal",
            collection,
            vertices=64,
        )


def create_guides(collection):
    cube_obj(
        "guide_rear_outer_width_performance_br",
        (0.0, REAR_Y, 0.04),
        (3.28, 0.045, 0.045),
        "mat_hp_guide_red",
        collection,
    )
    cube_obj(
        "guide_front_track_width",
        (0.0, FRONT_Y, 0.04),
        (2.10, 0.045, 0.045),
        "mat_hp_guide_red",
        collection,
    )
    cube_obj(
        "guide_wheelbase_3_050m",
        (0.0, 0.0, 0.08),
        (0.06, 3.050, 0.05),
        "mat_hp_guide_red",
        collection,
    )


def add_labels(collection):
    labels = [
        ("label_rear_size_800_70R38", (-1.65, REAR_Y - 0.55, 2.20), "Rear dual 800/70R38"),
        ("label_front_wide_ils", (-1.08, FRONT_Y + 0.45, 1.75), "Front wide ILS tire"),
        ("label_performance_br_weighted", (0.0, -2.40, 2.45), "ASM Performance BR - weighted wheelset"),
    ]
    for name, location, text in labels:
        curve = bpy.data.curves.new(name, "FONT")
        curve.body = text
        curve.size = 0.12
        curve.align_x = "CENTER"
        obj = bpy.data.objects.new(name, curve)
        obj.location = location
        obj.rotation_euler[0] = math.radians(72)
        obj.data.materials.append(mat("mat_hp_guide_red"))
        collection.objects.link(obj)


def setup_scene():
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.context.scene.render.engine = "CYCLES"

    camera_data = bpy.data.cameras.new("camera_wheelset_review")
    camera = bpy.data.objects.new("camera_wheelset_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (4.6, -5.4, 3.0)
    camera.rotation_euler = (math.radians(62), 0, math.radians(39))
    bpy.context.scene.camera = camera

    sun_data = bpy.data.lights.new("sun_wheelset_key", "SUN")
    sun = bpy.data.objects.new("sun_wheelset_key", sun_data)
    sun.rotation_euler = (math.radians(50), 0, math.radians(35))
    bpy.context.scene.collection.objects.link(sun)


def main():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    rear_collection = ensure_collection("01_rear_dual_wheels_800_70r38", root)
    front_collection = ensure_collection("02_front_wheels_wide_ils", root)
    helper_collection = ensure_collection("03_bake_helpers_and_guides", root)

    rear_positions = [
        ("rear_l_outer", (-1.43, REAR_Y, REAR_Z), False),
        ("rear_l_inner", (-0.96, REAR_Y, REAR_Z), True),
        ("rear_r_inner", (0.96, REAR_Y, REAR_Z), False),
        ("rear_r_outer", (1.43, REAR_Y, REAR_Z), True),
    ]
    for prefix, center, mirrored in rear_positions:
        create_wheel(prefix, center, REAR_RADIUS, REAR_WIDTH, REAR_RIM_RADIUS, rear_collection, 46, rear=True, mirrored=mirrored)

    for prefix, center, mirrored in [
        ("front_l", (-0.92, FRONT_Y, FRONT_Z), False),
        ("front_r", (0.92, FRONT_Y, FRONT_Z), True),
    ]:
        create_wheel(prefix, center, FRONT_RADIUS, FRONT_WIDTH, FRONT_RIM_RADIUS, front_collection, 38, rear=False, mirrored=mirrored)

    create_dual_spacers(rear_collection)
    create_guides(helper_collection)
    add_labels(helper_collection)
    setup_scene()

    print("ASM-8R-PERF-BR high-poly wheelset base created.")
    print("Save as ASM_8R_PERF_BR_highpoly_wheels_v001.blend")


if __name__ == "__main__":
    main()

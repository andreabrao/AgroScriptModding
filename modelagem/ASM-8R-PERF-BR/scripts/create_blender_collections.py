"""Create the initial Blender collection hierarchy for ASM-8R-PERF-BR.

Run inside Blender:
  Text Editor > Open > Run Script
"""

import bpy

PROJECT = "ASM_8R_PERF_BR"

COLLECTIONS = {
    "00_reference": [],
    "01_blockout": [],
    "02_high_poly": [
        "body",
        "engine_powertech_9l",
        "chassis_transmission",
        "ils_front_axle",
        "rear_hitch_hydraulics",
        "wheels_tires",
        "cab_exterior",
        "cab_interior",
        "lights",
        "weights",
        "asm_customs",
    ],
    "03_game_ready": ["lod0", "lod1", "lod2", "collision"],
    "04_bake": ["cages", "low_targets", "high_sources"],
    "05_textures": [],
    "06_export_i3d": [],
}

EMPTY_OBJECTS = [
    "vehicle_root",
    "body_root",
    "chassis_root",
    "engine_root",
    "cab_root",
    "cab_interior_root",
    "wheel_front_l",
    "wheel_front_r",
    "wheel_rear_l_outer",
    "wheel_rear_l_inner",
    "wheel_rear_r_outer",
    "wheel_rear_r_inner",
    "ils_front_axle",
    "rear_hitch_root",
    "front_weight_root",
    "lights_root",
]

MATERIALS = {
    "mat_jd_green_clearcoat": (0.02, 0.34, 0.08, 1.0),
    "mat_jd_yellow_rims": (0.95, 0.72, 0.08, 1.0),
    "mat_chassis_dark_metal": (0.17, 0.19, 0.20, 1.0),
    "mat_engine_cast_metal": (0.38, 0.40, 0.41, 1.0),
    "mat_black_rubber": (0.01, 0.01, 0.01, 1.0),
    "mat_cab_glass": (0.20, 0.35, 0.38, 0.35),
    "mat_led_lens": (0.85, 0.92, 1.0, 0.75),
    "mat_stainless_exhaust": (0.76, 0.74, 0.70, 1.0),
    "mat_cast_iron_weights": (0.12, 0.12, 0.11, 1.0),
    "mat_asm_decals": (1.0, 1.0, 1.0, 1.0),
}


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
        principled = material.node_tree.nodes.get("Principled BSDF")
        if principled:
            principled.inputs["Base Color"].default_value = color
            principled.inputs["Roughness"].default_value = 0.45
            principled.inputs["Metallic"].default_value = 0.0


def create_empties(parent_collection):
    for index, name in enumerate(EMPTY_OBJECTS):
        empty = bpy.data.objects.get(name)
        if empty is None:
            empty = bpy.data.objects.new(name, None)
            empty.empty_display_type = "PLAIN_AXES"
            empty.empty_display_size = 0.35
            empty.location = (0.0, index * 0.15, 0.0)
            parent_collection.objects.link(empty)


def main():
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0

    root = ensure_collection(PROJECT)
    for collection_name, children in COLLECTIONS.items():
        collection = ensure_collection(collection_name, root)
        for child_name in children:
            ensure_collection(child_name, collection)

    export_collection = bpy.data.collections.get("06_export_i3d") or root
    create_empties(export_collection)
    create_materials()

    print(f"{PROJECT}: collection hierarchy created.")


if __name__ == "__main__":
    main()

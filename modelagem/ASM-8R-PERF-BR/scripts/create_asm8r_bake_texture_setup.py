"""Create ASM-8R-PERF-BR low-poly, UV, bake and texture planning setup.

Run inside Blender:
  Scripting > Open this file > Run Script

This script does not unwrap the tractor automatically. It creates a clean
production scene with collections, atlas boards, LOD guides, bake cages and
material placeholders for Production Pass 08.
"""

import bpy

PROJECT = "ASM_8R_PERF_BR_PASS08_BAKE_TEXTURES"

MATERIALS = {
    "mat_guide_lod0_green": (0.02, 0.30, 0.07, 1.0, 0.18, 0.46),
    "mat_guide_lod1_yellow": (0.95, 0.74, 0.05, 1.0, 0.10, 0.42),
    "mat_guide_lod2_gray": (0.48, 0.50, 0.48, 1.0, 0.72, 0.38),
    "mat_guide_collision": (0.85, 0.12, 0.05, 0.42, 0.00, 0.50),
    "mat_guide_cage_blue": (0.10, 0.35, 0.82, 0.30, 0.00, 0.30),
    "mat_atlas_body": (0.03, 0.32, 0.08, 1.0, 0.15, 0.45),
    "mat_atlas_engine": (0.40, 0.42, 0.40, 1.0, 0.80, 0.35),
    "mat_atlas_wheels": (0.06, 0.055, 0.05, 1.0, 0.00, 0.82),
    "mat_atlas_interior": (0.04, 0.045, 0.045, 1.0, 0.00, 0.65),
    "mat_atlas_lights": (0.72, 0.90, 1.00, 1.0, 0.05, 0.18),
    "mat_atlas_decals": (0.94, 0.94, 0.90, 1.0, 0.00, 0.50),
    "mat_text_white": (0.92, 0.92, 0.88, 1.0, 0.00, 0.55),
}

ATLASES = [
    ("asm8r_body_4k", "body, cab, hood, grille, decals", "mat_atlas_body"),
    ("asm8r_engine_chassis_4k", "engine, chassis, e23, ILS, hitch", "mat_atlas_engine"),
    ("asm8r_wheels_tires_4k", "tires, rims, wheel weights", "mat_atlas_wheels"),
    ("asm8r_interior_4k", "CommandView III, seat, CommandARM, G5", "mat_atlas_interior"),
    ("asm8r_lights_2k", "LED lenses, reflectors, emissive", "mat_atlas_lights"),
    ("asm8r_decals_2k", "logos, warnings, labels, ASM plates", "mat_atlas_decals"),
]

MAPS = ["baseColor", "normal", "metallic", "roughness", "glossiness", "dirtWear", "emissive"]


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
            if "lights" in name:
                if "Emission Color" in bsdf.inputs:
                    bsdf.inputs["Emission Color"].default_value = (r, g, b, a)
                if "Emission Strength" in bsdf.inputs:
                    bsdf.inputs["Emission Strength"].default_value = 0.4
        if a < 1.0:
            material.blend_method = "BLEND"


def mat(name):
    return bpy.data.materials[name]


def link_to(collection, obj):
    for current in obj.users_collection:
        current.objects.unlink(obj)
    collection.objects.link(obj)


def shade(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)


def add_cube(name, collection, location, scale, material_name):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    return obj


def add_plane(name, collection, location, scale, material_name):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    return obj


def add_text(name, collection, text, location, size=0.18):
    bpy.ops.object.text_add(location=location, rotation=(1.5708, 0.0, 0.0))
    obj = bpy.context.object
    obj.name = name
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.materials.append(mat("mat_text_white"))
    link_to(collection, obj)
    return obj


def add_empty(name, collection, location):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=location)
    obj = bpy.context.object
    obj.name = name
    obj.empty_display_size = 0.35
    link_to(collection, obj)
    return obj


def create_lod_guides(root):
    lod_col = ensure_collection("00_LOD_AND_COLLISION_GUIDES", root)

    rows = [
        ("lod0_full_game_ready_proxy", "mat_guide_lod0_green", -2.4, 1.00, "LOD0"),
        ("lod1_mid_distance_proxy", "mat_guide_lod1_yellow", 0.0, 0.72, "LOD1"),
        ("lod2_far_distance_proxy", "mat_guide_lod2_gray", 2.1, 0.48, "LOD2"),
    ]

    for name, material, x, factor, label in rows:
        body = add_cube(f"{name}_body", lod_col, (x, 0.0, 1.15 * factor), (2.8 * factor, 1.0 * factor, 0.8 * factor), material)
        cab = add_cube(f"{name}_cab", lod_col, (x + 0.45 * factor, -0.05, 1.85 * factor), (0.95 * factor, 0.9 * factor, 0.9 * factor), material)
        hood = add_cube(f"{name}_hood", lod_col, (x - 0.75 * factor, 0.0, 1.55 * factor), (1.35 * factor, 0.88 * factor, 0.45 * factor), material)
        for obj in (body, cab, hood):
            shade(obj)
        add_text(f"label_{label.lower()}", lod_col, label, (x, -1.1, 0.05), 0.18)

    add_cube("col_chassis_simple", lod_col, (-2.4, 1.65, 0.75), (2.7, 0.75, 0.55), "mat_guide_collision")
    add_cube("col_cab_simple", lod_col, (-2.0, 1.65, 1.55), (0.95, 0.72, 0.9), "mat_guide_collision")
    add_cube("col_front_weight_simple", lod_col, (-3.95, 1.65, 0.65), (0.58, 0.7, 0.5), "mat_guide_collision")
    add_text("label_collision", lod_col, "COL simplified collision volumes", (-2.4, 2.3, 0.05), 0.14)


def create_atlas_boards(root):
    atlas_col = ensure_collection("01_TEXTURE_ATLASES", root)

    start_x = -3.6
    start_y = -2.6
    gap = 1.45

    for index, (atlas, description, material) in enumerate(ATLASES):
        row = index // 3
        col = index % 3
        x = start_x + col * 3.0
        y = start_y - row * gap
        add_plane(f"uv_board_{atlas}", atlas_col, (x, y, 0.02), (1.2, 1.2, 1.0), material)
        add_text(f"label_{atlas}", atlas_col, f"{atlas}\n{description}", (x, y - 0.85, 0.04), 0.115)

        for i, map_name in enumerate(MAPS):
            add_cube(
                f"slot_{atlas}_{map_name}",
                atlas_col,
                (x - 1.05 + i * 0.35, y + 0.86, 0.04),
                (0.22, 0.12, 0.025),
                material,
            )
            add_text(
                f"label_{atlas}_{map_name}",
                atlas_col,
                map_name[:4],
                (x - 1.05 + i * 0.35, y + 1.02, 0.06),
                0.055,
            )


def create_bake_cages(root):
    cage_col = ensure_collection("02_BAKE_CAGES_AND_MATCHING", root)

    parts = [
        ("body", (-3.5, 2.9, 0.65), (1.45, 0.72, 0.55)),
        ("engine_chassis", (-1.6, 2.9, 0.65), (1.65, 0.55, 0.42)),
        ("wheel_front", (0.2, 2.9, 0.55), (0.62, 0.62, 0.62)),
        ("wheel_rear_dual", (1.45, 2.9, 0.72), (0.9, 0.9, 0.9)),
        ("cab_interior", (2.9, 2.9, 0.9), (0.9, 0.75, 0.95)),
    ]

    for name, location, scale in parts:
        add_cube(f"hp_{name}_source_reference", cage_col, location, scale, "mat_guide_lod2_gray")
        add_cube(f"lp_{name}_bake_target", cage_col, (location[0], location[1] + 0.75, location[2]), scale, "mat_guide_lod0_green")
        add_cube(f"cage_{name}_projection", cage_col, (location[0], location[1] + 1.5, location[2]), tuple(value * 1.08 for value in scale), "mat_guide_cage_blue")
        add_text(f"label_bake_{name}", cage_col, name, (location[0], location[1] + 2.15, 0.06), 0.095)


def create_export_markers(root):
    marker_col = ensure_collection("03_EXPORT_MARKERS", root)

    markers = {
        "empty_export_root": (0.0, 0.0, 0.0),
        "empty_lod0_root": (-1.6, 0.0, 0.0),
        "empty_lod1_root": (0.0, 0.0, 0.0),
        "empty_lod2_root": (1.6, 0.0, 0.0),
        "empty_collision_root": (0.0, 1.35, 0.0),
        "empty_texture_bake_root": (0.0, -1.35, 0.0),
        "empty_dirt_wear_reference": (2.8, -1.35, 0.0),
    }

    for name, location in markers.items():
        add_empty(name, marker_col, location)

    add_text("label_pass08_lock", marker_col, "PASS 08: low-poly, UV, bake, textures 4K", (0.0, -2.2, 0.05), 0.16)


def setup_scene():
    clear_scene()
    create_materials()

    root = ensure_collection(PROJECT)
    create_lod_guides(root)
    create_atlas_boards(root)
    create_bake_cages(root)
    create_export_markers(root)

    bpy.ops.object.light_add(type="AREA", location=(0, -5, 5))
    light = bpy.context.object
    light.name = "area_light_bake_review_softbox"
    light.data.energy = 350
    light.data.size = 5

    bpy.ops.object.camera_add(location=(0, -8.5, 4.4), rotation=(1.12, 0.0, 0.0))
    bpy.context.scene.camera = bpy.context.object
    bpy.context.object.name = "camera_pass08_overview"

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.unit_settings.system = "METRIC"

    print(f"{PROJECT} setup created.")


if __name__ == "__main__":
    setup_scene()

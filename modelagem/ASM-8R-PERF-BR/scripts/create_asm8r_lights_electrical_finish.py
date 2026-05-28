"""Create ASM-8R-PERF-BR lights, electrical and exterior finish base.

Run inside Blender:
  Scripting > Open this file > Run Script
"""

import math
import bpy

PROJECT = "ASM_8R_PERF_BR_LIGHTS_ELECTRICAL_FINISH"

MATERIALS = {
    "mat_hp_light_lens_clear": (0.82, 0.92, 1.0, 0.55, 0.0, 0.08),
    "mat_hp_light_lens_red": (0.85, 0.04, 0.03, 0.75, 0.0, 0.18),
    "mat_hp_light_lens_orange": (1.0, 0.48, 0.05, 0.75, 0.0, 0.18),
    "mat_hp_light_reflector": (0.86, 0.84, 0.78, 1.0, 0.92, 0.18),
    "mat_hp_light_emissive_white": (0.90, 0.96, 1.0, 1.0, 0.0, 0.10),
    "mat_hp_electrical_black": (0.015, 0.015, 0.014, 1.0, 0.0, 0.78),
    "mat_hp_decal_asm": (0.95, 0.95, 0.90, 1.0, 0.0, 0.42),
    "mat_hp_green_mount": (0.02, 0.30, 0.07, 1.0, 0.16, 0.42),
    "mat_hp_guide_red": (0.78, 0.03, 0.02, 1.0, 0.0, 0.50),
}


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def ensure_collection(name, parent=None):
    collection = bpy.data.collections.get(name) or bpy.data.collections.new(name)
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
            if "emissive" in name and "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = (r, g, b, a)
                bsdf.inputs["Emission Strength"].default_value = 1.2
        if "lens" in name:
            material.blend_method = "BLEND"


def mat(name):
    return bpy.data.materials[name]


def link_to(collection, obj):
    for current in obj.users_collection:
        current.objects.unlink(obj)
    collection.objects.link(obj)


def add_bevel(obj, width=0.012, segments=2):
    bevel = obj.modifiers.new("hp_bevel", "BEVEL")
    bevel.width = width
    bevel.segments = segments
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")


def cube_obj(name, location, scale, material_name, collection, rotation=(0, 0, 0), bevel=0.012):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    if bevel:
        add_bevel(obj, bevel, 2)
    return obj


def cylinder_obj(name, location, radius, depth, material_name, collection, axis="Y", vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    if axis == "X":
        obj.rotation_euler[1] += math.radians(90)
    elif axis == "Y":
        obj.rotation_euler[0] += math.radians(90)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
    return obj


def pipe_between(name, start, end, radius, material_name, collection):
    sx, sy, sz = start
    ex, ey, ez = end
    dx, dy, dz = ex - sx, ey - sy, ez - sz
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length <= 0:
        return None
    center = ((sx + ex) / 2, (sy + ey) / 2, (sz + ez) / 2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=length, location=center)
    obj = bpy.context.object
    obj.name = name
    import mathutils
    direction = mathutils.Vector((dx / length, dy / length, dz / length))
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.data.materials.append(mat(material_name))
    link_to(collection, obj)
    return obj


def empty_obj(name, location, collection, size=0.18):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = size
    obj.location = location
    collection.objects.link(obj)
    return obj


def add_light_pair(prefix, y, z, x_abs, collection, lens_material="mat_hp_light_lens_clear"):
    for side, x in [("l", -x_abs), ("r", x_abs)]:
        cube_obj(f"hp_light_{prefix}_{side}_housing", (x, y, z), (0.20, 0.075, 0.12), "mat_hp_electrical_black", collection)
        cube_obj(f"hp_light_{prefix}_{side}_reflector", (x, y - 0.035, z), (0.15, 0.020, 0.08), "mat_hp_light_reflector", collection)
        cube_obj(f"hp_light_{prefix}_{side}_lens", (x, y - 0.055, z), (0.17, 0.018, 0.095), lens_material, collection)
        cube_obj(f"hp_light_{prefix}_{side}_emissive", (x, y - 0.066, z), (0.12, 0.008, 0.060), "mat_hp_light_emissive_white", collection, bevel=0.004)
        empty_obj(f"empty_light_{prefix}_{side}", (x, y - 0.075, z), collection)


def add_lights(collection):
    add_light_pair("front_main", 2.94, 1.82, 0.42, collection)
    add_light_pair("waist", 0.55, 2.12, 0.88, collection)
    add_light_pair("rear_work", -2.12, 2.22, 0.82, collection)
    add_light_pair("rear_brake", -2.42, 1.80, 0.74, collection, lens_material="mat_hp_light_lens_red")
    add_light_pair("rear_turn", -2.45, 1.96, 0.58, collection, lens_material="mat_hp_light_lens_orange")

    cube_obj("hp_asm_roof_led_bar_mount", (0, -0.26, 3.39), (1.36, 0.06, 0.05), "mat_hp_electrical_black", collection)
    cube_obj("hp_asm_roof_led_bar_lens", (0, -0.30, 3.42), (1.28, 0.025, 0.055), "mat_hp_light_lens_clear", collection)
    cube_obj("hp_asm_roof_led_bar_emissive", (0, -0.318, 3.42), (1.18, 0.010, 0.030), "mat_hp_light_emissive_white", collection, bevel=0.004)
    empty_obj("empty_light_asm_led_bar", (0, -0.34, 3.42), collection)

    for side, x in [("l", -0.34), ("r", 0.34)]:
        cylinder_obj(f"hp_asm_grille_aux_{side}_housing", (x, 2.99, 1.58), 0.115, 0.070, "mat_hp_electrical_black", collection)
        cylinder_obj(f"hp_asm_grille_aux_{side}_lens", (x, 3.035, 1.58), 0.100, 0.018, "mat_hp_light_lens_clear", collection)
        empty_obj(f"empty_light_asm_aux_{side}", (x, 3.06, 1.58), collection)


def add_wiring_and_decals(collection):
    pipe_between("hp_wire_roof_led_left", (-0.58, -0.30, 3.36), (-0.88, -0.80, 3.08), 0.010, "mat_hp_electrical_black", collection)
    pipe_between("hp_wire_roof_led_right", (0.58, -0.30, 3.36), (0.88, -0.80, 3.08), 0.010, "mat_hp_electrical_black", collection)
    pipe_between("hp_wire_aux_grille_l", (-0.34, 3.02, 1.48), (-0.70, 2.58, 1.28), 0.010, "mat_hp_electrical_black", collection)
    pipe_between("hp_wire_aux_grille_r", (0.34, 3.02, 1.48), (0.70, 2.58, 1.28), 0.010, "mat_hp_electrical_black", collection)
    cube_obj("hp_electrical_junction_box_roof", (0.84, -0.78, 3.08), (0.18, 0.12, 0.08), "mat_hp_electrical_black", collection)
    cube_obj("hp_decal_asm_performance_br_left", (-0.78, 0.82, 1.96), (0.012, 0.54, 0.13), "mat_hp_decal_asm", collection, bevel=0.001)
    cube_obj("hp_decal_asm_performance_br_right", (0.78, 0.82, 1.96), (0.012, 0.54, 0.13), "mat_hp_decal_asm", collection, bevel=0.001)
    cube_obj("hp_decal_model_8r_410_front", (0.0, 2.91, 2.12), (0.48, 0.012, 0.12), "mat_hp_decal_asm", collection, bevel=0.001)


def add_guides(collection):
    for name, location, text in [
        ("label_led360", (0, -2.55, 2.60), "LED 360 + rear work lights"),
        ("label_asm_led", (0, -0.36, 3.62), "ASM slim LED bar"),
        ("label_aux_grille", (0, 3.16, 1.86), "ASM grille auxiliary lights"),
    ]:
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
    bpy.context.scene.render.engine = "CYCLES"
    camera_data = bpy.data.cameras.new("camera_lights_finish_review")
    camera = bpy.data.objects.new("camera_lights_finish_review", camera_data)
    bpy.context.scene.collection.objects.link(camera)
    camera.location = (3.8, -5.2, 3.2)
    camera.rotation_euler = (math.radians(62), 0, math.radians(38))
    bpy.context.scene.camera = camera
    sun_data = bpy.data.lights.new("sun_lights_key", "SUN")
    sun = bpy.data.objects.new("sun_lights_key", sun_data)
    sun.rotation_euler = (math.radians(48), 0, math.radians(34))
    bpy.context.scene.collection.objects.link(sun)


def main():
    clear_scene()
    create_materials()
    root = ensure_collection(PROJECT)
    lights = ensure_collection("01_lights_led360_and_asm", root)
    finish = ensure_collection("02_wiring_decals_finish", root)
    guides = ensure_collection("03_guides_and_labels", root)
    add_lights(lights)
    add_wiring_and_decals(finish)
    add_guides(guides)
    setup_scene()
    print("ASM-8R-PERF-BR lights/electrical/finish base created.")


if __name__ == "__main__":
    main()

"""Create the final FS22 ASM 8R Performance BR mod folder skeleton.

Run from the repository root:
  python modelagem/ASM-8R-PERF-BR/scripts/create_asm8r_mod_skeleton.py

The script creates the FS22 mod folder shell, including a starter I3D node
hierarchy. The starter I3D must be replaced by the real Blender/Giants Editor
export when the mesh is ready.
"""

from pathlib import Path
from textwrap import dedent
import argparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT_DIR = PROJECT_ROOT / "export" / "FS22_ASM_8R_PERF_BR"


MOD_DESC_XML = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<modDesc descVersion="79">
    <author>AgroScriptModding</author>
    <version>1.0.0.0</version>
    <title>
        <en>ASM 8R Performance BR</en>
        <pt>ASM 8R Performance BR</pt>
    </title>
    <description>
        <en>John Deere 8R Performance BR prepared by AgroScriptModding.</en>
        <pt>John Deere 8R Performance BR preparado pela AgroScriptModding.</pt>
    </description>
    <iconFilename>store/icon_ASM_8R_PERF_BR.dds</iconFilename>
    <multiplayer supported="true"/>
    <storeItems>
        <storeItem xmlFilename="vehicles/ASM_8R_PERF_BR.xml"/>
    </storeItems>
</modDesc>
"""


VEHICLE_XML = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<vehicle type="tractor">
    <annotation>ASM-8R-PERF-BR final modeling package placeholder.</annotation>
    <storeData>
        <name>ASM 8R Performance BR</name>
        <specs>
            <neededPower>410</neededPower>
            <maxSpeed>50</maxSpeed>
        </specs>
        <functions>
            <function>$l10n_function_tractor</function>
        </functions>
        <image>store/store_ASM_8R_PERF_BR.dds</image>
        <price>485000</price>
        <dailyUpkeep>410</dailyUpkeep>
        <brand>JOHNDEERE</brand>
        <category>tractorsL</category>
    </storeData>
    <base>
        <filename>vehicles/ASM_8R_PERF_BR.i3d</filename>
        <size width="3.3" length="6.7" height="3.55"/>
    </base>
    <components>
        <component centerOfMass="0 0.95 0" solverIterationCount="10" mass="15500"/>
    </components>
    <wheels>
        <!-- Configure wheel nodes after I3D export. -->
    </wheels>
    <lights>
        <!-- Configure factory LED, ASM roof bar and auxiliary grille lights. -->
    </lights>
    <attacherJoints>
        <!-- Configure rear hitch, drawbar and PTO after Giants Editor setup. -->
    </attacherJoints>
</vehicle>
"""


README_EXPORT = """ASM 8R Performance BR - Export Folder

This folder is a delivery skeleton generated from the final modeling package.

Replace template/placeholders with final exported assets:
- vehicles/ASM_8R_PERF_BR.i3d
- textures/*.png or *.dds
- store/store_ASM_8R_PERF_BR.dds
- store/icon_ASM_8R_PERF_BR.dds

After replacing assets, configure the vehicle XML in Giants Editor and test in
Farming Simulator 22 first. FS25 adaptation should keep the same node naming
unless the target game changes schema requirements.
"""


TEXTURE_README = """Texture slots expected:

- asm8r_body_4k_baseColor / normal / metallic / roughness / glossiness / dirtWear
- asm8r_engine_chassis_4k_baseColor / normal / metallic / roughness / glossiness / dirtWear
- asm8r_wheels_tires_4k_baseColor / normal / metallic / roughness / glossiness / dirtWear
- asm8r_interior_4k_baseColor / normal / metallic / roughness / glossiness / emissive
- asm8r_lights_2k_baseColor / normal / emissive
- asm8r_decals_2k_baseColor / normal
"""


SOUND_README = """Sound setup placeholder.

Use this folder for engine, transmission, turbo and direct exhaust sound data
during the implementation phase. Modeling is already locked and should not be
changed by sound work.
"""


I3D_TEMPLATE = """<?xml version="1.0" encoding="iso-8859-1"?>
<i3D name="ASM_8R_PERF_BR" version="1.6">
    <Asset>
        <Export program="AgroScriptModding" version="1.0"/>
    </Asset>
    <Files>
        <!-- Add final texture and shape references after Blender/Giants export. -->
    </Files>
    <Materials>
        <!-- Replace with exported FS materials. -->
    </Materials>
    <Shapes>
        <!-- Replace with exported mesh shapes. -->
    </Shapes>
    <Scene>
        <TransformGroup name="ASM_8R_PERF_BR" nodeId="1">
            <TransformGroup name="visual" nodeId="2">
                <TransformGroup name="hood_body_cab" nodeId="3"/>
                <TransformGroup name="engine_chassis" nodeId="4"/>
                <TransformGroup name="cab_interior" nodeId="5"/>
            </TransformGroup>
            <TransformGroup name="wheels" nodeId="6">
                <TransformGroup name="wheel_front_left" nodeId="7"/>
                <TransformGroup name="wheel_front_right" nodeId="8"/>
                <TransformGroup name="wheel_rear_left_inner" nodeId="9"/>
                <TransformGroup name="wheel_rear_left_outer" nodeId="10"/>
                <TransformGroup name="wheel_rear_right_inner" nodeId="11"/>
                <TransformGroup name="wheel_rear_right_outer" nodeId="12"/>
            </TransformGroup>
            <TransformGroup name="steering" nodeId="13"/>
            <TransformGroup name="ils_front_axle" nodeId="14"/>
            <TransformGroup name="rear_hitch" nodeId="15"/>
            <TransformGroup name="hydraulics" nodeId="16"/>
            <TransformGroup name="lights" nodeId="17">
                <TransformGroup name="light_factory_front" nodeId="18"/>
                <TransformGroup name="light_factory_rear" nodeId="19"/>
                <TransformGroup name="light_asm_roof_bar" nodeId="20"/>
                <TransformGroup name="light_asm_grille_aux" nodeId="21"/>
            </TransformGroup>
            <TransformGroup name="collisions" nodeId="22"/>
            <TransformGroup name="attacherJoints" nodeId="23">
                <TransformGroup name="trailerLow" nodeId="24"/>
                <TransformGroup name="trailerHigh" nodeId="25"/>
                <TransformGroup name="ptoBack" nodeId="26"/>
            </TransformGroup>
            <TransformGroup name="cameras" nodeId="27">
                <TransformGroup name="outdoorCameraReference" nodeId="28"/>
                <TransformGroup name="indoorCameraReference" nodeId="29"/>
            </TransformGroup>
        </TransformGroup>
    </Scene>
</i3D>
"""


STORE_PLACEHOLDER = """DDS placeholder.

Replace this text file with:
- store_ASM_8R_PERF_BR.dds
- icon_ASM_8R_PERF_BR.dds
"""


def build_files(export_dir):
    return {
        export_dir / "modDesc.xml": MOD_DESC_XML,
        export_dir / "README_EXPORT.txt": README_EXPORT,
        export_dir / "vehicles" / "ASM_8R_PERF_BR.xml": VEHICLE_XML,
        export_dir / "vehicles" / "ASM_8R_PERF_BR.i3d": I3D_TEMPLATE,
        export_dir / "textures" / "README.txt": TEXTURE_README,
        export_dir / "sounds" / "README.txt": SOUND_README,
        export_dir / "store" / "store_ASM_8R_PERF_BR.dds.placeholder.txt": STORE_PLACEHOLDER,
        export_dir / "store" / "icon_ASM_8R_PERF_BR.dds.placeholder.txt": STORE_PLACEHOLDER,
    }


def write_file(path, content, force=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"skip existing: {path}")
        return
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")
    print(f"created: {path}")


def main():
    parser = argparse.ArgumentParser(description="Create ASM 8R mod skeleton.")
    parser.add_argument("--output", type=Path, default=DEFAULT_EXPORT_DIR, help="Target export folder.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing placeholder files.")
    args = parser.parse_args()

    export_dir = args.output.resolve()
    for path, content in build_files(export_dir).items():
        write_file(path, content, args.force)

    print(f"FS22 mod skeleton ready: {export_dir}")


if __name__ == "__main__":
    main()

import sys
from pathlib import Path

import bpy

COLOUR_BUCKET_SIZE = 16
UR5E_BASE_REPAIR = {
    "source_robot": "UR3e",
    "source_link": 0,
    "target_x_span": 0.1469,
    "target_top_z": 0.0946,
}


def parse_args():
    if "--" not in sys.argv:
        raise SystemExit(
            "Usage: blender --background --python convert_ply_to_dae_blender.py -- "
            "input.ply output.dae [--palette source|ur3e]"
        )
    args = sys.argv[sys.argv.index("--") + 1 :]
    if len(args) not in (2, 4):
        raise SystemExit("Expected input PLY and output DAE paths")

    palette = "source"
    if len(args) == 4:
        if args[2] != "--palette":
            raise SystemExit("Optional argument must be --palette source|ur3e")
        palette = args[3]

    if palette not in ("source", "ur3e"):
        raise SystemExit("Palette must be either source or ur3e")

    return Path(args[0]), Path(args[1]), palette


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_ply(path):
    if hasattr(bpy.ops.wm, "ply_import"):
        bpy.ops.wm.ply_import(filepath=str(path), import_colors="LINEAR")
    else:
        bpy.ops.import_mesh.ply(filepath=str(path))


def repair_source_path(path, robot_name, link_index):
    if robot_name != "UR5e" or link_index != 0:
        return path

    source_name = UR5E_BASE_REPAIR["source_robot"]
    source_file = f'{source_name}Link{UR5E_BASE_REPAIR["source_link"]}.ply'
    candidates = [
        path.parent.parent / source_name / source_file,
        path.parent.parent / f"@{source_name}" / source_file,
    ]
    source_path = next((candidate for candidate in candidates if candidate.exists()), None)
    if source_path is None:
        paths = "\n  ".join(str(candidate) for candidate in candidates)
        raise SystemExit(f"Missing UR5e base repair source mesh. Tried:\n  {paths}")

    return source_path


def repair_imported_geometry(robot_name, link_index):
    if robot_name != "UR5e" or link_index != 0:
        return

    objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    for obj in objects:
        mesh = obj.data
        xs = [vertex.co[0] for vertex in mesh.vertices]
        zs = [vertex.co[2] for vertex in mesh.vertices]
        x_span = max(xs) - min(xs)
        z_lower = min(zs)
        z_span = max(zs) - z_lower
        if x_span <= 1e-9 or z_span <= 1e-9:
            continue

        xy_scale = UR5E_BASE_REPAIR["target_x_span"] / x_span
        z_scale = UR5E_BASE_REPAIR["target_top_z"] / z_span
        for vertex in mesh.vertices:
            vertex.co[0] *= xy_scale
            vertex.co[1] *= xy_scale
            vertex.co[2] = (vertex.co[2] - z_lower) * z_scale

        mesh.update()


def quantize_colour(colour):
    rgba = [max(0.0, min(1.0, float(channel))) for channel in colour[:4]]
    rgb255 = [round(channel * 255) for channel in rgba[:3]]
    quantized = []
    for channel in rgb255:
        bucket = round(channel / COLOUR_BUCKET_SIZE) * COLOUR_BUCKET_SIZE
        quantized.append(max(0, min(255, bucket)))
    return (*quantized, 255)


def robot_link_from_path(path):
    stem = path.stem
    for marker in ("Link", "link"):
        if marker in stem:
            robot_name, link_text = stem.split(marker, 1)
            try:
                return robot_name, int(link_text)
            except ValueError:
                break
    return stem, None


def is_clear_cyan(colour):
    r, g, b, _ = colour
    return g > 0.72 and b > 0.72 and r < 0.72


def is_long_link_joint_region(robot_name, link_index, position_ratio):
    if robot_name not in {"UR5e", "UR10e"} or link_index not in {2, 3}:
        return False

    if position_ratio is None:
        return False

    if link_index == 2:
        return position_ratio < 0.18 or position_ratio > 0.82

    return position_ratio < 0.12 or position_ratio > 0.84


def apply_palette_style(
    colour,
    palette,
    robot_name=None,
    link_index=None,
    position_ratio=None,
):
    if palette == "source":
        return colour

    r, g, b, a = colour
    max_channel = max(r, g, b)
    min_channel = min(r, g, b)
    saturation = max_channel - min_channel
    ur_cyan = (85 / 255, 220 / 255, 255 / 255, a)
    ur_light = (229 / 255, 234 / 255, 237 / 255, a)
    ur_mid = (128 / 255, 128 / 255, 128 / 255, a)
    ur_dark = (64 / 255, 64 / 255, 64 / 255, a)

    if max_channel < 0.08:
        return ur_dark

    is_joint_housing_link = robot_name in {"UR5e", "UR10e"} and link_index in {1, 4, 5}
    is_end_joint_region = is_long_link_joint_region(
        robot_name,
        link_index,
        position_ratio,
    )

    if g > 0.72 and b > 0.72:
        if r < 0.72:
            return ur_cyan
        if is_joint_housing_link or is_end_joint_region:
            return ur_mid
        return ur_light

    if g > r + 0.10 and b > r + 0.10:
        if max(g, b) > 0.45:
            return ur_cyan
        return ur_dark

    if min_channel > 0.86:
        return ur_light

    if saturation < 0.08:
        luminance = (r + g + b) / 3
        if (is_joint_housing_link or is_end_joint_region) and luminance > 0.35:
            return ur_mid
        if luminance > 0.72:
            return ur_light
        if luminance > 0.35:
            return ur_mid
        return ur_dark

    if (is_joint_housing_link or is_end_joint_region) and min_channel > 0.45:
        return ur_mid

    return colour


def material_for_colour(obj, materials, colour_key):
    if colour_key in materials:
        return materials[colour_key]

    r, g, b, a = colour_key
    mat = bpy.data.materials.new(name=f"mat_{r:03d}_{g:03d}_{b:03d}")
    mat.diffuse_color = (r / 255, g / 255, b / 255, a / 255)
    obj.data.materials.append(mat)
    index = len(obj.data.materials) - 1
    materials[colour_key] = index
    return index


def polygon_colour(mesh, attribute, polygon):
    if attribute is None:
        return (0.72, 0.72, 0.72, 1.0)

    if attribute.domain == "CORNER":
        values = [attribute.data[index].color for index in polygon.loop_indices]
    elif attribute.domain == "POINT":
        values = [attribute.data[index].color for index in polygon.vertices]
    else:
        return (0.72, 0.72, 0.72, 1.0)

    count = len(values)
    if count == 0:
        return (0.72, 0.72, 0.72, 1.0)

    return tuple(sum(value[channel] for value in values) / count for channel in range(4))


def polygon_position_ratio(mesh, polygon, lower, upper, axis=0):
    values = [mesh.vertices[index].co[axis] for index in polygon.vertices]
    if not values:
        return None

    span = upper - lower
    if span <= 1e-9:
        return None

    centroid = sum(values) / len(values)
    return (centroid - lower) / span


def assign_colour_materials(palette, robot_name=None, link_index=None):
    objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    for obj in objects:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        mesh = obj.data
        attribute = None
        if mesh.color_attributes:
            attribute = mesh.color_attributes.active_color or mesh.color_attributes[0]

        mesh.materials.clear()
        materials = {}
        x_coordinates = [vertex.co[0] for vertex in mesh.vertices]
        x_lower = min(x_coordinates)
        x_upper = max(x_coordinates)
        for polygon in mesh.polygons:
            colour = polygon_colour(mesh, attribute, polygon)
            position_ratio = polygon_position_ratio(mesh, polygon, x_lower, x_upper)
            colour = apply_palette_style(
                colour,
                palette,
                robot_name,
                link_index,
                position_ratio,
            )
            colour_key = quantize_colour(colour)
            polygon.material_index = material_for_colour(obj, materials, colour_key)

        if not mesh.materials:
            material_for_colour(obj, materials, (184, 184, 184, 255))


def export_dae(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    bpy.ops.wm.collada_export(
        filepath=str(path),
        selected=True,
        apply_modifiers=True,
        triangulate=True,
    )


def main():
    input_path, output_path, palette = parse_args()
    robot_name, link_index = robot_link_from_path(input_path)
    source_path = repair_source_path(input_path, robot_name, link_index)
    clear_scene()
    import_ply(source_path)
    repair_imported_geometry(robot_name, link_index)
    assign_colour_materials(palette, robot_name, link_index)
    export_dae(output_path)


if __name__ == "__main__":
    main()

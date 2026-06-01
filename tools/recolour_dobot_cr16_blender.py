import argparse
import re
import sys
from pathlib import Path

import bpy


COLOURS = {
    "white": (0.92, 0.94, 0.93, 1.0),
    "light_grey": (0.72, 0.74, 0.73, 1.0),
    "grey": (0.46, 0.48, 0.47, 1.0),
    "metal": (0.62, 0.63, 0.61, 1.0),
    "dark": (0.08, 0.08, 0.08, 1.0),
    "blue": (0.00, 0.20, 0.48, 1.0),
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply a Dobot CR16-like material palette to a candidate DAE link."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)

    if "--" not in sys.argv:
        raise SystemExit(
            "Usage: blender --background --python recolour_dobot_cr16_blender.py -- "
            "input.dae output.dae"
        )

    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def mesh_objects():
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def import_dae(path):
    bpy.ops.wm.collada_import(filepath=str(path))


def link_index(path):
    match = re.search(r"Link(\d+)", path.stem)
    if not match:
        raise SystemExit(f"Could not infer link index from {path.name}")
    return int(match.group(1))


def material(name):
    mat = bpy.data.materials.new(name=f"dobot_cr16_{name}")
    mat.diffuse_color = COLOURS[name]
    return mat


def material_set(obj):
    obj.data.materials.clear()
    names = ["white", "light_grey", "grey", "metal", "dark", "blue"]
    materials = {name: material(name) for name in names}
    for mat in materials.values():
        obj.data.materials.append(mat)
    return {name: index for index, name in enumerate(names)}


def ratio(value, lower, upper):
    span = upper - lower
    if span <= 1e-9:
        return 0.5
    return (value - lower) / span


def centroid(mesh, polygon):
    points = [mesh.vertices[index].co for index in polygon.vertices]
    count = len(points)
    return (
        sum(point.x for point in points) / count,
        sum(point.y for point in points) / count,
        sum(point.z for point in points) / count,
    )


def in_band(value, centres, width):
    return any(abs(value - centre) <= width for centre in centres)


def link_colour(index, xr, yr, zr):
    if index == 0:
        if in_band(zr, (0.23,), 0.025):
            return "blue"
        if zr < 0.18:
            return "metal"
        if zr > 0.70:
            return "white"
        return "grey"

    if index == 1:
        if in_band(zr, (0.16, 0.84), 0.025):
            return "blue"
        if zr > 0.78 or zr < 0.12:
            return "white"
        return "grey"

    if index == 2:
        if in_band(xr, (0.13, 0.87), 0.025):
            return "blue"
        if xr < 0.11 or xr > 0.89:
            return "white"
        return "grey"

    if index == 3:
        if in_band(xr, (0.12, 0.88), 0.025):
            return "blue"
        if xr < 0.10 or xr > 0.90:
            return "grey"
        return "white"

    if index == 4:
        if in_band(zr, (0.20, 0.82), 0.025):
            return "blue"
        if zr < 0.18 or zr > 0.84:
            return "grey"
        return "white"

    if index == 5:
        if in_band(zr, (0.22, 0.82), 0.025):
            return "blue"
        if zr < 0.20 or zr > 0.84:
            return "grey"
        return "white"

    if index == 6:
        if zr > 0.74:
            return "dark"
        if zr < 0.18:
            return "metal"
        return "light_grey"

    return "white"


def recolour_object(obj, index):
    mesh = obj.data
    material_indices = material_set(obj)

    xs = [vertex.co.x for vertex in mesh.vertices]
    ys = [vertex.co.y for vertex in mesh.vertices]
    zs = [vertex.co.z for vertex in mesh.vertices]

    for polygon in mesh.polygons:
        x, y, z = centroid(mesh, polygon)
        colour_name = link_colour(
            index,
            ratio(x, min(xs), max(xs)),
            ratio(y, min(ys), max(ys)),
            ratio(z, min(zs), max(zs)),
        )
        polygon.material_index = material_indices[colour_name]


def export_dae(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()

    bpy.ops.object.select_all(action="DESELECT")
    for obj in mesh_objects():
        obj.select_set(True)
    if mesh_objects():
        bpy.context.view_layer.objects.active = mesh_objects()[0]

    bpy.ops.wm.collada_export(
        filepath=str(path),
        selected=True,
        apply_modifiers=True,
        triangulate=True,
    )


def main():
    args = parse_args()
    index = link_index(args.input)
    clear_scene()
    import_dae(args.input)
    for obj in mesh_objects():
        recolour_object(obj, index)
    export_dae(args.output)
    print(f"Recoloured {args.input.name} as Dobot CR16 link {index}")


if __name__ == "__main__":
    main()

import argparse
import sys
from pathlib import Path

import bmesh
import bpy


def parse_args():
    parser = argparse.ArgumentParser(
        description="Downsample a Collada DAE mesh using Blender's decimate modifier."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.5,
        help="Decimate ratio to keep. 0.5 keeps roughly half the faces.",
    )
    parser.add_argument(
        "--double-sided",
        action="store_true",
        help="Duplicate mesh faces with reversed normals for viewers that cull back faces.",
    )

    if "--" not in sys.argv:
        raise SystemExit(
            "Usage: blender --background --python downsample_dae_blender.py -- "
            "input.dae output.dae [--ratio 0.5]"
        )

    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    if not 0.0 < args.ratio <= 1.0:
        raise SystemExit("--ratio must be greater than 0 and no more than 1")

    return args


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def mesh_objects():
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def triangle_count(obj):
    obj.data.calc_loop_triangles()
    return len(obj.data.loop_triangles)


def import_dae(path):
    bpy.ops.wm.collada_import(filepath=str(path))


def apply_decimate(ratio):
    before = 0
    after = 0

    for obj in mesh_objects():
        before += triangle_count(obj)
        if triangle_count(obj) < 8:
            after += triangle_count(obj)
            continue

        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        modifier = obj.modifiers.new("downsample_decimate", "DECIMATE")
        modifier.ratio = ratio
        if hasattr(modifier, "use_collapse_triangulate"):
            modifier.use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        after += triangle_count(obj)

    return before, after


def make_double_sided():
    for obj in mesh_objects():
        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        original_faces = list(bm.faces)
        duplicated = bmesh.ops.duplicate(bm, geom=original_faces)
        for element in duplicated["geom"]:
            if isinstance(element, bmesh.types.BMFace):
                element.normal_flip()
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()


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
    clear_scene()
    import_dae(args.input)
    before, after = apply_decimate(args.ratio)
    if args.double_sided:
        make_double_sided()
    export_dae(args.output)
    print(
        f"{args.input.name}: {before} triangles -> {after} triangles "
        f"({after / before:.2%} retained)"
        f"{' with double-sided faces' if args.double_sided else ''}"
        if before
        else f"{args.input.name}: no mesh triangles found"
    )


if __name__ == "__main__":
    main()

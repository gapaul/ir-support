import argparse
from pathlib import Path

import numpy as np
import scipy.io as sio


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mat_path", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--stem", required=True)
    return parser.parse_args()


def as_uint8_colour(colour):
    rgb = np.asarray(colour, dtype=float).reshape(-1)[:3]
    if np.nanmax(rgb) <= 1.0:
        rgb = rgb * 255.0
    rgb = np.clip(np.rint(rgb), 0, 255).astype(np.uint8)
    return int(rgb[0]), int(rgb[1]), int(rgb[2]), 255


def write_ascii_ply(path, vertices, faces, colour):
    path.parent.mkdir(parents=True, exist_ok=True)
    red, green, blue, alpha = as_uint8_colour(colour)
    faces = np.asarray(faces, dtype=np.int64) - 1

    with path.open("w", encoding="ascii", newline="\n") as ply:
        ply.write("ply\n")
        ply.write("format ascii 1.0\n")
        ply.write(f"element vertex {len(vertices)}\n")
        ply.write("property float x\n")
        ply.write("property float y\n")
        ply.write("property float z\n")
        ply.write("property uchar red\n")
        ply.write("property uchar green\n")
        ply.write("property uchar blue\n")
        ply.write("property uchar alpha\n")
        ply.write(f"element face {len(faces)}\n")
        ply.write("property list uchar int vertex_indices\n")
        ply.write("end_header\n")
        for x, y, z in np.asarray(vertices, dtype=float):
            ply.write(f"{x:.9g} {y:.9g} {z:.9g} {red} {green} {blue} {alpha}\n")
        for face in faces:
            ply.write(f"3 {face[0]} {face[1]} {face[2]}\n")


def main():
    args = parse_args()
    data = sio.loadmat(args.mat_path, squeeze_me=True, struct_as_record=False)
    for index, shape in enumerate(data["shapeModel"]):
        write_ascii_ply(
            args.output_dir / f"{args.stem}Link{index}.ply",
            shape.vertex,
            shape.face,
            shape.colour,
        )


if __name__ == "__main__":
    main()

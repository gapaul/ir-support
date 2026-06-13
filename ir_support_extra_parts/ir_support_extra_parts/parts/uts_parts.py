from pathlib import Path

import numpy as np
import spatialgeometry as geometry


PARTS_DIR = Path(__file__).resolve().parent

# Optional source/reference URLs for packaged part meshes. Keep this empty unless
# there is a real, stable source URL for an unmodified or lightly modified asset.
PART_REFERENCE_URLS = {}


def _part_index():
    return {path.stem.lower(): path for path in sorted(PARTS_DIR.glob("*.dae"))}


def _normalise_name(name):
    name = str(name)
    suffix = Path(name).suffix.lower()
    if suffix in {".dae", ".ply", ".stl"}:
        name = name[: -len(suffix)]
    return name.lower()


def part_names():
    """Return the available UTS part names without file extensions."""

    return tuple(path.stem for path in sorted(PARTS_DIR.glob("*.dae")))


def part_path(name):
    """Return the packaged DAE path for a UTS part."""

    parts = _part_index()
    key = _normalise_name(name)
    if key not in parts:
        available = ", ".join(part_names())
        raise ValueError(f"Unknown UTS part '{name}'. Available parts: {available}")
    return parts[key]


def part_reference_url(name):
    """Return a reference URL for a packaged part if one is known."""

    key = _normalise_name(name)
    for known_name, url in PART_REFERENCE_URLS.items():
        if _normalise_name(known_name) == key:
            return url
    return None


def part_mesh(name, pose=None, color=None):
    """Create a spatialgeometry Mesh for a packaged UTS part."""

    path = str(part_path(name))
    mesh = geometry.Mesh(path, color=color) if color is not None else geometry.Mesh(path)
    if pose is not None:
        mesh.T = pose.A if hasattr(pose, "A") else np.asarray(pose, dtype=float)
    return mesh


PART_NAMES = part_names()

__all__ = [
    "PART_NAMES",
    "PART_REFERENCE_URLS",
    "part_names",
    "part_path",
    "part_reference_url",
    "part_mesh",
]


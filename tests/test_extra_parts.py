from pathlib import Path
import sys

import numpy as np
from spatialmath import SE3


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_PARTS_ROOT = REPO_ROOT / "ir_support_extra_parts"
for path in (REPO_ROOT, EXTRA_PARTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_parts.parts import PART_NAMES, part_mesh, part_names, part_path, part_reference_url  # noqa: E402


def test_extra_parts_are_discoverable_and_dae_only():
    assert "brick" in PART_NAMES
    assert "tableBlue1x1x0.5m" in part_names()

    parts_dir = EXTRA_PARTS_ROOT / "ir_support_extra_parts" / "parts"
    assert not list(parts_dir.glob("*.ply"))
    assert len(list(parts_dir.glob("*.dae"))) == len(PART_NAMES)


def test_extra_part_path_accepts_original_ply_name():
    path = part_path("brick.ply")

    assert path.name == "brick.dae"
    assert path.exists()


def test_extra_part_mesh_loads_with_pose():
    mesh = part_mesh("brick", pose=SE3(0.1, 0.2, 0.3))

    assert np.allclose(mesh.T[:3, 3], [0.1, 0.2, 0.3])


def test_all_extra_part_meshes_load():
    for index, name in enumerate(PART_NAMES):
        mesh = part_mesh(name, pose=SE3(index * 0.01, 0.0, 0.0))

        assert mesh is not None
        assert np.asarray(mesh.T).shape == (4, 4)
        assert np.isfinite(mesh.T).all()


def test_extra_part_reference_url_is_optional():
    assert part_reference_url("brick") is None
    assert part_reference_url("brick.dae") is None



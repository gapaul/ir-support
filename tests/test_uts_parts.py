from pathlib import Path

import numpy as np
from spatialmath import SE3

from ir_support.parts import PART_NAMES, part_mesh, part_names, part_path


def test_uts_parts_are_discoverable_and_dae_only():
    assert "brick" in PART_NAMES
    assert "tableBlue1x1x0.5m" in part_names()

    parts_dir = Path(__file__).resolve().parents[1] / "ir_support" / "parts"
    assert not list(parts_dir.glob("*.ply"))
    assert len(list(parts_dir.glob("*.dae"))) == len(PART_NAMES)


def test_uts_part_path_accepts_original_ply_name():
    path = part_path("brick.ply")

    assert path.name == "brick.dae"
    assert path.exists()


def test_uts_part_mesh_loads_with_pose():
    mesh = part_mesh("brick", pose=SE3(0.1, 0.2, 0.3))

    assert np.allclose(mesh.T[:3, 3], [0.1, 0.2, 0.3])


def test_all_uts_part_meshes_load():
    for index, name in enumerate(PART_NAMES):
        mesh = part_mesh(name, pose=SE3(index * 0.01, 0.0, 0.0))

        assert mesh is not None
        assert np.asarray(mesh.T).shape == (4, 4)
        assert np.isfinite(mesh.T).all()

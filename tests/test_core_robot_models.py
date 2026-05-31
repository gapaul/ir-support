from pathlib import Path

import numpy as np
import pytest
from spatialmath import SE3

from ir_support.robots import (
    DensoVM6083,
    DobotMagician,
    Fetch,
    HansCute,
    Sawyer,
    UR10,
    UR10e,
    UR3e,
)


ROBOT_EXPECTATIONS = [
    (UR3e, 6, 7),
    (DensoVM6083, 6, 7),
    (DobotMagician, 5, 6),
    (Fetch, 7, 8),
    (HansCute, 7, 8),
    (Sawyer, 7, 8),
    (UR10, 6, 7),
    (UR10e, 6, 7),
]


@pytest.mark.parametrize(("robot_cls", "joint_count", "mesh_count"), ROBOT_EXPECTATIONS)
def test_core_robot_model_loads_meshes_and_moves(robot_cls, joint_count, mesh_count):
    robot = robot_cls()

    assert robot.n == joint_count
    assert len(robot.links_3d) == mesh_count
    assert robot.home_q.shape == (joint_count,)
    assert np.isfinite(robot.fkine(robot.q).A).all()

    q_goal = robot.home_q + np.linspace(0.08, -0.08, joint_count)
    robot.q = q_goal

    for link_mesh in robot.links_3d:
        assert np.asarray(link_mesh.T).shape == (4, 4)
        assert np.isfinite(link_mesh.T).all()


def test_core_robot_model_accepts_base_transform():
    robot = UR3e(base=SE3(0.1, 0.2, 0.3))

    assert np.allclose(robot.base.t, [0.1, 0.2, 0.3])


def test_core_mesh_robot_assets_are_dae_only():
    robots_dir = Path(__file__).resolve().parents[1] / "ir_support" / "robots"
    robot_names = [robot_cls.__name__ for robot_cls, _, _ in ROBOT_EXPECTATIONS]

    for robot_name in robot_names:
        robot_dir = robots_dir / robot_name
        assert not list(robot_dir.glob("*.ply")), f"{robot_name} still has copied PLY assets"
        assert list(robot_dir.glob("*.dae")), f"{robot_name} has no DAE assets"

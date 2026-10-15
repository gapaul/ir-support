from pathlib import Path

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


def make_robot():
    mesh_dir = Path(__file__).parents[1] / "ir_support" / "robots" / "UR3e"
    robot = DHRobot3D(
        links=[rtb.RevoluteDH(a=0.2)],
        link3D_names={"link0": "UR3eLink0", "link1": "UR3eLink1"},
        link3d_dir=str(mesh_dir),
        qtest=[0.0],
        qtest_transforms=[np.eye(4), np.eye(4)],
    )
    robot._update_3dmodel()
    return robot


def assert_meshes_match_current_state(robot):
    expected_frames = robot._get_transforms(robot.q)
    for index, mesh in enumerate(robot.links_3d):
        expected = expected_frames[index] @ robot._relation_matrices[index]
        assert np.allclose(mesh.T, expected)


def test_assigning_q_updates_meshes_to_the_new_joint_state():
    robot = make_robot()

    robot.q = np.array([0.4])

    assert_meshes_match_current_state(robot)


def test_assigning_base_updates_meshes_to_the_new_base():
    robot = make_robot()

    robot.base = SE3.Tx(0.3) * SE3.Tz(0.1)

    assert_meshes_match_current_state(robot)

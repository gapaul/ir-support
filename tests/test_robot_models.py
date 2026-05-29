import numpy as np

from ir_support.robots import DensoVS060, LinearUR3, UR3, schunk_UTS_v2_0

from .helpers import assert_allclose


def test_schunk_robot_has_expected_basic_shape():
    robot = schunk_UTS_v2_0()

    assert robot.n == 6
    assert len(robot.links) == 6
    assert robot.qlim.shape == (2, 6)
    assert_allclose(robot.base.A[:3, 3], [0.0, 0.0, 0.0])


def test_denso_robot_loads_from_packaged_urdf():
    robot = DensoVS060()

    assert robot.n == 6
    assert_allclose(robot.q, np.zeros(6))
    assert_allclose(robot.base.A[:3, 3], [0.0, 0.0, 0.2])


def test_ur3_mesh_model_loads_packaged_geometry():
    robot = UR3()

    assert robot.n == 6
    assert len(robot.links_3d) == 7
    assert_allclose(robot.q, [0.0, -np.pi / 2, 0.0, 0.0, 0.0, 0.0])


def test_linear_ur3_mesh_model_loads_packaged_geometry():
    robot = LinearUR3()

    assert robot.n == 7
    assert len(robot.links_3d) == 8
    assert_allclose(robot.q, [0.0, 0.0, -np.pi / 2, 0.0, 0.0, 0.0, 0.0])

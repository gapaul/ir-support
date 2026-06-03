import sys
from pathlib import Path

import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.DensoVP6242.DensoVP6242 import DensoVP6242  # noqa: E402
from ir_support_extra_robots.robots.DensoVS068.DensoVS068 import DensoVS068  # noqa: E402
from ir_support_extra_robots.robots.DobotCR10.DobotCR10 import DobotCR10  # noqa: E402
from ir_support_extra_robots.robots.DobotNova2.DobotNova2 import DobotNova2  # noqa: E402
from ir_support_extra_robots.robots.FanucM20.FanucM20 import FanucM20  # noqa: E402
from ir_support_extra_robots.robots.IgusReBel.IgusReBel import IgusReBel  # noqa: E402
from ir_support_extra_robots.robots.KukaLBRiiwa14.KukaLBRiiwa14 import KukaLBRiiwa14  # noqa: E402
from ir_support_extra_robots.robots.ABBIRB1520ID.ABBIRB1520ID import ABBIRB1520ID  # noqa: E402
from ir_support_extra_robots.robots.ABBIRB1660ID.ABBIRB1660ID import ABBIRB1660ID  # noqa: E402


ROBOT_FACTORIES = [
    DensoVP6242,
    DensoVS068,
    DobotCR10,
    DobotNova2,
    FanucM20,
    IgusReBel,
    KukaLBRiiwa14,
    ABBIRB1520ID,
    ABBIRB1660ID,
]


@pytest.mark.parametrize("factory", ROBOT_FACTORIES)
def test_student_candidate_robot_batch3_loads_meshes_and_moves(factory):
    robot = factory()

    assert len(robot.links_3d) == robot.n + 1
    assert np.isfinite(robot.fkine(robot.q).A).all()

    q_goal = np.asarray(robot.q, dtype=float) + np.linspace(0.04, -0.04, robot.n)
    robot.q = q_goal

    assert np.allclose(robot.q, q_goal)
    for link_mesh in robot.links_3d:
        assert np.asarray(link_mesh.T).shape == (4, 4)
        assert np.isfinite(link_mesh.T).all()

import sys
from pathlib import Path

import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.ABBIRB2600.ABBIRB2600 import ABBIRB2600  # noqa: E402
from ir_support_extra_robots.robots.KukaKR3R540.KukaKR3R540 import KukaKR3R540  # noqa: E402
from ir_support_extra_robots.robots.KukaKR10R1100.KukaKR10R1100 import KukaKR10R1100  # noqa: E402
from ir_support_extra_robots.robots.EpsonVT6.EpsonVT6 import EpsonVT6  # noqa: E402
from ir_support_extra_robots.robots.FanucLRMate200iC.FanucLRMate200iC import FanucLRMate200iC  # noqa: E402
from ir_support_extra_robots.robots.KukaKR60.KukaKR60 import KukaKR60  # noqa: E402
from ir_support_extra_robots.robots.UnitreeZ1.UnitreeZ1 import UnitreeZ1  # noqa: E402
from ir_support_extra_robots.robots.ProSixVT6.ProSixVT6 import ProSixVT6  # noqa: E402
from ir_support_extra_robots.robots.MyCobot320.MyCobot320 import MyCobot320  # noqa: E402
from ir_support_extra_robots.robots.MitsubishiRV2RF.MitsubishiRV2RF import MitsubishiRV2RF  # noqa: E402


ROBOT_FACTORIES = [
    ABBIRB2600,
    KukaKR3R540,
    KukaKR10R1100,
    EpsonVT6,
    FanucLRMate200iC,
    KukaKR60,
    UnitreeZ1,
    ProSixVT6,
    MyCobot320,
    MitsubishiRV2RF,
]


@pytest.mark.parametrize("factory", ROBOT_FACTORIES)
def test_student_candidate_robot_batch2_loads_meshes_and_moves(factory):
    robot = factory()

    assert robot.n == 6
    assert len(robot.links_3d) == robot.n + 1
    assert np.isfinite(robot.fkine(robot.q).A).all()

    q_goal = np.asarray(robot.q, dtype=float) + np.linspace(0.04, -0.04, robot.n)
    robot.q = q_goal

    assert np.allclose(robot.q, q_goal)
    for link_mesh in robot.links_3d:
        assert np.asarray(link_mesh.T).shape == (4, 4)
        assert np.isfinite(link_mesh.T).all()

import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.BCN3DMoveo.BCN3DMoveo import BCN3DMoveo  # noqa: E402
from ir_support_extra_robots.robots.DobotNova5.DobotNova5 import DobotNova5  # noqa: E402
from ir_support_extra_robots.robots.DoosanA0509.DoosanA0509 import DoosanA0509  # noqa: E402
from ir_support_extra_robots.robots.KukaKR4.KukaKR4 import KukaKR4  # noqa: E402
from ir_support_extra_robots.robots.KukaKR5Arc.KukaKR5Arc import KukaKR5Arc  # noqa: E402
from ir_support_extra_robots.robots.KukaKR6R900.KukaKR6R900 import KukaKR6R900  # noqa: E402
from ir_support_extra_robots.robots.KukaTitan.KukaTitan import KukaTitan  # noqa: E402
from ir_support_extra_robots.robots.OmronTM12.OmronTM12 import OmronTM12  # noqa: E402
from ir_support_extra_robots.robots.OmronTM5700.OmronTM5700 import OmronTM5700  # noqa: E402
from ir_support_extra_robots.robots.UR16e.UR16e import UR16e  # noqa: E402


ROBOT_FACTORIES = [
    DoosanA0509,
    DobotNova5,
    UR16e,
    OmronTM12,
    OmronTM5700,
    KukaKR4,
    KukaKR5Arc,
    KukaKR6R900,
    KukaTitan,
    BCN3DMoveo,
]


def test_student_candidate_robot_batch4_loads():
    for factory in ROBOT_FACTORIES:
        robot = factory()
        assert robot.n == len(robot.links)
        assert len(robot.links_3d) == robot.n + 1
        assert np.asarray(robot.q, dtype=float).shape == (robot.n,)

        transforms = robot._get_transforms(robot.q)
        assert len(transforms) == robot.n + 1
        for transform in transforms:
            assert np.asarray(transform).shape == (4, 4)

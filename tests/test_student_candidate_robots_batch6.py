import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.OmronTM12X.OmronTM12X import OmronTM12X
from ir_support_extra_robots.robots.KukaK6R900.KukaK6R900 import KukaK6R900
from ir_support_extra_robots.robots.Kuka361.Kuka361 import Kuka361
from ir_support_extra_robots.robots.KukaAgilusKR.KukaAgilusKR import KukaAgilusKR
from ir_support_extra_robots.robots.JakaZu3.JakaZu3 import JakaZu3

ROBOT_FACTORIES = [
    OmronTM12X,
    KukaK6R900,
    Kuka361,
    KukaAgilusKR,
    JakaZu3,
]


def test_student_candidate_robot_batch6_imports_and_meshes():
    for factory in ROBOT_FACTORIES:
        robot = factory()
        assert robot.n >= 6
        assert len(robot.links_3d) == robot.n + 1
        for mesh in robot.links_3d:
            assert Path(mesh.filename).exists()

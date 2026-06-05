import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.ABBIRB1200.ABBIRB1200 import ABBIRB1200
from ir_support_extra_robots.robots.ABBIRB1100.ABBIRB1100 import ABBIRB1100
from ir_support_extra_robots.robots.ABBIRB910SC.ABBIRB910SC import ABBIRB910SC
from ir_support_extra_robots.robots.EpsonVT6L.EpsonVT6L import EpsonVT6L
from ir_support_extra_robots.robots.UR30.UR30 import UR30
from ir_support_extra_robots.robots.UFactoryXArm6.UFactoryXArm6 import UFactoryXArm6
from ir_support_extra_robots.robots.UFactoryLite6.UFactoryLite6 import UFactoryLite6
from ir_support_extra_robots.robots.KukaLBRiiwa7.KukaLBRiiwa7 import KukaLBRiiwa7

ROBOT_FACTORIES = [ABBIRB1200, ABBIRB1100, ABBIRB910SC, EpsonVT6L, UR30, UFactoryXArm6, UFactoryLite6, KukaLBRiiwa7]


def test_student_candidate_robot_batch7_imports_and_meshes():
    for factory in ROBOT_FACTORIES:
        robot = factory()
        assert robot.n >= 3
        assert len(robot.links_3d) == robot.n + 1
        for mesh in robot.links_3d:
            assert Path(mesh.filename).exists()

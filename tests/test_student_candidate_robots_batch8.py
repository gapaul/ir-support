import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.UR20.UR20 import UR20
from ir_support_extra_robots.robots.YaskawaHC20DTP.YaskawaHC20DTP import YaskawaHC20DTP
from ir_support_extra_robots.robots.PAROL6.PAROL6 import PAROL6
from ir_support_extra_robots.robots.ABBIRB1300.ABBIRB1300 import ABBIRB1300

ROBOT_FACTORIES = [("UR20", UR20), ("YaskawaHC20DTP", YaskawaHC20DTP), ("PAROL6", PAROL6), ("ABBIRB1300", ABBIRB1300)]


def test_student_candidate_robot_batch8_imports_and_meshes():
    for label, factory in ROBOT_FACTORIES:
        robot = factory()
        assert robot.n >= 6
        assert len(robot.links_3d) == robot.n + 1
        for mesh in robot.links_3d:
            assert Path(mesh.filename).exists()

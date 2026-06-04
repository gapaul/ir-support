import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.Pulse75.Pulse75 import Pulse75
from ir_support_extra_robots.robots.MotomanGP7.MotomanGP7 import MotomanGP7
from ir_support_extra_robots.robots.FanucCRX10IAL.FanucCRX10IAL import FanucCRX10IAL
from ir_support_extra_robots.robots.ABBIRB6740_260_300.ABBIRB6740_260_300 import ABBIRB6740_260_300
from ir_support_extra_robots.robots.OmronTM5900.OmronTM5900 import OmronTM5900
from ir_support_extra_robots.robots.KukaKR6R700CR.KukaKR6R700CR import KukaKR6R700CR
from ir_support_extra_robots.robots.KukaKR10.KukaKR10 import KukaKR10

ROBOT_FACTORIES = [
    Pulse75,
    MotomanGP7,
    FanucCRX10IAL,
    ABBIRB6740_260_300,
    OmronTM5900,
    KukaKR6R700CR,
    KukaKR10,
]



def test_student_candidate_robot_batch5_imports_and_meshes():
    for factory in ROBOT_FACTORIES:
        robot = factory()
        assert robot.n >= 6
        assert len(robot.links_3d) == robot.n + 1
        for mesh in robot.links_3d:
            assert Path(mesh.filename).exists()

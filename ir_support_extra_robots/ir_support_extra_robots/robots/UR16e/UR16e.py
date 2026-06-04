import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UR16e(UTSMeshRobot):
    """Candidate Universal Robots UR16e model ported from student work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Universal Robots UR16e, Group_72, 2023S"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.1807, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.4784, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.36, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.17415, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.11985, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.11655, a=0.0, alpha=0.0, offset=0.05, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UR16e",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UR16e",
            home_q=[0.0] * 6,
            base=base,
        )

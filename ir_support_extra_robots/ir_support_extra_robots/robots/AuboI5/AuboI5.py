import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class AuboI5(UTSMeshRobot):
    """Candidate AuboI5 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Aubo i5, Group_11, 2023S"
    manufacturer_url = "https://www.aubo-robotics.com/products/aubo-i5/"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.0985, a=0.0, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.1405, a=0.408, alpha=0.0, offset=pi / 2, qlim=self._qlim(-95, 95)),
    rtb.RevoluteDH(d=-0.1215, a=0.376, alpha=0.0, qlim=self._qlim(-160, 160)),
    rtb.RevoluteDH(d=0.1025, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.1025, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.094, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="AuboI5",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="AuboI5",
            home_q=[0.0] * 6,
            base=base,
        )

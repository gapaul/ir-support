import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DobotCR5(UTSMeshRobot):
    """Candidate DobotCR5 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Dobot CR5, Group_23, 2023S"
    manufacturer_url = "https://www.dobot-robots.com/products/cr-series/cr5.html"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.1348, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.1288, a=-0.274, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=-0.1165, a=0.23, alpha=0.0, offset=pi, qlim=self._qlim(-155, 155)),
    rtb.RevoluteDH(d=0.116, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.116, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.105, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DobotCR5",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DobotCR5",
            home_q=[0.0] * 6,
            base=base,
        )

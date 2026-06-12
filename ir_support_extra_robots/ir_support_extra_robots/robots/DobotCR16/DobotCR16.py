import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DobotCR16(UTSMeshRobot):
    """Candidate DobotCR16 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Dobot CR16, Group_103, 2023S"
    manufacturer_url = "https://www.dobot-robots.com/products/cr-series/cr16.html"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.1765, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.0, a=-0.512, alpha=0.0, qlim=self._qlim(-90, 90)),
    rtb.RevoluteDH(d=0.0, a=-0.363, alpha=0.0, qlim=self._qlim(-170, 170)),
    rtb.RevoluteDH(d=0.125, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.125, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.1084, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DobotCR16",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DobotCR16",
            home_q=[0.0] * 6,
            base=base,
        )

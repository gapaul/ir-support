import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ABBGoFa10(UTSMeshRobot):
    """Candidate ABBGoFa10 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "ABB GoFa 10, Group_13, 2023S"
    manufacturer_url = "https://www.abb.com/global/en/areas/robotics/products/robots/collaborative-robots/gofa"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.4, a=0.15, alpha=pi / 2, qlim=self._qlim(-270, 270)),
    rtb.RevoluteDH(d=0.0, a=0.707, alpha=0.0, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.0, a=-0.11, alpha=-pi / 2, qlim=self._qlim(-225, 85)),
    rtb.RevoluteDH(d=0.637, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.0, a=-0.08, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=self._qlim(-270, 270)),
        ]

        super().__init__(
            links=links,
            mesh_stem="ABBGoFa10",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ABBGoFa10",
            home_q=[0.0] * 6,
            base=base,
        )

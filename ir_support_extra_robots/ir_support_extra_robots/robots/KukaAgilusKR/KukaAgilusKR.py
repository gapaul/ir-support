import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaAgilusKR(UTSMeshRobot):
    """Candidate KUKA Agilus KR model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.

    The source comment says KUKA Agilus but does not pin the exact commercial variant.
    """

    source_note = 'KUKA Agilus-family KR candidate, Group_33, 2023S; original stem KUKAKR'

    def __init__(self, base=None):
        self.link_colors = [(0.04, 0.04, 0.04, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.04, 0.04, 0.04, 1.0)]
        links = [
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.56, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-90, 135)),
            rtb.RevoluteDH(d=0.0, a=-0.035, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-80, 165)),
            rtb.RevoluteDH(d=0.515, a=0.0, alpha=-pi / 2, qlim=self._qlim(-185, 185)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.087, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaAgilusKR",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaAgilusKR",
            home_q=[0.0] * 6,
            base=base,
        )

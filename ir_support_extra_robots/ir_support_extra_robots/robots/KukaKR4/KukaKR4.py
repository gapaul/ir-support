import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaKR4(UTSMeshRobot):
    """Candidate KUKA KR4 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "KUKA KR4, Group_41, 2023S"

    def __init__(self, base=None):
        self.link_colors = [
            (0.08, 0.08, 0.08, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.08, 0.08, 0.08, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.2, a=0.0, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.29, alpha=0.0, qlim=self._qlim(-195, 40)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-65, 30)),
            rtb.RevoluteDH(d=0.23, a=0.0, alpha=pi / 2, qlim=self._qlim(-185, 185)),
            rtb.RevoluteDH(d=0.0, a=0.01, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.025, a=0.0, alpha=0.0, qlim=self._qlim(-350, 350)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaKR4",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaKR4",
            home_q=[0.0] * 6,
            base=base,
        )

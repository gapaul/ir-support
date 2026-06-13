import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DobotNova5(UTSMeshRobot):
    """Candidate DOBOT Nova5 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Dobot Nova5, Group_49, 2023S"
    manufacturer_url = "https://www.dobot-robots.com/products/nova-series/nova5.html"

    def __init__(self, base=None):
        self.link_colors = [
            (0.18, 0.18, 0.18, 1.0),
            (0.96, 0.97, 0.95, 1.0),
            (0.95, 0.41, 0.05, 1.0),
            (0.96, 0.97, 0.95, 1.0),
            (0.95, 0.41, 0.05, 1.0),
            (0.96, 0.97, 0.95, 1.0),
            (0.95, 0.41, 0.05, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.089159, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.425, alpha=0.0, offset=-pi / 2 - pi / 4, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.0, a=-0.39225, alpha=0.0, offset=pi / 2 + pi / 4 + pi / 16, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.10915, a=0.0, alpha=pi / 2, offset=-pi / 8, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.09465, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0823, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DobotNova5",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DobotNova5",
            home_q=[0.0] * 6,
            base=base,
        )

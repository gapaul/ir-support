import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaKR6R900(UTSMeshRobot):
    """Candidate KUKA KR6 R900 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "KUKA KR6 R900, Group_61, 2023S"
    manufacturer_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/kr-agilus"

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
            rtb.RevoluteDH(d=0.4, a=0.025, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.455, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-100, 135)),
            rtb.RevoluteDH(d=0.0, a=0.035, alpha=pi / 2, qlim=self._qlim(-120, 156)),
            rtb.RevoluteDH(d=-0.455, a=0.0, alpha=-pi / 2, qlim=self._qlim(-185, 185)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=-0.08, a=0.0, alpha=pi, qlim=self._qlim(-350, 350)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaKR6R900",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaKR6R900",
            home_q=[0.0] * 6,
            base=base,
        )

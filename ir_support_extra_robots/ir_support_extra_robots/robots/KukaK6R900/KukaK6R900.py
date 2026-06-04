import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaK6R900(UTSMeshRobot):
    """Candidate KUKA K6 R900 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'KUKA K6 R900, Sheila_A2_2, 2024S; original stem KUKA_K6'

    def __init__(self, base=None):
        self.link_colors = [(0.04, 0.04, 0.04, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.04, 0.04, 0.04, 1.0)]
        links = [
            rtb.RevoluteDH(d=0.33825, a=0.12652, alpha=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.019332, a=0.34, alpha=0.0, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=-0.025, a=-0.02, alpha=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.33, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=-0.013, a=0.0, alpha=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.068, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaK6R900",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaK6R900",
            home_q=[0.0] * 6,
            base=base,
        )

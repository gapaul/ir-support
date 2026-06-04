import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class JakaZu3(UTSMeshRobot):
    """Candidate JAKA Zu3 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'JAKA Zu3, Group_24, 2023S; source cites JAKA Zu3 STEP files and Zhenyu Liu et al. 2023 DH parameters'

    def __init__(self, base=None):
        self.link_colors = [(0.04, 0.04, 0.04, 1.0), (0.82, 0.84, 0.82, 1.0), (0.82, 0.84, 0.82, 1.0), (0.05, 0.22, 0.55, 1.0), (0.82, 0.84, 0.82, 1.0), (0.05, 0.22, 0.55, 1.0), (0.04, 0.04, 0.04, 1.0)]
        links = [
            rtb.RevoluteDH(d=0.1506, a=0.0, alpha=pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.0, a=0.2460, alpha=0.0, qlim=self._qlim(-85, 265)),
            rtb.RevoluteDH(d=0.0, a=0.2280, alpha=0.0, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=0.1175, a=0.0, alpha=pi / 2, qlim=self._qlim(-85, 265)),
            rtb.RevoluteDH(d=0.1175, a=0.0, alpha=-pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.1050, a=0.0, alpha=0.0, qlim=self._qlim(-270, 270)),
        ]

        super().__init__(
            links=links,
            mesh_stem="JakaZu3",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="JakaZu3",
            home_q=[0.0] * 6,
            base=base,
        )

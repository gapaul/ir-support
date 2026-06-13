import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaKR10(UTSMeshRobot):
    """Candidate KUKA KR10 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'KUKA KR10, Khoa_A2_8, 2024S; using the Draft 3 link mesh set'
    reference_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/kr-agilus"

    def __init__(self, base=None):
        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.55, alpha=0.0, offset=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.0, a=-0.025, alpha=-pi / 2, offset=pi, qlim=self._qlim(-50, 150)),
            rtb.RevoluteDH(d=0.515, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-100, 100)),
            rtb.RevoluteDH(d=0.09, a=0.0, alpha=0.0, qlim=self._qlim(-180, 180)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaKR10",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaKR10",
            home_q=[0.0] * 6,
            base=base,
        )

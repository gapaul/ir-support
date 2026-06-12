import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaKR5Arc(UTSMeshRobot):
    """Candidate KUKA KR5 Arc model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "KUKA KR5 Arc, Danial_A2_5 and related 2024S submissions"
    reference_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/kr-cybertech-arc"

    def __init__(self, base=None):
        self.link_colors = [
            (0.08, 0.08, 0.08, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.4, a=0.18, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.135, a=0.6, alpha=pi, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.135, a=0.12, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.62, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaKR5Arc",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaKR5Arc",
            home_q=[0.0] * 6,
            base=base,
        )

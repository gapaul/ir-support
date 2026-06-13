import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DobotNova2(UTSMeshRobot):
    """Candidate DOBOT Nova2 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Dobot Nova2, Danial_A2_2, 2024S'
    manufacturer_url = "https://www.dobot-robots.com/products/nova-series/nova2.html"

    def __init__(self, base=None):
        self.link_colors = [
            (0.22, 0.23, 0.22, 1.0),
            (0.95, 0.33, 0.04, 1.0),
            (0.95, 0.33, 0.04, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.95, 0.33, 0.04, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.95, 0.33, 0.04, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.2234, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.28, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.225, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1175, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.12, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.088, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DobotNova2",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DobotNova2",
            home_q=[0.0] * 6,
            base=base,
        )

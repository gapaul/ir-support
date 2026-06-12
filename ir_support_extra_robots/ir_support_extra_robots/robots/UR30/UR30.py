import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UR30(UTSMeshRobot):
    """Candidate Universal Robots UR30 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Universal Robots UR30, Katia_A2_5, 2024S'
    manufacturer_url = "https://www.universal-robots.com/products/ur30/"

    def __init__(self, base=None):
        self.link_colors = [
            (0.28, 0.29, 0.28, 1.0),
            (0.91, 0.93, 0.91, 1.0),
            (0.45, 0.85, 0.95, 1.0),
            (0.91, 0.93, 0.91, 1.0),
            (0.45, 0.85, 0.95, 1.0),
            (0.91, 0.93, 0.91, 1.0),
            (0.45, 0.85, 0.95, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.2363, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.637, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.5037, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.201, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1593, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1543, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UR30",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UR30",
            home_q=[0.0] * 6,
            base=base,
        )

import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ABBIRB1100(UTSMeshRobot):
    """Candidate ABB IRB 1100 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'ABB IRB 1100, Group_2, 2023S'
    manufacturer_url = "https://www.abb.com/global/en/areas/robotics/products/robots/articulated-robots/small-robots/irb-1100"

    def __init__(self, base=None):
        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.325433, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.28, alpha=0.0, offset=pi / 2, qlim=self._qlim(-130, 130)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-110, 70)),
            rtb.RevoluteDH(d=0.299, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.056, a=0.0, alpha=0.0, qlim=self._qlim(-400, 400)),
        ]

        super().__init__(
            links=links,
            mesh_stem="ABBIRB1100",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ABBIRB1100",
            home_q=[0.0] * 6,
            base=base,
        )

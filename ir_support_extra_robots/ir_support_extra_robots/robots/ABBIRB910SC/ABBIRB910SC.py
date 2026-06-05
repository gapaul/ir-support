import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ABBIRB910SC(UTSMeshRobot):
    """Candidate ABB IRB 910SC model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'ABB IRB 910SC SCARA candidate, Group_114, 2023S'

    def __init__(self, base=None):
        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.04, 0.04, 0.04, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.1916, a=0.3, alpha=0.0, qlim=self._qlim(-140, 140)),
            rtb.RevoluteDH(d=0.0661, a=0.25, alpha=0.0, qlim=self._qlim(-150, 150)),
            rtb.PrismaticDH(theta=0.0, a=0.0, alpha=0.0, qlim=[-0.18, 0.0]),
        ]

        super().__init__(
            links=links,
            mesh_stem="ABBIRB910SC",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ABBIRB910SC",
            home_q=[0.0] * 3,
            base=base,
        )

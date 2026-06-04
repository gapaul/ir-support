import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class OmronTM5900(UTSMeshRobot):
    """Candidate Omron TM5-900 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Omron TM5-900, Group_70, 2023S; using the full TM5 link mesh set'

    def __init__(self, base=None):
        self.link_colors = [
            (0.38, 0.39, 0.37, 1.0),
            (0.2, 0.21, 0.2, 1.0),
            (0.38, 0.39, 0.37, 1.0),
            (0.38, 0.39, 0.37, 1.0),
            (0.2, 0.21, 0.2, 1.0),
            (0.38, 0.39, 0.37, 1.0),
            (0.91, 0.93, 0.91, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.1452, a=0.0, alpha=pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.0, a=-0.429, alpha=0.0, qlim=self._qlim(-180, 0)),
            rtb.RevoluteDH(d=0.0, a=-0.4115, alpha=0.0, qlim=self._qlim(-155, 155)),
            rtb.RevoluteDH(d=0.106, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.106, a=0.0, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.1135, a=0.0, alpha=0.0, qlim=self._qlim(-270, 270)),
        ]

        super().__init__(
            links=links,
            mesh_stem="OmronTM5900",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="OmronTM5900",
            home_q=[0.0] * 6,
            base=base,
        )

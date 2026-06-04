import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class OmronTM12(UTSMeshRobot):
    """Candidate Omron TM12 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Omron TM12, Group_1 and Group_37, 2023S"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.1652, a=0.0, alpha=pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.0, a=-0.6361, alpha=0.0, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=-0.5579, alpha=0.0, qlim=self._qlim(-155, 155)),
            rtb.RevoluteDH(d=0.13, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.106, a=0.0, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.23, a=0.0, alpha=0.0, offset=pi, qlim=self._qlim(-270, 270)),
        ]

        super().__init__(
            links=links,
            mesh_stem="OmronTM12",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="OmronTM12",
            home_q=[0.0] * 6,
            base=base,
        )

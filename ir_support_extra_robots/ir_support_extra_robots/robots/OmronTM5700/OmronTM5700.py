import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class OmronTM5700(UTSMeshRobot):
    """Candidate Omron TM5-700 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Omron TM5-700, Group_14, 2023S"

    def __init__(self, base=None):
        self.link_colors = [
            (0.42, 0.43, 0.41, 1.0),
            (0.18, 0.19, 0.18, 1.0),
            (0.28, 0.29, 0.27, 1.0),
            (0.30, 0.31, 0.29, 1.0),
            (0.22, 0.23, 0.22, 1.0),
            (0.36, 0.37, 0.35, 1.0),
            (0.78, 0.80, 0.78, 1.0),
        ]

        links = [
            rtb.RevoluteDH(d=0.1452, a=0.0, alpha=pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.146, a=0.329, alpha=0.0, offset=0, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=-0.1297, a=0.3115, alpha=0.0, qlim=self._qlim(-155, 155)),
            rtb.RevoluteDH(d=0.106, a=0.0, alpha=-pi / 2, offset=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.106, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.1132, a=0.0, alpha=0.0, qlim=self._qlim(-270, 270)),
        ]

        super().__init__(
            links=links,
            mesh_stem="OmronTM5700",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="OmronTM5700",
            home_q=[0.0] * 6,
            base=base,
        )

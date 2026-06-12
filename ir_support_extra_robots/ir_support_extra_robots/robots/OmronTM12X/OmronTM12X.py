import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class OmronTM12X(UTSMeshRobot):
    """Candidate Omron TM12X model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Omron/Techman TM12X, Group_69, 2023S; original stem omron_tm12x'
    manufacturer_url = "https://automation.omron.com/en/us/products/family/TM_Series_Collaborative_Robots"

    def __init__(self, base=None):
        self.link_colors = [(0.24, 0.25, 0.24, 1.0), (0.24, 0.25, 0.24, 1.0), (0.24, 0.25, 0.24, 1.0), (0.88, 0.88, 0.86, 1.0), (0.24, 0.25, 0.24, 1.0), (0.88, 0.88, 0.86, 1.0), (0.02, 0.13, 0.34, 1.0)]
        links = [
            rtb.RevoluteDH(d=0.1652, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.6361, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.5579, alpha=0.0, qlim=self._qlim(-166, 166)),
            rtb.RevoluteDH(d=0.120, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.106, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1132, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="OmronTM12X",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="OmronTM12X",
            home_q=[0.0] * 6,
            base=base,
        )

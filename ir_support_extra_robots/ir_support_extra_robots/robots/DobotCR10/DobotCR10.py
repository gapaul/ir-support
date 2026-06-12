import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DobotCR10(UTSMeshRobot):
    """Candidate DOBOT CR10 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Dobot CR10, Group_58, 2023S'
    manufacturer_url = "https://www.dobot-robots.com/products/cr-series/cr10.html"

    def __init__(self, base=None):
        self.link_colors = [
            (0.46, 0.48, 0.47, 1.0),
            (0.46, 0.48, 0.47, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.46, 0.48, 0.47, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.46, 0.48, 0.47, 1.0),
            (0.9, 0.92, 0.9, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.1765, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.125, a=-0.607, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=-0.125, a=0.568, alpha=0.0, offset=pi, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.125, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.125, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1114, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DobotCR10",
                    mesh_dir=os.path.abspath(os.path.dirname(__file__)),
                    name="DobotCR10",
                    home_q=[0.0] * 6,
                    base=base,
                )


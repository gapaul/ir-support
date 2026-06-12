import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DensoVS068(UTSMeshRobot):
    """Candidate DENSO VS068 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'DENSO VS068, Khoa_A2_7, 2024S'
    manufacturer_url = "https://www.denso-wave.com/en/robot/product/five-six/vs.html"

    def __init__(self, base=None):
        self.link_colors = [
            (0.22, 0.23, 0.22, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.03, 0.28, 0.72, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.03, 0.28, 0.72, 1.0),
            (0.9, 0.92, 0.9, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.148, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.305, alpha=0.0, offset=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-125, 155)),
            rtb.RevoluteDH(d=0.3, a=0.0, alpha=pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, offset=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.06, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DensoVS068",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DensoVS068",
            home_q=[0.0] * 6,
            base=base,
        )

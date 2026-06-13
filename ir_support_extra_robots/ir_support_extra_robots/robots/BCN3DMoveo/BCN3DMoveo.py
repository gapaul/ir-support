import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class BCN3DMoveo(UTSMeshRobot):
    """Candidate BCN3D Moveo model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "BCN3D Moveo, Group_36, 2023S"
    reference_url = "https://github.com/BCN3D/BCN3D-Moveo"

    def __init__(self, base=None):
        self.link_colors = [
            (0.055, 0.06, 0.06, 1.0),
            (0.055, 0.06, 0.06, 1.0),
            (0.02, 0.36, 0.75, 1.0),
            (0.02, 0.36, 0.75, 1.0),
            (0.055, 0.06, 0.06, 1.0),
            (0.72, 0.74, 0.72, 1.0),
            (0.02, 0.36, 0.75, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.22, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.225, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.13, a=0.0, alpha=0.0, qlim=self._qlim(0, 0)),
            rtb.RevoluteDH(d=0.09, a=0.0, alpha=-pi / 2, offset=pi, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0425, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-90, 90)),
        ]

        super().__init__(
            links=links,
            mesh_stem="BCN3DMoveo",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="BCN3DMoveo",
            home_q=[0.0] * 6,
            base=base,
        )

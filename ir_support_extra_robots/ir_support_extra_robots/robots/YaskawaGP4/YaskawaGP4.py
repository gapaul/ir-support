import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class YaskawaGP4(UTSMeshRobot):
    """Candidate YaskawaGP4 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Yaskawa GP4, Group_48, 2023S"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.33, a=0.0, alpha=pi / 2, qlim=self._qlim(-170, 170)),
    rtb.RevoluteDH(d=0.0, a=0.26, alpha=0.0, offset=pi / 2, qlim=self._qlim(-110, 130)),
    rtb.RevoluteDH(d=0.0, a=-0.015, alpha=-pi / 2, offset=pi, qlim=self._qlim(-200, 65)),
    rtb.RevoluteDH(d=-0.29, a=0.0, alpha=-pi / 2, qlim=self._qlim(-200, 200)),
    rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-123, 123)),
    rtb.RevoluteDH(d=-0.072, a=0.0, alpha=pi, offset=pi, qlim=self._qlim(-455, 455)),
        ]

        super().__init__(
            links=links,
            mesh_stem="YaskawaGP4",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="YaskawaGP4",
            home_q=[0.0] * 6,
            base=base,
        )

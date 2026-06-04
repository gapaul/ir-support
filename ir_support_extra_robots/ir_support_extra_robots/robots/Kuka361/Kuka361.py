import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class Kuka361(UTSMeshRobot):
    """Candidate Kuka361 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.

    The source code did not identify the exact KUKA product model; the student name is preserved.
    """

    source_note = 'Kuka361 / Kuker student KUKA candidate, Katia_A2_2, 2024S; exact commercial model identity not verified'

    def __init__(self, base=None):
        self.link_colors = [(0.04, 0.04, 0.04, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.92, 0.34, 0.02, 1.0), (0.04, 0.04, 0.04, 1.0)]
        links = [
            rtb.RevoluteDH(d=1.045, a=0.5, alpha=-pi / 2, qlim=self._qlim(-185, 185)),
            rtb.RevoluteDH(d=0.0, a=1.210, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-130, 20)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-190, 54)),
            rtb.RevoluteDH(d=1.025, a=0.0, alpha=-pi / 2, qlim=self._qlim(-350, 350)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.3, a=0.0, alpha=0.0, qlim=self._qlim(-350, 350)),
        ]

        super().__init__(
            links=links,
            mesh_stem="Kuka361",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="Kuka361",
            home_q=[0.0] * 6,
            base=base,
        )

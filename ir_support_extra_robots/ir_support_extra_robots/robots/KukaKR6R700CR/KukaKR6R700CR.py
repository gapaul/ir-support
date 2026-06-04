import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaKR6R700CR(UTSMeshRobot):
    """Candidate KUKA KR6 R700 CR model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'KUKA KR6 R700 CR, Group_8, 2023S'

    def __init__(self, base=None):
        base_adjust = SE3(0, 0, 0.20)
        if base is None:
            base = base_adjust
        elif isinstance(base, SE3):
            base = base * base_adjust
        else:
            base = SE3(np.asarray(base, dtype=float), check=False) * base_adjust

        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.183, a=0.025, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=-0.315, alpha=0.0, qlim=self._qlim(-10, 225)),
            rtb.RevoluteDH(d=0.0, a=-0.035, alpha=pi / 2, qlim=self._qlim(-120, 156)),
            rtb.RevoluteDH(d=0.365, a=0.0, alpha=-pi / 2, qlim=self._qlim(-185, 185)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.08, a=0.0, alpha=0.0, qlim=self._qlim(-350, 350)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaKR6R700CR",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaKR6R700CR",
            home_q=[0.0] * 6,
            base=base,
        )

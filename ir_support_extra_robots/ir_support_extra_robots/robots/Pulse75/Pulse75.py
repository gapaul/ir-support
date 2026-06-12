import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class Pulse75(UTSMeshRobot):
    """Candidate Rozum Robotics PULSE 75 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Rozum Robotics PULSE 75, Group_68, 2023S; rail-style prismatic first joint removed, rail plates trimmed from the base mesh, and base lowered onto the xy plane for the IR Support candidate model'
    manufacturer_url = "https://rozum.com/robotic-arm-pulse-75/"

    def __init__(self, base=None):
        base_adjust = SE3(0, 0, -0.06996) * SE3.Rx(pi / 2) * SE3.Ry(pi / 2) * SE3.Rz(pi) * SE3.Rx(pi / 2)
        if base is None:
            base = base_adjust
        elif isinstance(base, SE3):
            base = base * base_adjust
        else:
            base = SE3(np.asarray(base, dtype=float), check=False) * base_adjust

        self.link_colors = [
            (0.02, 0.02, 0.02, 1.0),
            (0.82, 0.84, 0.82, 1.0),
            (0.02, 0.02, 0.02, 1.0),
            (0.82, 0.84, 0.82, 1.0),
            (0.02, 0.02, 0.02, 1.0),
            (0.82, 0.84, 0.82, 1.0),
            (0.02, 0.02, 0.02, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.2725, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.135, a=-0.375, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=-0.115, a=-0.295, alpha=0.0, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.115, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1711, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1226, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="Pulse75",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="Pulse75",
            home_q=[0.0] * 6,
            base=base,
        )

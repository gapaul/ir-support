import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UFactoryXArm6(UTSMeshRobot):
    """Candidate uFactory xArm6 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'uFactory xArm6, Sheila_A2_7, 2024S'
    manufacturer_url = "https://www.ufactory.cc/xarm-collaborative-robot/"

    def __init__(self, base=None):
        self.link_colors = [
            (0.28, 0.29, 0.28, 1.0),
            (0.91, 0.93, 0.91, 1.0),
            (0.74, 0.76, 0.74, 1.0),
            (0.91, 0.93, 0.91, 1.0),
            (0.74, 0.76, 0.74, 1.0),
            (0.91, 0.93, 0.91, 1.0),
            (0.28, 0.29, 0.28, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.267, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.2895, alpha=0.0, offset=-79 * pi / 180, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0775, alpha=-pi / 2, offset=79 * pi / 180, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.3425, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.076, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.097, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UFactoryXArm6",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UFactoryXArm6",
            home_q=[0.0, 79 * pi / 180, -79 * pi / 180, 0.0, 0.0, 0.0],
            base=base,
        )

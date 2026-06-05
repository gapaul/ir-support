import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UFactoryLite6(UTSMeshRobot):
    """Candidate uFactory Lite6 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'uFactory Lite6, Group_5, 2023S; prismatic rail stripped from the original LinearLite6 source; first DH height adjusted to the standalone Lite6 value'

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
            rtb.RevoluteDH(d=0.2433, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.198, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.09, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=-0.227, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UFactoryLite6",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UFactoryLite6",
            home_q=[0.0] * 6,
            base=base,
        )

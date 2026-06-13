import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UnitreeZ1(UTSMeshRobot):
    """Candidate Unitree Z1 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    link_colors = [(0.04, 0.05, 0.06, 1.0),
             (0.55, 0.56, 0.55, 1.0),
             (0.76, 0.78, 0.76, 1.0),
             (0.56, 0.58, 0.57, 1.0),
             (0.3, 0.32, 0.32, 1.0),
             (0.2, 0.22, 0.22, 1.0),
             (0.04, 0.05, 0.06, 1.0)]

    source_note = "Unitree Z1, A2_Tan_8_DineshS_DanishS_MahakS, 2025S"
    manufacturer_url = "https://www.unitree.com/z1"

    def __init__(self, base=None):
        links = [

            rtb.RevoluteDH(d=0.068, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=-0.008, a=-0.243, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=-0.003, a=-0.215, alpha=0.0, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.117, a=0.0, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.09, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0823, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UnitreeZ1",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UnitreeZ1",
            home_q=[0.0] * 6,
            base=base,
        )

import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ProSixVT6(UTSMeshRobot):
    """Candidate Epson ProSix VT6 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "ProSix VT6, A2_Tan_8_DineshS_DanishS_MahakS, 2025S"

    def __init__(self, base=None):
        links = [

            rtb.RevoluteDH(d=0.2438, a=0.0004, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-154.1005, 154.1001)),
            rtb.RevoluteDH(d=0.0305, a=0.2803, alpha=0.0, offset=pi / 2, qlim=self._qlim(-150.1003, 150.1003)),
            rtb.RevoluteDH(d=-0.0203, a=0.0005, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-150.1005, 150.1005)),
            rtb.RevoluteDH(d=-0.2452, a=0.0001, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-148.98002, 148.9801)),
            rtb.RevoluteDH(d=0.0572, a=0.0006, alpha=pi / 2, qlim=self._qlim(-144.97002, 145.0005)),
            rtb.RevoluteDH(d=0.2626, a=0.0005, alpha=0.0, qlim=self._qlim(-148.98004, 148.9804)),
        ]

        super().__init__(
            links=links,
            mesh_stem="ProSixVT6",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ProSixVT6",
            home_q=[0.0] * 6,
            base=base,
        )

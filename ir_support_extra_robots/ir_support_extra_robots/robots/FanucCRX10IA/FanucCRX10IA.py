import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class FanucCRX10IA(UTSMeshRobot):
    """Candidate FanucCRX10IA model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "FANUC CRX-10iA, Victor_A2_9, 2024S; final fixed gripper link omitted from DH chain"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.2503, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
    rtb.RevoluteDH(d=0.2604, a=0.71, alpha=-pi, offset=pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.2604, a=0.0, alpha=-pi / 2, offset=pi, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.54, a=0.0, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.15, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.16, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="FanucCRX10IA",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="FanucCRX10IA",
            home_q=[0.0] * 6,
            base=base,
        )

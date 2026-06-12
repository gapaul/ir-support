import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class FanucLRMate200iD(UTSMeshRobot):
    """Candidate FanucLRMate200iD model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "FANUC LR Mate 200iD, Tony_A2_2, 2024S"
    manufacturer_url = "https://www.fanucamerica.com/products/robots/series/lr-mate/lr-mate-200id"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.325, a=0.05, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.0, a=0.331, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-90, 90)),
    rtb.RevoluteDH(d=0.0, a=0.035, alpha=-pi / 2, qlim=self._qlim(-90, 90)),
    rtb.RevoluteDH(d=0.3343, a=0.0, alpha=pi / 2, qlim=self._qlim(-90, 90)),
    rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-90, 90)),
    rtb.RevoluteDH(d=0.07, a=0.0, alpha=0.0, qlim=self._qlim(-90, 90)),
        ]

        super().__init__(
            links=links,
            mesh_stem="FanucLRMate200iD",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="FanucLRMate200iD",
            home_q=[0.0] * 6,
            base=base,
        )

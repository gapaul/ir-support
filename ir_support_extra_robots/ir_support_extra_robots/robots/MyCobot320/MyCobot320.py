import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class MyCobot320(UTSMeshRobot):
    """Candidate Elephant Robotics MyCobot 320 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    link_colors = [(0.05, 0.05, 0.05, 1.0),
             (0.94, 0.94, 0.92, 1.0),
             (0.12, 0.12, 0.12, 1.0),
             (0.94, 0.94, 0.92, 1.0),
             (0.12, 0.12, 0.12, 1.0),
             (0.94, 0.94, 0.92, 1.0),
             (0.05, 0.05, 0.05, 1.0)]

    source_note = "MyCobot320, A2_Tan_8_DineshS_DanishS_MahakS, 2025S"
    manufacturer_url = "https://www.elephantrobotics.com/en/mycobot-320/"

    def __init__(self, base=None):
        links = [

            rtb.RevoluteDH(d=0.17866, a=0.0, alpha=pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=-0.005, a=0.136, alpha=0.0, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=-0.1, a=0.005, alpha=0.0, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.08515, a=0.099, alpha=-pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.099, a=0.0, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=-0.0619, a=0.0, alpha=pi, qlim=self._qlim(-175, 175)),
        ]

        super().__init__(
            links=links,
            mesh_stem="MyCobot320",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="MyCobot320",
            home_q=[0.0] * 6,
            base=base,
        )

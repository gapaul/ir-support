import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ABBIRB1520ID(UTSMeshRobot):
    """Candidate ABB IRB 1520ID model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    The submitted terminal tool offset has been shortened to keep the visual
    wrist flange attached to the robot arm.
    """

    source_note = 'ABB IRB 1520ID, Tony_A2_1, 2024S'
    manufacturer_url = "https://www.abb.com/global/en/areas/robotics/products/robots/articulated-robots/medium-robots/irb-1520id"

    def __init__(self, base=None):
        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.04, 0.04, 0.04, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.453, a=0.16, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.59, alpha=0.0, offset=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.2, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.723, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.21, a=-0.02, alpha=pi / 2, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="ABBIRB1520ID",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ABBIRB1520ID",
            home_q=[0.0] * 6,
            base=base,
        )

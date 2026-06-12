import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaTitan(UTSMeshRobot):
    """Candidate KUKA Titan model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "KUKA Titan, Karlos_A2_1, 2024S"
    manufacturer_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/kr-titan"

    def __init__(self, base=None):
        self.link_colors = [
            (0.08, 0.08, 0.08, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.92, 0.34, 0.02, 1.0),
            (0.08, 0.08, 0.08, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=1.1, a=0.6, alpha=-pi / 2, qlim=self._qlim(-150, 150)),
            rtb.RevoluteDH(d=0.0, a=1.465, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-40, 107.5)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-200, 55)),
            rtb.RevoluteDH(d=1.2, a=0.0, alpha=-pi / 2, qlim=self._qlim(-350, 350)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-118, 118)),
            rtb.RevoluteDH(d=0.372, a=0.0, alpha=0.0, qlim=self._qlim(-350, 350)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaTitan",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaTitan",
            home_q=[0.0] * 6,
            base=base,
            meshes_are_global_at_home=True,
        )

import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaLBRiiwa14(UTSMeshRobot):
    """Candidate KUKA LBR iiwa 14 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'KUKA LBR iiwa 14, Group_51, 2023S; Robotiq gripper assets omitted'
    manufacturer_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/lbr-iiwa"

    def __init__(self, base=None):
        self.link_colors = [
            (0.92, 0.34, 0.02, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.92, 0.34, 0.02, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.36, a=0.0, alpha=-pi / 2, offset=100 * pi / 180, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.42, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.126, a=0.0, alpha=0.0, qlim=self._qlim(-180, 180)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaLBRiiwa14",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaLBRiiwa14",
            home_q=[0.0] * 7,
            base=base,
        )

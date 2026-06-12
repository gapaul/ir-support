import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaLBRiiwa7(UTSMeshRobot):
    """Candidate KUKA LBR iiwa 7 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'KUKA LBR iiwa 7, Group_38, 2023S'
    manufacturer_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/lbr-iiwa"

    def __init__(self, base=None):
        self.link_colors = [
            (0.22, 0.23, 0.23, 1.0),
            (0.82, 0.84, 0.82, 1.0),
            (0.95, 0.38, 0.02, 1.0),
            (0.82, 0.84, 0.82, 1.0),
            (0.95, 0.38, 0.02, 1.0),
            (0.82, 0.84, 0.82, 1.0),
            (0.95, 0.38, 0.02, 1.0),
            (0.22, 0.23, 0.23, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.34, a=0.0, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.126, a=0.0, alpha=0.0, qlim=self._qlim(-175, 175)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KukaLBRiiwa7",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaLBRiiwa7",
            home_q=[0.0] * 7,
            base=base,
        )

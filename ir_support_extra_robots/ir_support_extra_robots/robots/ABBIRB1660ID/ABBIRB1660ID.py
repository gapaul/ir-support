import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ABBIRB1660ID(UTSMeshRobot):
    """Candidate ABB IRB 1660ID model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    The student rail joint has been omitted, and the arm DH convention has
    been corrected to keep the global-home visual meshes attached while moving.
    """

    source_note = 'ABB IRB 1660ID, Group_63, 2023S; original student rail variant omitted and arm meshes scaled from millimetres'
    manufacturer_url = "https://www.abb.com/global/en/areas/robotics/products/robots/articulated-robots/medium-robots/irb-1660id"

    def __init__(self, base=None):
        self.link_colors = [
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.04, 0.04, 0.04, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.4865, a=0.15, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.7, alpha=0.0, offset=pi / 2, qlim=self._qlim(-90, 150)),
            rtb.RevoluteDH(d=0.0, a=0.11, alpha=pi / 2, qlim=self._qlim(-238, 79)),
            rtb.RevoluteDH(d=0.678, a=0.0, alpha=pi / 2, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.12, a=0.0, alpha=pi / 2, qlim=self._qlim(-400, 400)),
        ]

        super().__init__(
            links=links,
            mesh_stem="ABBIRB1660ID",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ABBIRB1660ID",
            home_q=[0.0] * 6,
            base=base,
            meshes_are_global_at_home=True,
        )


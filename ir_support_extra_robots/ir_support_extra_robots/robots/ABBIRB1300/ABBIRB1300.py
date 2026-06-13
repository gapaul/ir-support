import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class ABBIRB1300(UTSMeshRobot):
    """Candidate ABB IRB 1300 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'ABB 1300-class candidate from a student folder named CRB1300, A2_AnhMinh_46_PhuTrungN_NhatThienM_MohammadFaiyadH, 2025S; source DAE meshes were authored in millimetres and scaled to metres'
    manufacturer_url = "https://www.abb.com/global/en/areas/robotics/products/robots/articulated-robots/small-robots/irb-1300"

    def __init__(self, base=None):
        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
            (0.98, 0.42, 0.03, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.544, a=0.0, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.425, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-95, 155)),
            rtb.RevoluteDH(d=0.0, a=-0.04, alpha=pi / 2, offset=-pi, qlim=self._qlim(-210, 69)),
            rtb.RevoluteDH(d=0.475, a=0.0, alpha=-pi / 2, qlim=self._qlim(-230, 230)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-130, 130)),
            rtb.RevoluteDH(d=0.09, a=0.0, alpha=0.0, qlim=self._qlim(-400, 400)),
        ]

        super().__init__(
            links=links,
            mesh_stem="ABBIRB1300",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="ABBIRB1300",
            home_q=[0.0] * 6,
            base=base,
            meshes_are_global_at_home=True,
        )

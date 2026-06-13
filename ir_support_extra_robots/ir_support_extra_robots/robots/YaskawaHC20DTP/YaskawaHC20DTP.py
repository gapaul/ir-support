import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class YaskawaHC20DTP(UTSMeshRobot):
    """Candidate Yaskawa HC20DTP model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Yaskawa HC20DTP, Group_60, 2023S; source cites Yaskawa HC20DTP datasheet dimensions'
    manufacturer_url = "https://www.motoman.com/en-us/products/robots/collaborative/hc-series/hc20dtp"

    def __init__(self, base=None):
        self.link_colors = [
            (0.16, 0.16, 0.15, 1.0),
            (0.40, 0.41, 0.39, 1.0),
            (0.44, 0.45, 0.43, 1.0),
            (0.46, 0.47, 0.45, 1.0),
            (0.88, 0.89, 0.86, 1.0),
            (0.44, 0.45, 0.43, 1.0),
            (0.16, 0.16, 0.15, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.38, a=0.0, alpha=pi / 2, qlim=self._qlim(-210, 210)),
            rtb.RevoluteDH(d=0.0, a=0.82, alpha=0.0, offset=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, offset=pi, qlim=self._qlim(-67, 247)),
            rtb.RevoluteDH(d=0.88, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-210, 210)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.2, a=0.0, alpha=0.0, qlim=self._qlim(-210, 210)),
        ]

        super().__init__(
            links=links,
            mesh_stem="YaskawaHC20DTP",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="YaskawaHC20DTP",
            home_q=[0.0] * 6,
            base=base,
        )

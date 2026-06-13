import os
from math import pi

import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DoosanA0509(UTSMeshRobot):
    """Candidate Doosan A0509 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Doosan A0509, Group_75, 2023S"
    manufacturer_url = "https://www.doosanrobotics.com/en/products/a-series/a0509"

    def __init__(self, base=None):
        self.link_colors = [
            (0.48, 0.50, 0.50, 1.0),
            (0.90, 0.91, 0.89, 1.0),
            (0.92, 0.93, 0.91, 1.0),
            (0.90, 0.91, 0.89, 1.0),
            (0.92, 0.93, 0.91, 1.0),
            (0.88, 0.89, 0.87, 1.0),
            (0.34, 0.35, 0.35, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.155, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.409, alpha=0.0, offset=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.367, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.127, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]
        mount = SE3.Rz(pi)
        resolved_base = mount if base is None else self._as_se3(base) * mount

        super().__init__(
            links=links,
            mesh_stem="DoosanA0509",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DoosanA0509",
            home_q=[0.0] * 6,
            base=resolved_base,
        )

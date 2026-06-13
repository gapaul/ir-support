import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class FanucCRX5IA(UTSMeshRobot):
    """Candidate FanucCRX5IA model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "FANUC CRX-5iA candidate, Group_9, 2023S"
    manufacturer_url = "https://www.fanucamerica.com/products/robots/series/collaborative-robots/crx-5ia-cobot"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.18, a=0.0, alpha=pi / 2, qlim=self._qlim(-200, 200)),
    rtb.RevoluteDH(d=0.095, a=0.41, alpha=-pi, offset=pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.1, a=0.0, alpha=-pi / 2, qlim=self._qlim(-317.5, 317.5)),
    rtb.RevoluteDH(d=0.43, a=0.0, alpha=-pi / 2, qlim=self._qlim(-190, 190)),
    rtb.RevoluteDH(d=0.13, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
    rtb.RevoluteDH(d=0.145, a=0.0, alpha=0.0, qlim=self._qlim(-225, 225)),
        ]

        super().__init__(
            links=links,
            mesh_stem="FanucCRX5IA",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="FanucCRX5IA",
            home_q=[0.0] * 6,
            base=base,
        )

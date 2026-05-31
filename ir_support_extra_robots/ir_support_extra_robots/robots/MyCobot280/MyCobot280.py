import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class MyCobot280(UTSMeshRobot):
    """MyCobot 280 model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.13156, a=0.0, alpha=pi / 2, qlim=self._qlim(-165, 165)),
            rtb.RevoluteDH(d=-0.06639, a=0.1104, alpha=0.0, qlim=self._qlim(-165, 165)),
            rtb.RevoluteDH(d=0.06639, a=0.096, alpha=0.0, qlim=self._qlim(-165, 165)),
            rtb.RevoluteDH(d=-0.06639, a=0.0, alpha=-pi / 2, qlim=self._qlim(-165, 165)),
            rtb.RevoluteDH(d=0.07318, a=0.0, alpha=-pi / 2, qlim=self._qlim(-165, 165)),
            rtb.RevoluteDH(d=-0.0436, a=0.0, alpha=0.0, qlim=self._qlim(-175, 175)),
        ]

        super().__init__(
            links=links,
            mesh_stem="MyCobot280",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="MyCobot280",
            home_q=[0.0] * 6,
            base=base,
        )

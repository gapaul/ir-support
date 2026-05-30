import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DensoVM6083(UTSMeshRobot):
    """Denso VM6083 model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.475, a=0.180, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.385, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-90, 135)),
            rtb.RevoluteDH(d=0.0, a=-0.100, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-80, 165)),
            rtb.RevoluteDH(d=0.445, a=0.0, alpha=-pi / 2, qlim=self._qlim(-185, 185)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.09, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DensoVM6083",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DensoVM6083",
            home_q=[0.0] * 6,
            base=base,
        )

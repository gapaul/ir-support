import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UR10(UTSMeshRobot):
    """Universal Robots UR10 model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.128, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.6127, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.5716, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.16389, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1157, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.09037, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UR10",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UR10",
            home_q=[0.0, -pi / 2, 0.0, 0.0, 0.0, 0.0],
            base=base,
        )

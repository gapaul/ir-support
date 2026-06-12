import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UR5e(UTSMeshRobot):
    """Universal Robots UR5e model ported from the UTS MATLAB toolbox."""
    manufacturer_url = "https://www.universal-robots.com/products/ur5e/"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.1625, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.425, alpha=0.0, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.0, a=-0.3922, alpha=0.0, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.1333, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0997, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0996, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UR5e",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UR5e",
            home_q=[0.0, -pi / 2, 0.0, 0.0, 0.0, 0.0],
            base=base,
        )

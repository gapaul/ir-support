import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class UR3e(UTSMeshRobot):
    """Universal Robots UR3e model ported from the UTS MATLAB toolbox."""


    manufacturer_url = "https://www.universal-robots.com/products/ur3e/"
    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.15185, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.24355, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=-0.2132, alpha=0.0, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.13105, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.08535, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0921, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="UR3e",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="UR3e",
            home_q=[0.0, -pi / 2, 0.0, 0.0, 0.0, 0.0],
            base=base,
        )


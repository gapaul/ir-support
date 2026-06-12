import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class IRB120(UTSMeshRobot):
    """ABB IRB120 model ported from the UTS MATLAB toolbox."""
    manufacturer_url = "https://www.abb.com/global/en/areas/robotics/products/robots/articulated-robots/small-robots/irb-120"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.29, a=0.0, alpha=-pi / 2, qlim=self._qlim(-165, 165)),
            rtb.RevoluteDH(d=0.0, a=0.27, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-110, 110)),
            rtb.RevoluteDH(d=0.0, a=0.07, alpha=-pi / 2, qlim=self._qlim(-110, 70)),
            rtb.RevoluteDH(d=0.302, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.072, a=0.0, alpha=0.0, qlim=self._qlim(-400, 400)),
        ]

        super().__init__(
            links=links,
            mesh_stem="IRB120",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="IRB120",
            home_q=[0.0] * 6,
            base=base,
        )

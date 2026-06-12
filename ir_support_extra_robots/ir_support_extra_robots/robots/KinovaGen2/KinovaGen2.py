import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KinovaGen2(UTSMeshRobot):
    """Kinova Gen2 model ported from the UTS MATLAB toolbox."""
    manufacturer_url = "https://www.kinovarobotics.com/product/gen2-robots"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.2755, a=0.0, alpha=pi / 2, qlim=self._qlim(-720, 720)),
            rtb.RevoluteDH(d=0.0, a=0.410, alpha=-pi, qlim=self._qlim(47, 313)),
            rtb.RevoluteDH(d=0.013, a=0.0, alpha=pi / 2, qlim=self._qlim(19, 341)),
            rtb.RevoluteDH(d=0.3111, a=0.0, alpha=pi / 2, qlim=self._qlim(-720, 720)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi, qlim=self._qlim(65, 295)),
            rtb.RevoluteDH(d=0.2638, a=0.0, alpha=0.0, qlim=self._qlim(-720, 720)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KinovaGen2",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KinovaGen2",
            home_q=[0.0] * 6,
            base=base,
        )

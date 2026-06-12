import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KinovaGen3(UTSMeshRobot):
    """Kinova Gen3 model ported from the UTS MATLAB toolbox."""
    manufacturer_url = "https://www.kinovarobotics.com/product/gen3-robots"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.2433, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-154.1, 154.1)),
            rtb.RevoluteDH(d=0.03, a=0.28, alpha=0.0, offset=pi / 2, qlim=self._qlim(-150.1, 150.1)),
            rtb.RevoluteDH(d=-0.02, a=0.0, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-150.1, 150.1)),
            rtb.RevoluteDH(d=-0.245, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-148.98, 148.98)),
            rtb.RevoluteDH(d=0.057, a=0.0, alpha=pi / 2, qlim=self._qlim(-144.97, 145.0)),
            rtb.RevoluteDH(d=0.2622, a=0.0, alpha=0.0, qlim=self._qlim(-148.98, 148.98)),
        ]

        super().__init__(
            links=links,
            mesh_stem="KinovaGen3",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KinovaGen3",
            home_q=[0.0] * 6,
            base=base,
        )

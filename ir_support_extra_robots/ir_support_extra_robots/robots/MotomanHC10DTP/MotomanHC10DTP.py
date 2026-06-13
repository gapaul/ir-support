import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class MotomanHC10DTP(UTSMeshRobot):
    """Motoman HC10DTP model ported from the UTS MATLAB toolbox."""
    manufacturer_url = "https://www.motoman.com/en-us/products/robots/collaborative/hc-series/hc10dtp"

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.275, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.7, alpha=0.0, offset=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.5, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.162, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.170, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="MotomanHC10DTP",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="MotomanHC10DTP",
            home_q=[0.0] * 6,
            base=base,
        )

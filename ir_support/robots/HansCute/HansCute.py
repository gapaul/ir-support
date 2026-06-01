import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class HansCute(UTSMeshRobot):
    """Hans Cute model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.15, a=0.0, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.125, a=0.0, alpha=pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.065, alpha=-pi / 2, offset=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.0, a=0.065, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=-0.004, a=0.0, alpha=-pi / 2, offset=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.028, a=0.0, alpha=0.0, offset=pi / 2, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="HansCute",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="HansCute",
            home_q=[0.0] * 7,
            base=base,
        )

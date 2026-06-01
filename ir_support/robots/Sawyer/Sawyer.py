import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class Sawyer(UTSMeshRobot):
    """Sawyer model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.317, a=0.081, alpha=-pi / 2, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=0.1925, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-219, 131)),
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=-pi / 2, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=-0.1685, a=0.0, alpha=pi / 2, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=-pi / 2, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=0.1363, a=0.0, alpha=pi / 2, qlim=self._qlim(-175, 175)),
            rtb.RevoluteDH(d=0.13375, a=0.0, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-270, 270)),
        ]

        super().__init__(
            links=links,
            mesh_stem="Sawyer",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="Sawyer",
            home_q=[0.0, -pi / 2, 0.0, -pi / 2, 0.0, pi / 2, 0.0],
            base=base,
        )

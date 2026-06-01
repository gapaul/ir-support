import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DobotMagician(UTSMeshRobot):
    """Dobot Magician model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.1392, a=0.0, alpha=-pi / 2, qlim=self._qlim(-135, 135)),
            rtb.RevoluteDH(d=0.0, a=0.135, alpha=0.0, offset=-pi / 2, qlim=self._qlim(5, 80)),
            rtb.RevoluteDH(d=0.0, a=0.147, alpha=0.0, qlim=self._qlim(-5, 85)),
            rtb.RevoluteDH(d=0.0, a=0.06, alpha=pi / 2, offset=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=-0.05, a=0.0, alpha=0.0, offset=pi, qlim=self._qlim(-85, 85)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DobotMagician",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DobotMagician",
            home_q=[0.0] * 5,
            base=base,
        )

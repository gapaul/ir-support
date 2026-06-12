import os
from math import pi

import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class Fetch(UTSMeshRobot):
    """Fetch arm model ported from the UTS MATLAB toolbox."""


    reference_url = "https://docs.fetchrobotics.com/"
    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.05, a=0.117, alpha=-pi / 2, qlim=self._qlim(-92, 92)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-70, 87)),
            rtb.RevoluteDH(d=0.35, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-129, 129)),
            rtb.RevoluteDH(d=0.32, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-125, 125)),
            rtb.RevoluteDH(d=0.15, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]
        default_base = SE3(0.0, 0.0254, 0.734)
        base_transform = default_base if base is None else default_base * self._as_se3(base)

        super().__init__(
            links=links,
            mesh_stem="Fetch",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="Fetch",
            home_q=[0.0] * 7,
            base=base_transform,
        )
        self.tool = SE3.Rx(pi)


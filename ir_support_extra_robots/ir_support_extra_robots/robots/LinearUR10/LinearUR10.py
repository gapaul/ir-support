import os
from math import pi

import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class LinearUR10(UTSMeshRobot):
    """UR10 on a linear rail model ported from the UTS MATLAB toolbox."""
    reference_url = "https://www.universal-robots.com/products/ur10-robot/"

    def __init__(self, base=None):
        links = [
            rtb.PrismaticDH(theta=pi, a=0.0, alpha=pi / 2, qlim=[-0.8, -0.01]),
            rtb.RevoluteDH(d=0.1697, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.176, a=0.6129, alpha=-pi, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.12781, a=0.5716, alpha=pi, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.1157, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.1157, a=0.0, alpha=-pi / 2, qlim=self._qlim(-360, 360)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]
        default_base = SE3.Rx(pi / 2) * SE3.Ry(pi / 2)
        base_transform = default_base if base is None else self._as_se3(base) * default_base

        super().__init__(
            links=links,
            mesh_stem="LinearUR10",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="LinearUR10",
            home_q=[0.0, 0.0, -pi / 2, 0.0, 0.0, 0.0, 0.0],
            base=base_transform,
        )

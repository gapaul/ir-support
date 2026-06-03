import os
import warnings
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class DensoVP6242(UTSMeshRobot):
    """Candidate DENSO VP6242 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'DENSO VP6242 student model, Group_76, 2023S; active class includes two fixed intermediate visual links'

    def __init__(self, base=None):
        warnings.warn(
            'The student VP6242 visual set is an 8-link interpretation rather than a manufacturer-verified 6-axis model.',
            UserWarning,
            stacklevel=2,
        )
        self.link_colors = [
            (0.22, 0.23, 0.22, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.03, 0.28, 0.72, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.03, 0.28, 0.72, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.78, 0.8, 0.79, 1.0),
            (0.03, 0.28, 0.72, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.281, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.0, a=0.212, alpha=0.0, offset=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-70, 71)),
            rtb.RevoluteDH(d=0.075, a=0.117, alpha=pi / 2, qlim=self._qlim(0, 0)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(0, 0)),
            rtb.RevoluteDH(d=0.1, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.175, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="DensoVP6242",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DensoVP6242",
            home_q=[0.0] * 8,
            base=base,
        )

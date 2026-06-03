import os
import warnings
from math import pi

import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class IgusReBel(UTSMeshRobot):
    """Candidate igus ReBeL model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'igus ReBeL, Danial_A2_6, 2024S; original student rail variant omitted'

    def __init__(self, base=None):
        warnings.warn(
            'The original student ReBeL submission included a linear rail; this Python model intentionally omits it.',
            UserWarning,
            stacklevel=2,
        )
        base = self._as_se3(base) if base is not None else SE3()
        self.link_colors = [
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.95, 0.45, 0.02, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.9, 0.92, 0.9, 1.0),
            (0.95, 0.45, 0.02, 1.0),
            (0.04, 0.04, 0.04, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.301, a=0.0, alpha=-pi / 2, qlim=self._qlim(-179, 179)),
            rtb.RevoluteDH(d=0.0, a=0.2415, alpha=-pi, offset=-pi / 2, qlim=self._qlim(-80, 140)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, offset=-pi / 2, qlim=self._qlim(-80, 140)),
            rtb.RevoluteDH(d=0.3, a=0.0, alpha=pi / 2, qlim=self._qlim(-179, 179)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-95, 95)),
            rtb.RevoluteDH(d=0.129, a=0.0, alpha=0.0, qlim=self._qlim(-179, 179)),
        ]

        super().__init__(
            links=links,
            mesh_stem="IgusReBel",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="IgusReBel",
            home_q=[0.0] * 6,
            base=base,
        )

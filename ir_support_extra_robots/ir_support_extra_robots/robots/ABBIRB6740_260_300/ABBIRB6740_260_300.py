import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class ABBIRB6740_260_300(DHRobot3D):
    """Candidate ABB IRB 6740-260/3.00 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'ABB IRB 6740-260/3.00, A2_Tony_19_JaidenP_VuNhatMinhH, 2025S'

    @staticmethod
    def _qlim(lower, upper):
        from math import radians

        return [radians(lower), radians(upper)]

    @staticmethod
    def _as_se3(value):
        if isinstance(value, SE3):
            return value
        return SE3(np.asarray(value, dtype=float), check=False)

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.78, a=0.32, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=1.1125, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-90, 70)),
            rtb.RevoluteDH(d=0.0, a=0.2, alpha=-pi / 2, qlim=self._qlim(-170, 65)),
            rtb.RevoluteDH(d=1.142, a=0.0, alpha=pi / 2, qlim=self._qlim(-300, 300)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.2, a=-0.02, alpha=0.0, offset=-pi, qlim=self._qlim(-360, 360)),
        ]
        link3d_names = {
            "link0": "ABBIRB6740_260_300Link0",
            "link1": "ABBIRB6740_260_300Link1",
            "link2": "ABBIRB6740_260_300Link2",
            "link3": "ABBIRB6740_260_300Link3",
            "link4": "ABBIRB6740_260_300Link4",
            "link5": "ABBIRB6740_260_300Link5",
            "link6": "ABBIRB6740_260_300Link6",
            "color0": (0.04, 0.04, 0.04, 1.0),
            "color1": (0.98, 0.42, 0.03, 1.0),
            "color2": (0.98, 0.42, 0.03, 1.0),
            "color3": (0.98, 0.42, 0.03, 1.0),
            "color4": (0.98, 0.42, 0.03, 1.0),
            "color5": (0.98, 0.42, 0.03, 1.0),
            "color6": (0.98, 0.42, 0.03, 1.0),
        }
        qtest = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        qtest_transforms = [
            spb.transl(0, 0.04, 0),
            spb.transl(0.14, 0.084, 0.6),
            spb.transl(0.390, -0.081, 0.745),
            spb.transl(0.381, 0.068, 1.965),
            spb.transl(1.5825, 0.068, 2.1525),
            spb.transl(1.5825, 0.068, 2.205),
            spb.transl(1.8620, 0.048, 2.229),
        ]

        super().__init__(
            links,
            link3d_names,
            name="ABBIRB6740_260_300",
            link3d_dir=os.path.abspath(os.path.dirname(__file__)),
            qtest=qtest,
            qtest_transforms=qtest_transforms,
        )

        if base is not None:
            self.base = self._as_se3(base)
        self.q = qtest

import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class EpsonVT6L(DHRobot3D):
    """Candidate Epson VT6L model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Epson VT6L, A2_Adam_61_DanielI_DanielT_EmilB, 2025S; large DAE source downsampled for the candidate package'

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
            rtb.RevoluteDH(d=0.408866, a=0.100016, alpha=pi / 2, qlim=self._qlim(-240, 240)),
            rtb.RevoluteDH(d=0.0, a=0.422049, alpha=0.0, qlim=self._qlim(-135, 135)),
            rtb.RevoluteDH(d=-0.000274, a=4.3e-05, alpha=pi / 2, qlim=self._qlim(-155, 155)),
            rtb.RevoluteDH(d=0.39755, a=0.00024, alpha=pi / 2, qlim=self._qlim(-200, 200)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.0, a=0.080391, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]
        link3d_names = {
            "link0": "EpsonVT6LLink0",
            "link1": "EpsonVT6LLink1",
            "link2": "EpsonVT6LLink2",
            "link3": "EpsonVT6LLink3",
            "link4": "EpsonVT6LLink4",
            "link5": "EpsonVT6LLink5",
            "link6": "EpsonVT6LLink6",
            "color0": (0.28, 0.29, 0.28, 1.0),
            "color1": (0.91, 0.93, 0.91, 1.0),
            "color2": (0.91, 0.93, 0.91, 1.0),
            "color3": (0.03, 0.28, 0.72, 1.0),
            "color4": (0.91, 0.93, 0.91, 1.0),
            "color5": (0.03, 0.28, 0.72, 1.0),
            "color6": (0.91, 0.93, 0.91, 1.0),
        }
        qtest = [pi / 2, pi / 2, 0.0, 0.0, 0.0, 0.0]
        qtest_transforms = [
            spb.transl(0, 0, 0),
            spb.transl(0, 0.100016, 0.408866),
            spb.transl(0.113624, 0.102903, 0.409187),
            spb.transl(0, 0.102625, 0.830915),
            spb.transl(0, 0.102668, 0.831189),
            spb.transl(0.001681, 0.500218, 0.831429),
            spb.transl(0.001729, 0.500169, 0.831603),
        ]

        super().__init__(
            links,
            link3d_names,
            name="EpsonVT6L",
            link3d_dir=os.path.abspath(os.path.dirname(__file__)),
            qtest=qtest,
            qtest_transforms=qtest_transforms,
        )

        if base is not None:
            self.base = self._as_se3(base)
        self.q = qtest

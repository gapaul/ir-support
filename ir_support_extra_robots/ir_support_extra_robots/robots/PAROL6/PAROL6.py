import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class PAROL6(DHRobot3D):
    """Candidate PAROL6 desktop robot arm model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'PAROL6 desktop robot arm, A2_Louis_25_RubyL_MadeleineC, 2025S; source STL set used with the submitted mesh calibration offsets'

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
            rtb.RevoluteDH(d=0.1105, a=0.02342, alpha=-pi / 2, qlim=self._qlim(-123.05, 123.05)),
            rtb.RevoluteDH(d=0.0, a=0.18, alpha=pi, offset=-pi / 2, qlim=self._qlim(-145.0, -3.38)),
            rtb.RevoluteDH(d=0.0, a=-0.0435, alpha=pi / 2, offset=pi, qlim=self._qlim(-72.13, 107.87)),
            rtb.RevoluteDH(d=-0.17635, a=0.0, alpha=-pi / 2, qlim=self._qlim(-105.47, 105.47)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=-0.0628, a=-0.04525, alpha=pi, offset=pi, qlim=self._qlim(-180, 180)),
        ]
        link3d_names = {
            "link0": "PAROL6Link0",
            "link1": "PAROL6Link1",
            "link2": "PAROL6Link2",
            "link3": "PAROL6Link3",
            "link4": "PAROL6Link4",
            "link5": "PAROL6Link5",
            "link6": "PAROL6Link6",
            "color0": (0.32, 0.33, 0.32, 1.0),
            "color1": (0.72, 0.74, 0.72, 1.0),
            "color2": (0.88, 0.36, 0.04, 1.0),
            "color3": (0.72, 0.74, 0.72, 1.0),
            "color4": (0.88, 0.36, 0.04, 1.0),
            "color5": (0.72, 0.74, 0.72, 1.0),
            "color6": (0.32, 0.33, 0.32, 1.0),
        }
        qtest = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        qtest_transforms = [
            np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float),
            np.array([[1, 0, 0, 0], [0, 1, 0, 6.76617357e-18], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float),
            np.array([[1, -1.2246468e-16, 0, 0.02342], [0, 6.123234e-17, 1, 0], [-1.2246468e-16, -1, 6.123234e-17, 0.1105], [0, 0, 0, 1]], dtype=float),
            np.array([[1.8369702e-16, -1, -2.46519033e-32, 0.02342], [-1.8369702e-16, 0, -1, -1.10218212e-17], [1, 1.8369702e-16, -1.8369702e-16, 0.2905], [0, 0, 0, 1]], dtype=float),
            np.array([[-1.8369702e-16, -6.123234e-17, -1, 0.02342], [6.123234e-17, -1, 6.123234e-17, -2.88710483e-18], [-1, -6.123234e-17, 1.8369702e-16, 0.334], [0, 0, 0, 1]], dtype=float),
            np.array([[1.8369702e-16, 6.123234e-17, -1, 0.19977], [-1.8369702e-16, 1, 6.123234e-17, -2.44837511e-17], [1, 1.8369702e-16, 1.8369702e-16, 0.334], [0, 0, 0, 1]], dtype=float),
            np.array([[1.8369702e-16, 6.123234e-17, -1, 0.19257], [-1.8369702e-16, 1, 6.123234e-17, -1.54703507e-17], [1, 1.8369702e-16, 1.8369702e-16, 0.334], [0, 0, 0, 1]], dtype=float),
        ]

        super().__init__(
            links,
            link3d_names,
            name="PAROL6",
            link3d_dir=os.path.abspath(os.path.dirname(__file__)),
            qtest=qtest,
            qtest_transforms=qtest_transforms,
        )

        if base is not None:
            self.base = self._as_se3(base)
        self.q = qtest

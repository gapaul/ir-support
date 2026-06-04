import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class FanucCRX10IAL(DHRobot3D):
    """Candidate FANUC CRX-10iA/L model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'FANUC CRX-10iA/L, A2_AnhMinh_42_DaniyaS_ZainK, 2025S; using the smaller v2 DAE mesh set and the submitted identity CAD calibration transforms'

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
            rtb.RevoluteDH(d=0.2503, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.2604, a=0.71, alpha=-pi, offset=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.2604, a=0.0, alpha=-pi / 2, offset=-pi / 2, qlim=self._qlim(-270, 270)),
            rtb.RevoluteDH(d=0.54, a=0.0, alpha=-pi / 2, qlim=self._qlim(-190.8, 190.8)),
            rtb.RevoluteDH(d=0.15, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.16, a=0.0, alpha=0.0, qlim=self._qlim(-225, 225)),
        ]
        link3d_names = {
            "link0": "FanucCRX10IALLink0",
            "link1": "FanucCRX10IALLink1",
            "link2": "FanucCRX10IALLink2",
            "link3": "FanucCRX10IALLink3",
            "link4": "FanucCRX10IALLink4",
            "link5": "FanucCRX10IALLink5",
            "link6": "FanucCRX10IALLink6",
            "color0": (0.34, 0.35, 0.34, 1.0),
            "color1": (0.88, 0.9, 0.87, 1.0),
            "color2": (0.88, 0.9, 0.87, 1.0),
            "color3": (0.88, 0.9, 0.87, 1.0),
            "color4": (0.34, 0.35, 0.34, 1.0),
            "color5": (0.88, 0.9, 0.87, 1.0),
            "color6": (0.02, 0.13, 0.34, 1.0),
        }
        qtest = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        qtest_transforms = [
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
        ]

        super().__init__(
            links,
            link3d_names,
            name="FanucCRX10IAL",
            link3d_dir=os.path.abspath(os.path.dirname(__file__)),
            qtest=qtest,
            qtest_transforms=qtest_transforms,
        )

        if base is not None:
            self.base = self._as_se3(base)
        self.q = qtest

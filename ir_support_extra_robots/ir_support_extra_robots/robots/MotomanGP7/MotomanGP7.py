import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class MotomanGP7(DHRobot3D):
    """Candidate Yaskawa Motoman GP7 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'Yaskawa Motoman GP7, A2_Tony_14_JonathanD_RhysH, 2025S; selected as a cleaner GP7 DAE source than the larger shortlist PLY set'

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
            rtb.RevoluteDH(d=0.33, a=0.04, alpha=pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.0, a=0.445, alpha=0.0, qlim=self._qlim(-65, 145)),
            rtb.RevoluteDH(d=0.0, a=0.04, alpha=pi / 2, qlim=self._qlim(-70, 190)),
            rtb.RevoluteDH(d=0.44, a=0.0, alpha=-pi / 2, qlim=self._qlim(-190, 190)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-135, 135)),
            rtb.RevoluteDH(d=0.08, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]
        link3d_names = {
            "link0": "MotomanGP7Link0",
            "link1": "MotomanGP7Link1",
            "link2": "MotomanGP7Link2",
            "link3": "MotomanGP7Link3",
            "link4": "MotomanGP7Link4",
            "link5": "MotomanGP7Link5",
            "link6": "MotomanGP7Link6",
            "color0": (0.04, 0.04, 0.04, 1.0),
            "color1": (0.0, 0.18, 0.75, 1.0),
            "color2": (0.0, 0.18, 0.75, 1.0),
            "color3": (0.0, 0.18, 0.75, 1.0),
            "color4": (0.0, 0.18, 0.75, 1.0),
            "color5": (0.0, 0.18, 0.75, 1.0),
            "color6": (0.0, 0.18, 0.75, 1.0),
        }
        qtest = [0.0, 0.0, pi / 2, 0.0, 0.0, 0.0]
        qtest_transforms = [
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0),
            spb.transl(0.037637, 0, 0.333708) @ spb.rpy2tr(0, pi / 2, 0, order='xyz'),
            spb.transl(0.484115, 0, 0.333412),
            spb.transl(0.484116, 0, 0.374893),
            spb.transl(0.923412, 0, 0.374425),
            spb.transl(1.005, 0, 0.373663),
        ]

        super().__init__(
            links,
            link3d_names,
            name="MotomanGP7",
            link3d_dir=os.path.abspath(os.path.dirname(__file__)),
            qtest=qtest,
            qtest_transforms=qtest_transforms,
        )

        if base is not None:
            self.base = self._as_se3(base)
        self.q = qtest

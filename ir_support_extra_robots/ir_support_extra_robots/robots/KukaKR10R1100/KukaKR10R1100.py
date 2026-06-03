import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class KukaKR10R1100(DHRobot3D):
    """Candidate KUKA KR10 R1100 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Kuka KR10 R1100, A2_Tony_12_AbishaN_JessicaL_AryaD, 2025S"

    @staticmethod
    def _as_se3(value):
        if isinstance(value, SE3):
            return value
        matrix = np.asarray(value, dtype=float)
        if matrix.shape != (4, 4):
            raise ValueError("base must be an SE3 or a 4x4 homogeneous transform")
        return SE3(matrix, check=False)

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.4, a=0.0, alpha=-pi / 2, qlim=[-170 * pi / 180, 170 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.515, alpha=0.0, offset=-pi / 2, qlim=[-190 * pi / 180, 45 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.035, alpha=pi / 2, qlim=[-120 * pi / 180, 156 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, offset=-pi, qlim=[-185 * pi / 180, 185 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=[-120 * pi / 180, 120 * pi / 180]),
            rtb.RevoluteDH(d=0.3, a=0.0, alpha=0.0, offset=-pi, qlim=[-350 * pi / 180, 350 * pi / 180]),
        ]
        link3d_names = {f"link{i}": f"KukaKR10R1100AlignedLink{i}" for i in range(7)}
        link_colors = [(0.08, 0.08, 0.08, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.08, 0.08, 0.08, 1.0)]
        link3d_names.update({f"color{i}": colour for i, colour in enumerate(link_colors)})
        qtest = [0.0] * 6
        qtest_transforms = [
            spb.transl(0, 0, 0.02),
            spb.transl(-0.125, -0.13, -0.04),
            spb.transl(-0.079, -0.116, -0.04),
            spb.transl(-0.07, -0.07, -0.04),
            spb.transl(-0.02, -0.055, -0.039),
            spb.transl(-0.02, -0.03, -0.042),
            spb.transl(-0.02, -0.01, -0.042),
        ]
        super().__init__(links, link3d_names, os.path.abspath(os.path.dirname(__file__)), "KukaKR10R1100", qtest, qtest_transforms)
        self.home_q = np.array(qtest, dtype=float)
        if base is not None:
            self.base = self._as_se3(base)
        self.q = self.home_q.copy()
        self._update_3dmodel()

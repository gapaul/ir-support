import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class ABBIRB2600(DHRobot3D):
    """Candidate ABB IRB2600 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "ABB IRB2600, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S"

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
            rtb.RevoluteDH(d=0.445, a=0.15, alpha=-pi / 2, qlim=[-pi, pi]),
            rtb.RevoluteDH(d=0.0, a=0.7, alpha=0.0, offset=-pi / 2, qlim=[-95 * pi / 180, 155 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.115, alpha=-pi / 2, qlim=[-pi, 75 * pi / 180]),
            rtb.RevoluteDH(d=0.795, a=0.0, alpha=pi / 2, qlim=[-400 * pi / 180, 400 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=[-120 * pi / 180, 120 * pi / 180]),
            rtb.RevoluteDH(d=0.085, a=0.0, alpha=0.0, offset=pi, qlim=[-400 * pi / 180, 400 * pi / 180]),
        ]
        link3d_names = {f"link{i}": f"ABBIRB2600Link{i}" for i in range(7)}
        link_colors = [(0.78, 0.8, 0.8, 1.0),
             (0.9, 0.91, 0.9, 1.0),
             (0.72, 0.74, 0.74, 1.0),
             (0.9, 0.91, 0.9, 1.0),
             (0.72, 0.74, 0.74, 1.0),
             (0.9, 0.91, 0.9, 1.0),
             (0.16, 0.16, 0.16, 1.0)]
        link3d_names.update({f"color{i}": colour for i, colour in enumerate(link_colors)})
        qtest = [0.0] * 6
        qtest_transforms = [
            spb.transl(0, 0, 0) @ spb.rpy2tr(0, 0, 0, order="xyz"),
            spb.transl(0.15, 0, 0.49) @ spb.rpy2tr(0, 0, -pi / 2, order="xyz"),
            spb.transl(0.15, 0, 1.19) @ spb.rpy2tr(pi / 2, pi, pi / 2, order="xyz"),
            spb.transl(0.154, 0, 1.28) @ spb.rpy2tr(pi, pi / 2, 0, order="xyz"),
            spb.transl(0.95, 0, 1.28) @ spb.rpy2tr(-pi / 2, 0, -pi / 2, order="xyz"),
            spb.transl(0.957, 0, 1.28) @ spb.rpy2tr(pi, pi / 2, 0, order="xyz"),
            spb.transl(0.957, 0, 1.28) @ spb.rpy2tr(pi, pi / 2, 0, order="xyz"),
        ]
        super().__init__(links, link3d_names, os.path.abspath(os.path.dirname(__file__)), "ABBIRB2600", qtest, qtest_transforms)
        self.home_q = np.array(qtest, dtype=float)
        if base is not None:
            self.base = self._as_se3(base)
        self.q = self.home_q.copy()
        self._update_3dmodel()

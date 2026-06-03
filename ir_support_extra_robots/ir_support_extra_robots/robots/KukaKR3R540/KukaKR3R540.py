import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class KukaKR3R540(DHRobot3D):
    """Candidate KUKA KR3 R540 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Kuka KR3 540, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S"

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
            rtb.RevoluteDH(d=0.345, a=0.02, alpha=-pi / 2, qlim=[-170 * pi / 180, 170 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.26, alpha=0.0, qlim=[-170 * pi / 180, 50 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.02, alpha=-pi / 2, qlim=[-110 * pi / 180, 155 * pi / 180]),
            rtb.RevoluteDH(d=0.26, a=0.0, alpha=pi / 2, qlim=[-175 * pi / 180, 175 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=[-120 * pi / 180, 120 * pi / 180]),
            rtb.RevoluteDH(d=0.075, a=0.0, alpha=0.0, qlim=[-350 * pi / 180, 350 * pi / 180]),
        ]
        link3d_names = {f"link{i}": f"KukaKR3R540VisualLink{i}" for i in range(7)}
        link_colors = [(0.08, 0.08, 0.08, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.08, 0.08, 0.08, 1.0)]
        link3d_names.update({f"color{i}": colour for i, colour in enumerate(link_colors)})
        qtest = [0, -pi / 2, -pi / 2, 0, 0, 0]
        qtest_transforms = [
            spb.transl(0, 0, 0),
            spb.transl(0, 0, 0.174),
            spb.transl(0.02, 0, 0.345),
            spb.transl(0.019, 0, 0.6),
            spb.transl(0, 0, 0.713),
            spb.transl(0, 0, 0.86),
            spb.transl(0, 0, 0.93),
        ]
        super().__init__(links, link3d_names, os.path.abspath(os.path.dirname(__file__)), "KukaKR3R540", qtest, qtest_transforms)
        self.home_q = np.array(qtest, dtype=float)
        if base is not None:
            self.base = self._as_se3(base)
        self.q = self.home_q.copy()
        self._update_3dmodel()

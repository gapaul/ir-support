import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class MitsubishiRV2RF(UTSMeshRobot):
    """Candidate Mitsubishi RV-2FR model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Mitsubishi RV-2FR, A2_Khoa_57_HongLinhN_NhatMinhV, 2025S"
    manufacturer_url = "https://www.mitsubishielectric.com/fa/products/rbt/robot/pmerit/vertical/rv_2f/index.html"

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
            rtb.RevoluteDH(d=0.29, a=0.0, alpha=-pi / 2, qlim=[-240 * pi / 180, 240 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.27, alpha=0.0, offset=-pi / 2, qlim=[-120 * pi / 180, 120 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=-0.01, alpha=pi / 2, offset=pi / 2, qlim=[0, 160 * pi / 180]),
            rtb.RevoluteDH(d=0.272, a=0.0, alpha=-pi / 2, qlim=[-200 * pi / 180, 200 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=-0.004, alpha=pi / 2, qlim=[-120 * pi / 180, 120 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=[-360 * pi / 180, 360 * pi / 180]),
        ]
        link3d_names = {f"link{i}": f"MitsubishiRV2RFLink{i}" for i in range(7)}
        link_colors = [(0.52, 0.54, 0.54, 1.0),
             (0.9, 0.91, 0.88, 1.0),
             (0.9, 0.91, 0.88, 1.0),
             (0.78, 0.8, 0.78, 1.0),
             (0.9, 0.91, 0.88, 1.0),
             (0.76, 0.78, 0.78, 1.0),
             (0.12, 0.12, 0.12, 1.0)]
        link3d_names.update({f"color{i}": colour for i, colour in enumerate(link_colors)})
        qtest = [0, 0, pi / 2, 0, 0, 0]
        qtest_transforms = [spb.transl(0, 0, 0) for _ in range(7)]
        super().__init__(
            links=links,
            mesh_stem="MitsubishiRV2RF",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="MitsubishiRV2RF",
            home_q=qtest,
            base=base,
            link3d_names=link3d_names,
            qtest_transforms=qtest_transforms,
        )
        self.home_q = np.array(qtest, dtype=float)
        if base is not None:
            self.base = self._as_se3(base)
        self.q = self.home_q.copy()
        self._update_3dmodel()

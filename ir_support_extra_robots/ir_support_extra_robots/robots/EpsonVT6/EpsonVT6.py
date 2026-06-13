import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class EpsonVT6(UTSMeshRobot):
    """Candidate Epson VT6 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = "Epson VT6, A2_Tony_12_AbishaN_JessicaL_AryaD, 2025S"
    manufacturer_url = "https://epson.com/For-Work/Robots/6-Axis/VT6L-All-in-One-6-Axis-Robot/p/VT6LA901S"

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
            rtb.RevoluteDH(d=0.411523, a=-0.09816, alpha=pi / 2, qlim=[-170 * pi / 180, 170 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.4234, alpha=0.0, qlim=[30 * pi / 180, 160 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=[-60 * pi / 180, 45 * pi / 180]),
            rtb.RevoluteDH(d=-0.395804, a=0.0, alpha=pi / 2, qlim=[-200 * pi / 180, 200 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=[-125 * pi / 180, 125 * pi / 180]),
            rtb.RevoluteDH(d=-0.087348, a=0.0, alpha=0.0, qlim=[-360 * pi / 180, 360 * pi / 180]),
        ]
        link3d_names = {f"link{i}": f"EpsonVT6VisualLink{i}" for i in range(7)}
        link_colors = [(0.48, 0.5, 0.52, 1.0),
             (0.94, 0.95, 0.94, 1.0),
             (0.72, 0.74, 0.75, 1.0),
             (0.94, 0.95, 0.94, 1.0),
             (0.55, 0.58, 0.6, 1.0),
             (0.94, 0.95, 0.94, 1.0),
             (0.18, 0.2, 0.22, 1.0)]
        link3d_names.update({f"color{i}": colour for i, colour in enumerate(link_colors)})
        qtest = [0, pi / 2, 0, 0, 0, 0]
        qtest_transforms = [
            spb.transl(0.0, 0.0, 0.0),
            spb.transl(-0.09816, 0.0, 0.411523),
            spb.transl(-0.096768, 0.115981, 0.41144),
            spb.transl(-0.095738, 0.0, 0.83492),
            spb.transl(-0.094503, 0.0, 0.83447),
            spb.transl(-0.490307, 0.001991, 0.837018),
            spb.transl(-0.577655, 0.001991, 0.837018),
        ]
        super().__init__(
            links=links,
            mesh_stem="EpsonVT6",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="EpsonVT6",
            home_q=qtest,
            base=base,
            link3d_names=link3d_names,
            qtest_transforms=qtest_transforms,
        )
        self.home_q = np.array(qtest, dtype=float)
        self.tool = SE3(0, 0, 0.108)
        if base is not None:
            self.base = self._as_se3(base)
        self.q = self.home_q.copy()
        self._update_3dmodel()

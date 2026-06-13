import os
import warnings
from math import pi

import numpy as np
import roboticstoolbox as rtb
import spatialmath.base as spb
from spatialmath import SE3

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class KukaKR60(UTSMeshRobot):
    """Candidate KUKA KR60 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    is known to have incorrect visual geometry around the last three joints.
    Use it only as a rough visual placeholder until the wrist model is fixed.
    """

    source_note = "Kuka KR60, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S"
    reference_url = "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/kr-quantec"
    kuka_reference = "https://www.kuka.com/en-se/company/press/news/2019/12/new-kr-iontec"

    @staticmethod
    def _as_se3(value):
        if isinstance(value, SE3):
            return value
        matrix = np.asarray(value, dtype=float)
        if matrix.shape != (4, 4):
            raise ValueError("base must be an SE3 or a 4x4 homogeneous transform")
        return SE3(matrix, check=False)

    def __init__(self, base=None):
        warnings.warn(
            "KukaKR60 is a student-contributed visual model with known errors. "
            "The last three visual links are incorrectly aligned and should be "
            "fixed against manufacturer geometry before serious use. "
            f"KUKA reference: {self.kuka_reference}",
            UserWarning,
            stacklevel=2,
        )
        links = [
            rtb.RevoluteDH(d=0.815, a=0.35, alpha=-pi / 2, qlim=[-185 * pi / 180, 185 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.85, alpha=0.0, offset=-pi / 2 - pi / 9, qlim=[-35 * pi / 180, 135 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.145, alpha=-pi / 2, qlim=[-120 * pi / 180, 158 * pi / 180]),
            rtb.RevoluteDH(d=0.82, a=0.0, alpha=pi / 2, qlim=[-350 * pi / 180, 350 * pi / 180]),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=[-119 * pi / 180, 119 * pi / 180]),
            rtb.RevoluteDH(d=0.17, a=0.0, alpha=0.0, qlim=[-350 * pi / 180, 350 * pi / 180]),
        ]
        link3d_names = {f"link{i}": f"KukaKR60Link{i}" for i in range(7)}
        link_colors = [(0.08, 0.08, 0.08, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.92, 0.34, 0.02, 1.0),
             (0.08, 0.08, 0.08, 1.0)]
        link3d_names.update({f"color{i}": colour for i, colour in enumerate(link_colors)})
        qtest = [0, -35 * pi / 180, 25 * pi / 180, 0, 0, 0]
        qtest_transforms = [
            spb.transl(0, 0, 0),
            spb.transl(0.36, 0, 0.8) @ spb.rpy2tr(2 * pi, 2 * pi, -pi / 2, order="xyz"),
            spb.transl(-0.25, -0.005, 1.4) @ spb.rpy2tr(-3 * pi / 4, 0, -pi / 2, order="xyz"),
            spb.transl(-0.3, 0, 1.5) @ spb.rpy2tr(0, pi / 2, pi, order="xyz"),
            spb.transl(0.18, 0, 1.55) @ spb.rpy2tr(-11 * pi / 18 + pi / 10, 0, -pi / 2, order="xyz"),
            spb.transl(0.5, 0, 1.55) @ spb.rpy2tr(pi, 2 * pi / 5 + pi / 10, 0, order="xyz"),
            spb.transl(0.65, 0, 1.55) @ spb.rpy2tr(0, 2 * pi / 5 + pi / 10, 0, order="xyz"),
        ]
        super().__init__(
            links=links,
            mesh_stem="KukaKR60",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="KukaKR60",
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

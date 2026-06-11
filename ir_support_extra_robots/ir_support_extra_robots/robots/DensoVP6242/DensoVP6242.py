import os
from math import pi

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class DensoVP6242(DHRobot3D):
    """Candidate DENSO VP6242 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.
    """

    source_note = 'DENSO VP6242 student model, Group_76, 2023S; repaired to a 6-axis approximation using DENSO VP-6242 published dimensions'
    _MESH_FRAME_Q_MAP = (0, 1, 2, None, None, 3, 4, 5)
    _MESH_FRAME_INDICES = (0, 1, 2, 3, 6, 7, 8)

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
        # DENSO lists the VP-6242 as a 6-axis robot with a 210 mm first arm,
        # 210 mm second arm, and 75 mm J3/front-arm offset. The original
        # student model inserted two zero-motion spacer links, so the fake DOF
        # are removed while preserving the old home-frame visual alignment.
        links = [
            rtb.RevoluteDH(d=0.157, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.0, a=0.212, alpha=0.0, offset=pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.075, a=0.210, alpha=pi / 2, offset=pi / 2, qlim=self._qlim(-19, 160)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, qlim=self._qlim(-160, 160)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.06, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]
        link3d_names = {
            "link0": "DensoVP6242Link0",
            "link1": "DensoVP6242Link1",
            "link2": "DensoVP6242Link2",
            "link3": "DensoVP6242Link3",
            "link4": "DensoVP6242Link4",
            "link5": "DensoVP6242Link5",
            "link6": "DensoVP6242Link6",
            "color0": (0.22, 0.23, 0.22, 1.0),
            "color1": (0.9, 0.92, 0.9, 1.0),
            "color2": (0.9, 0.92, 0.9, 1.0),
            "color3": (0.03, 0.28, 0.72, 1.0),
            "color4": (0.9, 0.92, 0.9, 1.0),
            "color5": (0.03, 0.28, 0.72, 1.0),
            "color6": (0.9, 0.92, 0.9, 1.0),
        }
        qtest = [0.0] * 6

        # The mesh files came from a student model that used two fixed spacer
        # frames. Keep those frames privately so the visual geometry stays
        # aligned, but expose only the corrected 6-axis robot above.
        self._mesh_frame_links = [
            rtb.RevoluteDH(d=0.281, a=0.0, alpha=pi / 2),
            rtb.RevoluteDH(d=0.0, a=0.212, alpha=0.0, offset=pi / 2),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2),
            rtb.RevoluteDH(d=0.075, a=0.117, alpha=pi / 2),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=pi / 2, offset=pi / 2),
            rtb.RevoluteDH(d=0.1, a=0.0, alpha=pi / 2),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2),
            rtb.RevoluteDH(d=0.175, a=0.0, alpha=0.0),
        ]
        qtest_transforms = self._mesh_frame_transforms(
            qtest,
            base_transform=np.eye(4),
        )

        super().__init__(
            links,
            link3d_names,
            link3d_dir=os.path.abspath(os.path.dirname(__file__)),
            name="DensoVP6242",
            qtest=qtest,
            qtest_transforms=qtest_transforms,
        )

        self.home_q = np.array(qtest, dtype=float)
        if base is not None:
            self.base = self._as_se3(base)
        self.q = qtest

    def _mesh_frame_transforms(self, q, base_transform=None):
        q = list(q)
        visual_q = [
            0.0 if q_index is None else q[q_index]
            for q_index in self._MESH_FRAME_Q_MAP
        ]
        transforms = [self.base.A if base_transform is None else base_transform]
        for link, qi in zip(self._mesh_frame_links, visual_q):
            transforms.append(transforms[-1] @ link.A(qi).A)
        return [transforms[index] for index in self._MESH_FRAME_INDICES]

    def _get_transforms(self, q):
        if not hasattr(self, "_mesh_frame_links"):
            return super()._get_transforms(q)
        return self._mesh_frame_transforms(q)

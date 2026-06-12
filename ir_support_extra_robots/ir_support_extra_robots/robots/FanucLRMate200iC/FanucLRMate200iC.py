import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class FanucLRMate200iC(UTSMeshRobot):
    """Candidate FANUC LR Mate 200iC model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    Use cautiously until it graduates from the temporary candidate set.

    The original student LR Mate 200iC STL visuals were not reliable in
    Swift, so this candidate uses the existing LR Mate 200iD DAE visual
    mesh family with the 200iC DH parameters.
    """

    link_colors = [(0.05, 0.05, 0.05, 1.0),
             (0.98, 0.78, 0.02, 1.0),
             (0.98, 0.78, 0.02, 1.0),
             (0.98, 0.78, 0.02, 1.0),
             (0.98, 0.78, 0.02, 1.0),
             (0.98, 0.78, 0.02, 1.0),
             (0.05, 0.05, 0.05, 1.0)]

    source_note = "Fanuc200ic, A2_Khoa_51_MarcusF_HarrshawarthanG_YutoB, 2025S"
    reference_url = "https://www.fanuc.eu/uk/en/robots/robot-filter-page/lrmate-series/lrmate-200ic"

    def __init__(self, base=None):
        links = [

            rtb.RevoluteDH(d=0.33, a=0.075, alpha=-pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.3, alpha=0.0, offset=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.0, a=0.075, alpha=-pi / 2, qlim=self._qlim(-170, 170)),
            rtb.RevoluteDH(d=0.32, a=0.0, alpha=pi / 2, qlim=self._qlim(-190, 190)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=-pi / 2, qlim=self._qlim(-120, 120)),
            rtb.RevoluteDH(d=0.08, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="FanucLRMate200iC",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="FanucLRMate200iC",
            home_q=[0.0] * 6,
            base=base,
        )

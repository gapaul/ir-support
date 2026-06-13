import os
from math import pi

import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class FanucM20(UTSMeshRobot):
    """Candidate FANUC M-20 model ported from student Assignment 2 work.

    WARNING: This model was created by UTS students in 41013 Robotics and
    has not yet been verified against manufacturer kinematics or geometry.
    The final wrist/end-flange visuals have been simplified because the
    submitted end geometry was not reliably aligned with the DH chain. The
    final offsets are based on ROS-Industrial M-20iA frame spacing.
    """

    source_note = 'FANUC M-20, Group_82, 2023S'
    reference_url = "https://github.com/ros-industrial/fanuc/tree/kinetic-devel/fanuc_m20ia_support"

    def __init__(self, base=None):
        self.link_colors = [
            (0.04, 0.04, 0.04, 1.0),
            (1.0, 0.78, 0.02, 1.0),
            (1.0, 0.78, 0.02, 1.0),
            (1.0, 0.78, 0.02, 1.0),
            (1.0, 0.78, 0.02, 1.0),
            (1.0, 0.78, 0.02, 1.0),
            (0.04, 0.04, 0.04, 1.0),
        ]
        links = [
            rtb.RevoluteDH(d=0.475, a=0.1, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.84, alpha=pi, offset=pi / 2, qlim=self._qlim(-90, 90)),
            rtb.RevoluteDH(d=0.0, a=0.27627, alpha=-pi / 2, qlim=self._qlim(-125, 90)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=self._qlim(-225, 50)),
            rtb.RevoluteDH(d=1.055, a=0.0, alpha=pi / 2, qlim=self._qlim(-180, 180)),
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=self._qlim(-450, 450)),
        ]

        super().__init__(
            links=links,
            mesh_stem="FanucM20",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="FanucM20",
            home_q=[0.0] * 6,
            base=base,
        )

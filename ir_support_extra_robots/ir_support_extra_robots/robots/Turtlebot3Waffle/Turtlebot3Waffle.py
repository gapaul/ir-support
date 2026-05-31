import os
import roboticstoolbox as rtb

from ir_support.robots.UTSMeshRobot import UTSMeshRobot


class Turtlebot3Waffle(UTSMeshRobot):
    """TurtleBot3 Waffle visual model ported from the UTS MATLAB toolbox."""

    def __init__(self, base=None):
        links = [
            rtb.RevoluteDH(d=0.0, a=0.0, alpha=0.0, qlim=self._qlim(-360, 360)),
        ]

        super().__init__(
            links=links,
            mesh_stem="Turtlebot3Waffle",
            mesh_dir=os.path.abspath(os.path.dirname(__file__)),
            name="Turtlebot3Waffle",
            home_q=[0.0],
            base=base,
        )

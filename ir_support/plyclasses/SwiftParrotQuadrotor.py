from pathlib import Path
from typing import List, Optional, Sequence, Union

import numpy as np
import spatialgeometry as sg
import swift
from spatialmath import SE3


class SwiftParrotQuadrotor:
    """Simple Parrot quadrotor mesh actor for the Swift simulator."""

    def __init__(
        self,
        swift_env: swift.Swift,
        pose: Optional[Union[SE3, np.ndarray]] = None,
        scale: Optional[Union[float, Sequence[float]]] = None,
    ):
        if not isinstance(swift_env, swift.Swift):
            raise TypeError("swift_env must be a swift.Swift environment")

        self.swift = swift_env
        self._dae = Path(__file__).with_name("ParrotQuadrotor.dae")
        self.mesh = sg.Mesh(filename=str(self._dae), pose=self._as_se3(pose))

        if scale is not None:
            self.mesh.scale = self._as_scale(scale)

        self.swift.add(self.mesh)

    @property
    def T(self):
        return self.mesh.T

    @T.setter
    def T(self, pose: Union[SE3, np.ndarray]):
        self.set_pose(pose)

    def set_pose(self, pose: Union[SE3, np.ndarray]):
        """Set the quadrotor pose."""
        self.mesh.T = self._as_se3(pose).A

    def step(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0):
        """Move the quadrotor by a small translation and step Swift once."""
        self.mesh.T = self.mesh.T @ SE3.Trans(dx, dy, dz).A
        self.swift.step()
        return self.mesh.T

    @staticmethod
    def _as_se3(pose: Optional[Union[SE3, np.ndarray]]) -> SE3:
        if pose is None:
            return SE3()

        if isinstance(pose, SE3):
            return pose

        matrix = np.asarray(pose, dtype=float)
        if matrix.shape != (4, 4):
            raise ValueError("pose must be an SE3 or a 4x4 homogeneous transform")

        return SE3(matrix, check=False)

    @staticmethod
    def _as_scale(scale: Union[float, Sequence[float]]) -> List[float]:
        if np.isscalar(scale):
            value = float(scale)
            return [value, value, value]

        values = np.asarray(scale, dtype=float).reshape(-1)
        if values.size != 3:
            raise ValueError("scale must be a scalar or a length-3 sequence")

        return values.tolist()

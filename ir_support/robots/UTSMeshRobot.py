from math import radians
from typing import Iterable, Optional, Sequence, Union

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from ir_support.robots.DHRobot3D import DHRobot3D


class UTSMeshRobot(DHRobot3D):
    """Base class for UTS MATLAB-style DH robots with link-local mesh assets."""

    def __init__(
        self,
        links: Sequence[rtb.DHLink],
        mesh_stem: str,
        mesh_dir: str,
        name: Optional[str] = None,
        home_q: Optional[Iterable[float]] = None,
        base: Optional[Union[SE3, np.ndarray]] = None,
    ):
        self.home_q = np.array(
            list(home_q) if home_q is not None else [0.0] * len(links),
            dtype=float,
        )
        link3d_names = {
            f"link{i}": f"{mesh_stem}Link{i}" for i in range(len(links) + 1)
        }
        qtest_transforms = self._link_frame_transforms(links, self.home_q)

        super().__init__(
            list(links),
            link3d_names,
            link3d_dir=mesh_dir,
            name=name or mesh_stem,
            qtest=self.home_q.tolist(),
            qtest_transforms=qtest_transforms,
        )

        if base is not None:
            self.base = self._as_se3(base)
        self.q = self.home_q.copy()
        self._update_3dmodel()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in {"q", "base"} and hasattr(self, "links_3d"):
            self._update_3dmodel()

    @staticmethod
    def _link_frame_transforms(links, q):
        transforms = [np.eye(4)]
        for link, qi in zip(links, q):
            transforms.append(transforms[-1] @ link.A(qi).A)
        return transforms

    @staticmethod
    def _as_se3(value):
        if isinstance(value, SE3):
            return value

        matrix = np.asarray(value, dtype=float)
        if matrix.shape != (4, 4):
            raise ValueError("base must be an SE3 or a 4x4 homogeneous transform")
        return SE3(matrix, check=False)
    @staticmethod
    def _qlim(lower, upper):
        return [radians(lower), radians(upper)]

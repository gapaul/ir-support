"""Headless tests for the Swift Parrot quadrotor helper.

Run `view_swift_parrot_quadrotor.py` directly if you want to open Swift and
inspect the model visually.
"""

from pathlib import Path

import numpy as np
from spatialmath import SE3

from ir_support.plyclasses import SwiftParrotQuadrotor


def test_parrot_quadrotor_asset_exists():
    asset_path = (
        Path(__file__).resolve().parents[1]
        / "ir_support"
        / "plyclasses"
        / "ParrotQuadrotor.dae"
    )

    assert asset_path.exists()
    assert asset_path.stat().st_size > 0


def test_parrot_quadrotor_pose_conversion():
    pose = SwiftParrotQuadrotor._as_se3(SE3(1, 2, 3))

    assert np.allclose(pose.A[:3, 3], [1, 2, 3])


def test_parrot_quadrotor_rejects_invalid_pose():
    invalid_pose = np.eye(3)

    try:
        SwiftParrotQuadrotor._as_se3(invalid_pose)
    except ValueError:
        return

    raise AssertionError("Expected invalid Parrot quadrotor pose to raise ValueError")


def test_parrot_quadrotor_accepts_scalar_scale():
    assert SwiftParrotQuadrotor._as_scale(0.8) == [0.8, 0.8, 0.8]


def test_parrot_quadrotor_accepts_xyz_scale():
    assert SwiftParrotQuadrotor._as_scale([1, 2, 3]) == [1.0, 2.0, 3.0]

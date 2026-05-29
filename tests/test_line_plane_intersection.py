import numpy as np
import pytest

from ir_support.functions.line_plane_intersection import line_plane_intersection

from .helpers import assert_allclose


@pytest.mark.parametrize(
    (
        "plane_normal",
        "point_on_plane",
        "point1_on_line",
        "point2_on_line",
        "expected_point",
        "expected_check",
    ),
    [
        (
            [-1, 0, 0],
            [1.5, 0, 0],
            np.array([1.0, 0.2, 0.3]),
            np.array([2.0, 0.2, 0.3]),
            [1.5, 0.2, 0.3],
            1,
        ),
        (
            [0, 0, 1],
            [0, 0, 0],
            np.array([0.4, -0.2, 1.0]),
            np.array([0.4, -0.2, -0.5]),
            [0.4, -0.2, 0.0],
            1,
        ),
        (
            [0, 0, 1],
            [0, 0, 0],
            np.array([0.0, 0.0, 1.0]),
            np.array([1.0, 0.0, 1.0]),
            [0.0, 0.0, 0.0],
            0,
        ),
        (
            [0, 0, 1],
            [0, 0, 0],
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            [0.0, 0.0, 0.0],
            2,
        ),
        (
            [1, 0, 0],
            [2, 0, 0],
            np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            [2.0, 0.0, 0.0],
            3,
        ),
    ],
)
def test_line_plane_intersection_cases(
    plane_normal,
    point_on_plane,
    point1_on_line,
    point2_on_line,
    expected_point,
    expected_check,
):
    intersection_point, check = line_plane_intersection(
        plane_normal,
        point_on_plane,
        point1_on_line,
        point2_on_line,
    )

    assert check == expected_check
    assert_allclose(intersection_point, expected_point)

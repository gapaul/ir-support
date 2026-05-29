import numpy as np

from ir_support.classes.RectangularPrism import RectangularPrism

from .helpers import assert_allclose


def test_rectangular_prism_lab_cube_geometry():
    vertices, faces, normals = RectangularPrism(
        1.5,
        1.5,
        1.5,
        center=[2, 0, -0.5],
    ).get_data()

    assert vertices.shape == (8, 3)
    assert faces == [
        [0, 1, 2, 3],
        [0, 4, 7, 3],
        [0, 1, 5, 4],
        [2, 6, 5, 1],
        [3, 7, 6, 2],
        [4, 5, 6, 7],
    ]
    assert len(normals) == 6

    assert_allclose(vertices.min(axis=0), [1.25, -0.75, -1.25])
    assert_allclose(vertices.max(axis=0), [2.75, 0.75, 0.25])


def test_rectangular_prism_non_cube_vertices_and_normals():
    vertices, faces, normals = RectangularPrism(
        2.0,
        4.0,
        6.0,
        center=[1.0, 2.0, 3.0],
    ).get_data()

    expected_vertices = np.array([
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 4.0, 0.0],
        [0.0, 4.0, 0.0],
        [0.0, 0.0, 6.0],
        [2.0, 0.0, 6.0],
        [2.0, 4.0, 6.0],
        [0.0, 4.0, 6.0],
    ])
    expected_normals = np.array([
        [0.0, 0.0, 8.0],
        [-24.0, 0.0, 0.0],
        [0.0, -12.0, 0.0],
        [24.0, 0.0, 0.0],
        [0.0, 12.0, 0.0],
        [0.0, 0.0, 8.0],
    ])

    assert_allclose(vertices, expected_vertices)
    assert len(faces) == 6
    assert_allclose(normals, expected_normals)

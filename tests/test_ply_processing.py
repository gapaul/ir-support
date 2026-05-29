import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Path3DCollection, Poly3DCollection

from ir_support.plyprocess.ply_processing import (
    default_color_array,
    get_vertices,
    move_object,
    place_object,
    scale_object,
    set_vertices,
    transform_vertices,
)

from .helpers import assert_allclose


def test_transform_vertices_applies_homogeneous_transform():
    vertices = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ])
    transform = np.array([
        [0.0, -1.0, 0.0, 0.2],
        [1.0, 0.0, 0.0, -0.3],
        [0.0, 0.0, 1.0, 0.4],
        [0.0, 0.0, 0.0, 1.0],
    ])

    assert_allclose(
        transform_vertices(vertices, transform),
        [
            [0.2, -0.3, 0.4],
            [0.2, 0.7, 0.4],
            [-0.8, -0.3, 0.4],
        ],
    )


def test_default_colour_array_is_rgb_gradient():
    colours = default_color_array(3)

    assert colours.shape == (3, 3)
    assert_allclose(
        colours,
        [
            [0.0, 1.0, 0.5],
            [0.5, 0.5, 0.5],
            [1.0, 0.0, 0.5],
        ],
    )


def test_place_object_scatter_and_vertex_helpers():
    vertices = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ])

    scatter = place_object(vertices=vertices, output="scatter")

    assert isinstance(scatter, Path3DCollection)
    assert_allclose(get_vertices(scatter), vertices)

    set_vertices(scatter, vertices + 1)
    assert_allclose(get_vertices(scatter), vertices + 1)

    scale_object(scatter, 2)
    assert_allclose(get_vertices(scatter), (vertices + 1) * 2)


def test_place_object_surface_returns_poly_collection():
    vertices = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 1, 3],
    ])

    surface = place_object(vertices=vertices, faces=faces, output="surface")

    assert isinstance(surface, Poly3DCollection)


def test_move_object_updates_scatter_vertices():
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    scatter = ax.scatter(
        np.array([0.0, 1.0]),
        np.array([0.0, 0.5]),
        np.array([0.0, -0.5]),
    )
    transform = np.array([
        [1.0, 0.0, 0.0, 0.1],
        [0.0, 1.0, 0.0, -0.2],
        [0.0, 0.0, 1.0, 0.3],
        [0.0, 0.0, 0.0, 1.0],
    ])

    move_object(scatter, transform)

    assert_allclose(
        get_vertices(scatter),
        [
            [0.1, -0.2, 0.3],
            [1.1, 0.3, -0.2],
        ],
    )

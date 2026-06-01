import numpy as np

from ir_support.functions.make_ellipsoid import make_ellipsoid

from .helpers import assert_allclose


def test_make_ellipsoid_from_radii_has_expected_sample_points():
    u = np.array([0.0, np.pi / 2])
    v = np.array([0.0, np.pi / 2])

    x, y, z = make_ellipsoid([3, 2, 1], [0, 0, 0], u=u, v=v, is_plot=False)

    assert x.shape == (2, 2)
    assert y.shape == (2, 2)
    assert z.shape == (2, 2)
    assert_allclose(x, [[0.0, 3.0], [0.0, 0.0]])
    assert_allclose(y, [[0.0, 0.0], [0.0, 2.0]])
    assert_allclose(z, [[1.0, 0.0], [1.0, 0.0]])


def test_make_ellipsoid_accepts_documented_row_vector_radii():
    x, y, z = make_ellipsoid(
        [[3, 2, 1]],
        [0, 0, 0],
        u=np.array([0.0, np.pi / 2]),
        v=np.array([0.0, np.pi / 2]),
        is_plot=False,
    )

    assert x.shape == (2, 2)
    assert y.shape == (2, 2)
    assert z.shape == (2, 2)


def test_make_ellipsoid_from_diagonal_matrix_matches_radii_case():
    u = np.linspace(0, 2 * np.pi, 9)
    v = np.linspace(0, np.pi, 7)

    from_radii = make_ellipsoid([3, 2, 1], [0.1, -0.2, 0.3], u=u, v=v, is_plot=False)
    from_matrix = make_ellipsoid(
        np.diag([9, 4, 1]),
        [0.1, -0.2, 0.3],
        u=u,
        v=v,
        is_plot=False,
    )

    for actual, expected in zip(from_matrix, from_radii):
        assert_allclose(actual, expected)


def test_make_ellipsoid_handles_lab_upper_half_degenerate_case():
    u = np.linspace(0, 2 * np.pi, 8)
    v = np.linspace(0, np.pi / 2, 6)
    x, y, z = make_ellipsoid(
        np.array([1, 0, 1]),
        np.array([0.2, -0.1, 0.4]),
        u=u,
        v=v,
        is_plot=False,
    )

    assert x.shape == (8, 6)
    assert y.shape == (8, 6)
    assert z.shape == (8, 6)
    assert np.isfinite(x).all()
    assert np.isfinite(y).all()
    assert np.isfinite(z).all()

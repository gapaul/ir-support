import numpy as np


TOLERANCE = 1e-12


def assert_allclose(actual, expected, *, atol=TOLERANCE):
    np.testing.assert_allclose(
        np.asarray(actual, dtype=float),
        np.asarray(expected, dtype=float),
        rtol=0,
        atol=atol,
    )

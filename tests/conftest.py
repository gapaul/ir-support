import os

import matplotlib
import matplotlib.pyplot as plt
import pytest


os.environ.setdefault("MPLBACKEND", "Agg")
matplotlib.use("Agg", force=True)


@pytest.fixture(autouse=True)
def close_matplotlib_figures():
    yield
    plt.close("all")

import sys
from pathlib import Path

import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import ir_support_extra_robots.robots as extra_robots  # noqa: E402


ROBOT_FACTORIES = [getattr(extra_robots, name) for name in extra_robots.__all__]


@pytest.mark.parametrize("factory", ROBOT_FACTORIES)
def test_extra_robot_loads_meshes_and_moves(factory):
    robot = factory()

    assert robot.n >= 1
    assert len(robot.links_3d) == robot.n + 1
    assert robot.home_q.shape == (robot.n,)
    assert np.isfinite(robot.fkine(robot.q).A).all()

    q_goal = robot.home_q + np.linspace(0.08, -0.08, robot.n)
    robot.q = q_goal

    assert np.allclose(robot.q, q_goal)
    for link_mesh in robot.links_3d:
        assert np.asarray(link_mesh.T).shape == (4, 4)
        assert np.isfinite(link_mesh.T).all()

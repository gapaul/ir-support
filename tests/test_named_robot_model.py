import numpy as np

from tests.view_robot_model_swift import (
    add_robot_to_env,
    build_motion_goal,
    estimate_robot_reach,
    instantiate_robot,
    robot_options,
    resolve_robot_factory,
    robot_detail_lines,
    robot_home_q,
    robot_reference_url,
)


ROBOT_NAME = "UR3e"
ROBOT_PACKAGE = "core"


class DummySwiftEnv:
    def __init__(self):
        self.added = []

    def add(self, robot):
        self.added.append(robot)


def test_named_robot_model_loads_and_moves():
    factory, package_name = resolve_robot_factory(ROBOT_NAME, ROBOT_PACKAGE)
    robot = instantiate_robot(factory)
    home_q = robot_home_q(robot)
    goal_q = build_motion_goal(robot)

    assert package_name == ROBOT_PACKAGE
    assert robot.n >= 1
    assert home_q.shape == (robot.n,)
    assert goal_q.shape == (robot.n,)
    assert np.isfinite(robot.fkine(home_q).A).all()

    robot.q = goal_q
    assert np.allclose(robot.q, goal_q)
    assert np.isfinite(robot.fkine(robot.q).A).all()


def test_viewer_can_add_non_mesh_robot_with_swift_add():
    factory, package_name = resolve_robot_factory("DensoVS060", "core")
    robot = instantiate_robot(factory)
    env = DummySwiftEnv()

    add_method = add_robot_to_env(env, robot)

    assert package_name == "core"
    assert add_method == "robot"
    assert env.added == [robot]
    assert np.isclose(robot.base.t[2], 0.2)


def test_core_robot_reference_url_and_detail_lines():
    factory, _ = resolve_robot_factory("UR3e", "core")
    robot = instantiate_robot(factory)
    home_q = robot_home_q(robot)
    goal_q = build_motion_goal(robot)
    reach = estimate_robot_reach(robot, home_q, goal_q)
    detail_lines = robot_detail_lines(robot, reach)

    assert robot_reference_url(robot) == "https://www.universal-robots.com/products/ur3e/"
    assert any(line == "DOF: 6" for line in detail_lines)
    assert any(line.startswith("Model reach estimate:") for line in detail_lines)
    assert any(line.startswith("Reference URL: https://") for line in detail_lines)
    assert any(line.startswith("q1: d=") for line in detail_lines)

def test_all_viewer_robot_options_have_reference_urls():
    missing = []
    for option in robot_options():
        factory, _ = resolve_robot_factory(option.name, option.package)
        robot = instantiate_robot(factory)
        if not robot_reference_url(robot):
            missing.append(option.label)

    assert missing == []


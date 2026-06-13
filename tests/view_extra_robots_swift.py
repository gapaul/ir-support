"""Open optional extra robot models in Swift and animate them.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_extra_robots.py` stays headless and fast.
"""

import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import roboticstoolbox as rtb
import swift
from spatialmath import SE3


HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
ANIMATION_STEPS = 60
STEP_SECONDS = 0.03
ROBOT_COLUMNS = 5
ROBOT_SPACING = 2.0
SHOW_LABELS = True
CACHE_BUST_SWIFT_MESHES = True
RUN_CACHE_TOKEN = time.time_ns()


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import ir_support_extra_robots.robots as extra_robots  # noqa: E402


ROBOT_FACTORIES = [getattr(extra_robots, name) for name in extra_robots.__all__]

MESH_CACHE_DIR = None


def grid_position(index):
    return divmod(index, ROBOT_COLUMNS)


def grid_base(index):
    row, col = grid_position(index)
    x = (col - (ROBOT_COLUMNS - 1) / 2) * ROBOT_SPACING
    y = -row * ROBOT_SPACING
    return SE3(x, y, 0.0)


def robot_label(index, factory):
    row, col = grid_position(index)
    return f"{index + 1}. {factory.__name__} (row {row + 1}, col {col + 1})"


def add_robot_labels(env):
    if HEADLESS or not SHOW_LABELS:
        return

    env.add(swift.Label("IR Support extra robots"))
    for index, factory in enumerate(ROBOT_FACTORIES):
        env.add(swift.Label(robot_label(index, factory)))


def movement_delta(robot):
    delta = np.zeros(robot.n)
    for index, link in enumerate(robot.links):
        if getattr(link, "isprismatic", False):
            delta[index] = -0.2
        else:
            direction = 1 if index % 2 == 0 else -1
            delta[index] = direction * 0.25
    return delta


def cache_bust_robot_meshes(robot):
    if not CACHE_BUST_SWIFT_MESHES:
        return

    links_3d = getattr(robot, "links_3d", [])
    if not links_3d:
        return

    global MESH_CACHE_DIR
    if MESH_CACHE_DIR is None:
        MESH_CACHE_DIR = Path(tempfile.mkdtemp(prefix="ir_support_swift_meshes_"))

    for mesh in links_3d:
        if not hasattr(mesh, "filename"):
            continue
        source = Path(mesh.filename)
        if not source.exists():
            continue
        dest = (
            MESH_CACHE_DIR
            / f"{source.stem}_{RUN_CACHE_TOKEN}_{source.stat().st_mtime_ns}{source.suffix}"
        )
        shutil.copy2(source, dest)
        mesh.filename = str(dest.resolve())


def main():
    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)
    add_robot_labels(env)

    robots = []
    trajectories = []

    for index, factory in enumerate(ROBOT_FACTORIES):
        robot = factory(base=grid_base(index))
        robot.q = robot.home_q.copy()
        cache_bust_robot_meshes(robot)
        robot.add_to_env(env)
        robots.append(robot)

        goal_q = robot.home_q + movement_delta(robot)
        trajectory = rtb.jtraj(robot.home_q, goal_q, ANIMATION_STEPS).q
        return_trajectory = rtb.jtraj(goal_q, robot.home_q, ANIMATION_STEPS).q
        trajectories.append(np.vstack((trajectory, return_trajectory)))

        print(f"Loaded {robot_label(index, factory)}: {robot.n} joints, {len(robot.links_3d)} meshes")

    print("Animating optional extra robots in Swift...")

    for step_index in range(trajectories[0].shape[0]):
        for robot, trajectory in zip(robots, trajectories):
            robot.q = trajectory[step_index]
        env.step(STEP_SECONDS)

    print("Animation complete.")

    if HEADLESS:
        return

    if WAIT_FOR_ENTER_BEFORE_CLOSING:
        input("Press Enter to close Swift...")
    else:
        time.sleep(3)

    try:
        env.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()

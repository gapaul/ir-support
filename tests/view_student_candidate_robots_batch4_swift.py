"""
Open the fourth student candidate robot batch in Swift.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_student_candidate_robots_batch4.py` stays headless and fast.
"""

import sys
import shutil
import tempfile
import time
from pathlib import Path

import numpy as np
import swift
from spatialmath import SE3


HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
ANIMATION_STEPS = 70
ANIMATION_REPEATS = 100
STEP_SECONDS = 0.1
ROBOT_COLUMNS = 5
ROBOT_SPACING = 2.7
REVOLUTE_JOINT_AMPLITUDE = 0.38
PRISMATIC_JOINT_AMPLITUDE = 0.12
DEFAULT_CAMERA_DISTANCE = 2.0
CACHE_BUST_SWIFT_MESHES = True


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.BCN3DMoveo.BCN3DMoveo import BCN3DMoveo  # noqa: E402
from ir_support_extra_robots.robots.DobotNova5.DobotNova5 import DobotNova5  # noqa: E402
from ir_support_extra_robots.robots.DoosanA0509.DoosanA0509 import DoosanA0509  # noqa: E402
from ir_support_extra_robots.robots.KukaKR4.KukaKR4 import KukaKR4  # noqa: E402
from ir_support_extra_robots.robots.KukaKR5Arc.KukaKR5Arc import KukaKR5Arc  # noqa: E402
from ir_support_extra_robots.robots.KukaKR6R900.KukaKR6R900 import KukaKR6R900  # noqa: E402
from ir_support_extra_robots.robots.KukaTitan.KukaTitan import KukaTitan  # noqa: E402
from ir_support_extra_robots.robots.OmronTM12.OmronTM12 import OmronTM12  # noqa: E402
from ir_support_extra_robots.robots.OmronTM5700.OmronTM5700 import OmronTM5700  # noqa: E402
from ir_support_extra_robots.robots.UR16e.UR16e import UR16e  # noqa: E402


ROBOT_FACTORIES = [
    DoosanA0509,
    DobotNova5,
    UR16e,
    OmronTM12,
    OmronTM5700,
    KukaKR4,
    KukaKR5Arc,
    KukaKR6R900,
    KukaTitan,
    BCN3DMoveo,
]

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


def robot_base_position(index):
    return np.array(grid_base(index).t, dtype=float)


def robot_camera_pose(robot, index):
    base_position = robot_base_position(index)
    transforms = np.asarray([transform[:3, 3] for transform in robot._get_transforms(robot.q)])
    if transforms.size:
        centred = transforms - transforms.mean(axis=0)
        span = max(np.linalg.norm(centred, axis=1).max() * 2.0, 0.5)
    else:
        span = DEFAULT_CAMERA_DISTANCE

    distance = min(max(span * 1.7, DEFAULT_CAMERA_DISTANCE), 5.0)
    look_at = base_position + np.array([0.0, 0.0, min(max(span * 0.35, 0.25), 1.5)])
    position = base_position + np.array([distance, -distance, min(max(distance * 0.55, 0.8), 3.0)])
    return position, look_at


def set_robot_camera(env, robot, index):
    position, look_at = robot_camera_pose(robot, index)
    env.set_camera_pose(position, look_at)


def cache_bust_robot_meshes(robot):
    """Use fresh mesh file URLs so the browser cannot reuse stale DAE assets."""
    if not CACHE_BUST_SWIFT_MESHES:
        return

    global MESH_CACHE_DIR
    if MESH_CACHE_DIR is None:
        MESH_CACHE_DIR = Path(tempfile.mkdtemp(prefix="ir_support_swift_meshes_"))
        print(f"Using Swift mesh cache-bust folder: {MESH_CACHE_DIR}")

    robot_cache_dir = MESH_CACHE_DIR / robot.name
    robot_cache_dir.mkdir(parents=True, exist_ok=True)

    for index, mesh in enumerate(robot.links_3d):
        source = Path(mesh.filename)
        if not source.exists():
            continue

        dest = robot_cache_dir / f"{source.stem}_{index}_{source.stat().st_mtime_ns}{source.suffix}"
        shutil.copy2(source, dest)
        mesh.filename = str(dest)


def add_robot_buttons(env, robots):
    if HEADLESS:
        return
    env.add(swift.Label("Student candidate robots, batch 4"))
    for index, (factory, robot) in enumerate(zip(ROBOT_FACTORIES, robots)):
        env.add(
            swift.Button(
                lambda _, robot=robot, index=index: set_robot_camera(env, robot, index),
                desc=robot_label(index, factory),
            )
        )


def joint_limits(robot, index):
    qlim = np.asarray(getattr(robot, "qlim", []), dtype=float)
    if qlim.shape == (robot.n, 2):
        return qlim[index, 0], qlim[index, 1]
    if qlim.shape == (2, robot.n):
        return qlim[0, index], qlim[1, index]
    return -np.inf, np.inf


def joint_wave_ranges(robot, start_q):
    centres = np.asarray(start_q, dtype=float).copy()
    amplitudes = np.zeros(robot.n)

    for index, link in enumerate(robot.links):
        lower, upper = joint_limits(robot, index)
        desired = PRISMATIC_JOINT_AMPLITUDE if getattr(link, "isprismatic", False) else REVOLUTE_JOINT_AMPLITUDE

        low_target = start_q[index] - desired
        high_target = start_q[index] + desired
        if np.isfinite(lower):
            low_target = max(low_target, lower)
        if np.isfinite(upper):
            high_target = min(high_target, upper)

        if high_target > low_target:
            centres[index] = 0.5 * (low_target + high_target)
            amplitudes[index] = 0.5 * (high_target - low_target)

    return centres, amplitudes


def make_joint_wave_trajectory(robot, start_q):
    centres, amplitudes = joint_wave_ranges(robot, start_q)
    theta = np.linspace(0.0, 2.0 * np.pi, ANIMATION_STEPS, endpoint=False)
    phases = np.linspace(0.0, np.pi, robot.n, endpoint=False)
    return centres + amplitudes * np.sin(theta[:, None] + phases[None, :])


def main():
    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)

    robots = []
    trajectories = []

    for index, factory in enumerate(ROBOT_FACTORIES):
        robot = factory(base=grid_base(index))
        cache_bust_robot_meshes(robot)
        robot.add_to_env(env)
        robots.append(robot)

        start_q = np.asarray(robot.q, dtype=float).copy()
        trajectories.append(make_joint_wave_trajectory(robot, start_q))

        print(f"Loaded {robot_label(index, factory)}: {robot.n} joints, {len(robot.links_3d)} meshes")

    add_robot_buttons(env, robots)

    print("Animating student candidate robot batch 4 in Swift...")

    for _ in range(ANIMATION_REPEATS):
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

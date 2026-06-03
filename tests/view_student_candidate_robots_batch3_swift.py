"""
Open the third student candidate robot batch in Swift.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_student_candidate_robots_batch3.py` stays headless and fast.
"""

import sys
import time
from pathlib import Path

import numpy as np
import swift
from spatialmath import SE3


HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
SAVE_SWIFT_SCREENSHOT = True
SCREENSHOT_PATH = Path(__file__).resolve().parent / "_swift_screenshots" / "student_candidate_robots_batch3.png"
ANIMATION_STEPS = 70
ANIMATION_REPEATS = 10
STEP_SECONDS = 0.03
ROBOT_COLUMNS = 5
ROBOT_SPACING = 2.35
REVOLUTE_JOINT_AMPLITUDE = 0.38
PRISMATIC_JOINT_AMPLITUDE = 0.12
DEFAULT_CAMERA_DISTANCE = 2.0


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_robots.robots.DensoVP6242.DensoVP6242 import DensoVP6242  # noqa: E402
from ir_support_extra_robots.robots.DensoVS068.DensoVS068 import DensoVS068  # noqa: E402
from ir_support_extra_robots.robots.DobotCR10.DobotCR10 import DobotCR10  # noqa: E402
from ir_support_extra_robots.robots.DobotNova2.DobotNova2 import DobotNova2  # noqa: E402
from ir_support_extra_robots.robots.FanucM20.FanucM20 import FanucM20  # noqa: E402
from ir_support_extra_robots.robots.IgusReBel.IgusReBel import IgusReBel  # noqa: E402
from ir_support_extra_robots.robots.KukaLBRiiwa14.KukaLBRiiwa14 import KukaLBRiiwa14  # noqa: E402
from ir_support_extra_robots.robots.ABBIRB1520ID.ABBIRB1520ID import ABBIRB1520ID  # noqa: E402
from ir_support_extra_robots.robots.ABBIRB1660ID.ABBIRB1660ID import ABBIRB1660ID  # noqa: E402


ROBOT_FACTORIES = [
    DensoVP6242,
    DensoVS068,
    DobotCR10,
    DobotNova2,
    FanucM20,
    IgusReBel,
    KukaLBRiiwa14,
    ABBIRB1520ID,
    ABBIRB1660ID,
]


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

    distance = min(max(span * 1.7, DEFAULT_CAMERA_DISTANCE), 4.2)
    look_at = base_position + np.array([0.0, 0.0, min(max(span * 0.35, 0.25), 1.1)])
    position = base_position + np.array([distance, -distance, min(max(distance * 0.55, 0.8), 2.5)])
    return position, look_at


def set_robot_camera(env, robot, index):
    position, look_at = robot_camera_pose(robot, index)
    env.set_camera_pose(position, look_at)


def add_robot_buttons(env, robots):
    if HEADLESS:
        return
    env.add(swift.Label("Student candidate robots, batch 3"))
    for index, (factory, robot) in enumerate(zip(ROBOT_FACTORIES, robots)):
        env.add(
            swift.Button(
                lambda _, robot=robot, index=index: set_robot_camera(env, robot, index),
                desc=robot_label(index, factory),
            )
        )


def save_swift_screenshot():
    if HEADLESS or not SAVE_SWIFT_SCREENSHOT:
        return
    try:
        from PIL import ImageGrab
    except ImportError:
        print("Pillow ImageGrab is not available; skipping screenshot capture.")
        return

    input(
        "Set the Swift browser view you want captured, then press Enter here "
        "to save a screenshot..."
    )
    SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image = ImageGrab.grab()
    image.save(SCREENSHOT_PATH)
    print(f"Saved Swift screenshot to: {SCREENSHOT_PATH}")


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
        robot.add_to_env(env)
        robots.append(robot)

        start_q = np.asarray(robot.q, dtype=float).copy()
        trajectories.append(make_joint_wave_trajectory(robot, start_q))

        print(f"Loaded {robot_label(index, factory)}: {robot.n} joints, {len(robot.links_3d)} meshes")

    add_robot_buttons(env, robots)

    print("Animating student candidate robot batch 3 in Swift...")

    for _ in range(ANIMATION_REPEATS):
        for step_index in range(trajectories[0].shape[0]):
            for robot, trajectory in zip(robots, trajectories):
                robot.q = trajectory[step_index]
            env.step(STEP_SECONDS)

    print("Animation complete.")
    save_swift_screenshot()

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

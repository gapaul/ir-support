"""
Capture a selected student candidate robot moving in Swift.

Run this file directly from the IDE, for example with Ctrl+F5. It loads one
robot, moves it through three poses, switches between three camera views, and
saves screenshots that can be inspected after the run.
"""

import sys
import time
from pathlib import Path

import numpy as np
import swift
from spatialmath import SE3


SELECTED_ROBOT_NAME = "FanucM20"
HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
STEP_SECONDS = 0.04
SETTLE_STEPS = 12
OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "_swift_screenshots"
    / "student_candidate_robot_motion"
)
SCREENSHOT_MODE = "cropped_desktop"  # "cropped_desktop", "full_desktop", or "swift_download"
SWIFT_CANVAS_CROP = (198, 88, 1920, 1040)  # left, top, right, bottom for a maximised browser window


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from view_student_candidate_robots_batch3_swift import (  # noqa: E402
    ROBOT_FACTORIES,
    make_joint_wave_trajectory,
)


VIEW_DIRECTIONS = {
    "front": np.array([1.0, -1.0, 0.55]),
    "side": np.array([0.0, -1.35, 0.45]),
    "top": np.array([0.55, -0.55, 1.8]),
}


def selected_factory():
    for factory in ROBOT_FACTORIES:
        if factory.__name__.lower() == SELECTED_ROBOT_NAME.lower():
            return factory
    available = ", ".join(factory.__name__ for factory in ROBOT_FACTORIES)
    raise ValueError(f"Unknown robot {SELECTED_ROBOT_NAME!r}. Available: {available}")


def robot_span_and_centre(robot):
    transforms = np.asarray([transform[:3, 3] for transform in robot._get_transforms(robot.q)])
    centre = transforms.mean(axis=0)
    span = max(np.linalg.norm(transforms - centre, axis=1).max() * 2.0, 0.6)
    return span, centre


def set_camera(env, robot, view_name):
    span, centre = robot_span_and_centre(robot)
    look_at = centre + np.array([0.0, 0.0, min(max(span * 0.15, 0.15), 0.8)])
    direction = VIEW_DIRECTIONS[view_name].astype(float)
    direction /= np.linalg.norm(direction)
    distance = min(max(span * 1.55, 1.5), 4.0)
    env.set_camera_pose(look_at + direction * distance, look_at)


def settle(env):
    for _ in range(SETTLE_STEPS):
        env.step(STEP_SECONDS)


def save_desktop_capture(path, *, crop=True):
    try:
        from PIL import ImageGrab
    except ImportError:
        print("Pillow ImageGrab is not available; skipping desktop screenshot.")
        return

    bbox = SWIFT_CANVAS_CROP if crop else None
    image = ImageGrab.grab(bbox=bbox)
    image.save(path)
    print(f"Saved {path}")


def save_screenshot(env, output_stem, output_path):
    mode = SCREENSHOT_MODE.lower()
    if mode == "swift_download":
        env.screenshot(output_stem)
        print(f"Requested Swift browser download for {output_stem}.png")
    elif mode == "cropped_desktop" and not HEADLESS:
        save_desktop_capture(output_path, crop=True)
    elif mode == "full_desktop" and not HEADLESS:
        save_desktop_capture(output_path, crop=False)
    else:
        raise ValueError(
            "SCREENSHOT_MODE must be 'cropped_desktop', 'full_desktop', "
            "or 'swift_download'"
        )


def pose_samples(trajectory):
    indexes = [0, len(trajectory) // 3, (2 * len(trajectory)) // 3]
    return [(sample_index + 1, trajectory[index]) for sample_index, index in enumerate(indexes)]


def main():
    factory = selected_factory()
    output_dir = OUTPUT_DIR / factory.__name__
    output_dir.mkdir(parents=True, exist_ok=True)

    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)

    robot = factory(base=SE3())
    robot.add_to_env(env)
    env.add(swift.Label(f"Inspecting {factory.__name__}"))

    start_q = np.asarray(robot.q, dtype=float).copy()
    trajectory = make_joint_wave_trajectory(robot, start_q)

    print(f"Loaded {factory.__name__}: {robot.n} joints, {len(robot.links_3d)} meshes")
    print(f"Saving screenshots to {output_dir}")

    for view_name in VIEW_DIRECTIONS:
        set_camera(env, robot, view_name)
        settle(env)
        for pose_index, q in pose_samples(trajectory):
            robot.q = q
            settle(env)
            stem = f"{factory.__name__}_{view_name}_pose{pose_index}"
            save_screenshot(env, stem, output_dir / f"{stem}.png")

    if not HEADLESS and WAIT_FOR_ENTER_BEFORE_CLOSING:
        input("Press Enter to close Swift...")

    try:
        env.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()

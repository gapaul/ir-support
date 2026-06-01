"""Open the Parrot quadrotor in Swift.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_swift_parrot_quadrotor.py` stays headless and fast.
"""

import sys
import time
from pathlib import Path

import keyboard
import swift
from spatialmath import SE3


# Toggle this to True if you want the same script to run without opening Swift.
HEADLESS = False

# Keep the browser window open after the automatic movement.
WAIT_FOR_ENTER_BEFORE_CLOSING = True

# Keyboard movement step while the script is running.
STEP_SIZE = 0.05

# Number of automatic circle steps before switching to keyboard control.
AUTO_STEPS = 180
STEP_SECONDS = 0.02


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ir_support import SwiftParrotQuadrotor  # noqa: E402


def set_follow_camera(env, drone):
    position = drone.T[:3, 3]
    env.set_camera_pose(
        position=[position[0] + 5, position[1] - 7, position[2] + 4],
        look_at=position,
    )


def keyboard_step(drone):
    dx = dy = dz = 0.0

    if keyboard.is_pressed("w"):
        dx += STEP_SIZE
    if keyboard.is_pressed("s"):
        dx -= STEP_SIZE
    if keyboard.is_pressed("a"):
        dy += STEP_SIZE
    if keyboard.is_pressed("d"):
        dy -= STEP_SIZE
    if keyboard.is_pressed("r"):
        dz += STEP_SIZE
    if keyboard.is_pressed("f"):
        dz -= STEP_SIZE

    if dx or dy or dz:
        drone.step(dx, dy, dz)
        return True

    return False


def main():
    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)

    drone = SwiftParrotQuadrotor(env, pose=SE3(0, 0, 2), scale=2.0)
    set_follow_camera(env, drone)

    for step_index in range(AUTO_STEPS):
        angle = step_index * 0.04
        drone.set_pose(SE3(2.0, 0, 2.0) * SE3.Rz(angle) * SE3(0, 1.5, 0))
        set_follow_camera(env, drone)
        env.step(STEP_SECONDS)

    if HEADLESS:
        return

    print("W/S: X +/-   A/D: Y +/-   R/F: Z +/-   Q or Esc: quit")
    while True:
        if keyboard.is_pressed("q") or keyboard.is_pressed("esc"):
            break

        moved = keyboard_step(drone)
        set_follow_camera(env, drone)
        if not moved:
            env.step(STEP_SECONDS)
        time.sleep(STEP_SECONDS)

    if WAIT_FOR_ENTER_BEFORE_CLOSING:
        input("Press Enter to close Swift...")

    try:
        env.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()

"""Open the UTS robot models in Swift and animate them.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_uts_robot_models.py` stays headless and fast.
"""

import sys
import time
from pathlib import Path

import numpy as np
import roboticstoolbox as rtb
import swift
from spatialmath import SE3


# Toggle this to True if you want the same script to run without opening Swift.
HEADLESS = False

# Keep the browser window open after the motion so you can inspect the models.
WAIT_FOR_ENTER_BEFORE_CLOSING = True

# Increase this if the animation is too quick to inspect.
ANIMATION_STEPS = 60
STEP_SECONDS = 0.03

# Keep the default as all ported UTS robot models. For a quicker visual check,
# replace this with a smaller list such as [UR3e, UR5e, UR10e].
ROBOT_COLUMNS = 4
ROBOT_SPACING = 2.0


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ir_support import (  # noqa: E402
    DensoVM6083,
    DobotMagician,
    Fetch,
    HansCute,
    IRB120,
    KinovaGen2,
    KinovaGen3,
    LinearUR10,
    MotomanHC10DTP,
    MyCobot280,
    Sawyer,
    Turtlebot3Waffle,
    UR10,
    UR10e,
    UR3e,
    UR5e,
)


ROBOT_FACTORIES = [
    UR3e,
    UR5e,
    UR10e,
    DensoVM6083,
    UR10,
    DobotMagician,
    MyCobot280,
    IRB120,
    HansCute,
    KinovaGen2,
    KinovaGen3,
    MotomanHC10DTP,
    Sawyer,
    Fetch,
    LinearUR10,
    Turtlebot3Waffle,
]


def grid_base(index):
    row, col = divmod(index, ROBOT_COLUMNS)
    x = (col - (ROBOT_COLUMNS - 1) / 2) * ROBOT_SPACING
    y = -row * ROBOT_SPACING
    return SE3(x, y, 0.0)


def movement_delta(robot):
    delta = np.zeros(robot.n)
    for index, link in enumerate(robot.links):
        if getattr(link, "isprismatic", False):
            delta[index] = -0.2
        else:
            direction = 1 if index % 2 == 0 else -1
            delta[index] = direction * 0.25
    return delta


def main():
    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)

    robots = []
    trajectories = []

    for index, factory in enumerate(ROBOT_FACTORIES):
        robot = factory(base=grid_base(index))
        robot.q = robot.home_q.copy()
        robot.add_to_env(env)
        robots.append(robot)

        goal_q = robot.home_q + movement_delta(robot)
        trajectory = rtb.jtraj(robot.home_q, goal_q, ANIMATION_STEPS).q
        return_trajectory = rtb.jtraj(goal_q, robot.home_q, ANIMATION_STEPS).q
        trajectories.append(np.vstack((trajectory, return_trajectory)))

        print(f"Loaded {factory.__name__}: {robot.n} joints, {len(robot.links_3d)} meshes")

    print("Animating UTS robot models in Swift...")

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

"""Open all ported UTS Parts assets in Swift and animate them.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_uts_parts.py` stays headless and fast.
"""

import sys
import time
from math import pi
from pathlib import Path

import numpy as np
import swift
from spatialmath import SE3


# Toggle this to True if you want the same script to run without opening Swift.
HEADLESS = False

# Keep the browser window open after the motion so you can inspect the parts.
WAIT_FOR_ENTER_BEFORE_CLOSING = True

# Increase this if the animation is too quick to inspect.
ANIMATION_STEPS = 160
STEP_SECONDS = 0.03

# Grid spacing is intentionally generous because the parts include fences,
# tables, people, and a very tall pen model.
PART_COLUMNS = 5
GRID_SPACING_X = 4.5
GRID_SPACING_Y = 4.5

# Motion applied around each part's grid cell.
X_AMPLITUDE = 0.45
Y_AMPLITUDE = 0.35
Z_AMPLITUDE = 0.45
Z_BIAS = 0.25


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ir_support.parts import part_mesh, part_names  # noqa: E402


# Replace this with a tuple of names if you want to inspect a smaller subset.
PARTS_TO_LOAD = part_names()


def grid_pose(index):
    row, col = divmod(index, PART_COLUMNS)
    x = (col - (PART_COLUMNS - 1) / 2) * GRID_SPACING_X
    y = -row * GRID_SPACING_Y
    return SE3(x, y, 0.0)


def motion_pose(index, step_index):
    progress = step_index / max(ANIMATION_STEPS - 1, 1)
    phase = 2 * pi * progress + index * 0.41
    x = X_AMPLITUDE * np.sin(phase)
    y = Y_AMPLITUDE * np.cos(phase * 1.25)
    z = Z_BIAS + Z_AMPLITUDE * (0.5 + 0.5 * np.sin(phase * 1.7))
    return SE3(x, y, z)


def main():
    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)

    meshes = []
    base_poses = []

    for index, name in enumerate(PARTS_TO_LOAD):
        base_pose = grid_pose(index)
        mesh = part_mesh(name, pose=base_pose)
        env.add(mesh)
        meshes.append(mesh)
        base_poses.append(base_pose)
        print(f"Loaded part {index + 1:02d}/{len(PARTS_TO_LOAD)}: {name}")

    print("Animating UTS parts in x, y, and z...")

    for step_index in range(ANIMATION_STEPS):
        for index, (mesh, base_pose) in enumerate(zip(meshes, base_poses)):
            mesh.T = (base_pose * motion_pose(index, step_index)).A
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

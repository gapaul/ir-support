"""
Open the first student candidate object batch in Swift.

Run this file directly from the IDE, for example with Ctrl+F5.
The pytest file `test_student_candidate_parts_batch1.py` stays headless and fast.
"""

import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import swift
from spatialmath import SE3


HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
ANIMATION_STEPS = 120
ANIMATION_REPEATS = 100
STEP_SECONDS = 0.04
PART_COLUMNS = 4
PART_SPACING = 2.5
LIFT_HEIGHT = 1.0
DEFAULT_CAMERA_DISTANCE = 2.3
CACHE_BUST_SWIFT_MESHES = True
RUN_CACHE_TOKEN = time.time_ns()


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_PARTS_ROOT = REPO_ROOT / "ir_support_extra_parts"
for path in (REPO_ROOT, EXTRA_PARTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_parts.parts import part_mesh, part_path  # noqa: E402


PART_NAMES = [
    "Workbench",
    "GlassBottle",
    "PintCup",
    "ShotGlass",
    "WineCup",
    "WineBottle",
    "Plate",
    "SafetyHelmet",
    "WarningSign",
    "WetFloorSign",
    "BlueBin",
    "Apple",
    "MilkPitcher",
    "CardboardBox",
    "MilkCarton",
    "BananaPeel",
    "SauceBottle",
]

MESH_CACHE_DIR = None


def grid_position(index):
    return divmod(index, PART_COLUMNS)


def grid_pose(index, z=0.0, angle=0.0):
    row, col = grid_position(index)
    x = (col - (PART_COLUMNS - 1) / 2) * PART_SPACING
    y = -row * PART_SPACING
    return SE3(x, y, z) * SE3.Rz(angle)


def part_label(index, name):
    row, col = grid_position(index)
    return f"{index + 1}. {name} (row {row + 1}, col {col + 1})"


def part_base_position(index):
    return np.array(grid_pose(index).t, dtype=float)


def set_part_camera(env, index):
    base_position = part_base_position(index)
    row, col = grid_position(index)
    direction = np.array([1.0, -1.0, 0.65], dtype=float)
    direction = direction / np.linalg.norm(direction)
    distance = DEFAULT_CAMERA_DISTANCE
    if row >= 3:
        distance = 2.6
    if col in {0, PART_COLUMNS - 1}:
        distance += 0.2

    look_at = base_position + np.array([0.0, 0.0, 0.45])
    position = look_at + direction * distance
    env.set_camera_pose(position, look_at)


def cache_bust_part_mesh(mesh, name):
    if not CACHE_BUST_SWIFT_MESHES:
        return mesh

    global MESH_CACHE_DIR
    if MESH_CACHE_DIR is None:
        MESH_CACHE_DIR = Path(tempfile.mkdtemp(prefix="ir_support_swift_parts_"))
        print(f"Using Swift mesh cache-bust folder: {MESH_CACHE_DIR}")

    source = Path(part_path(name))
    dest = (
        MESH_CACHE_DIR
        / f"{source.stem}_{RUN_CACHE_TOKEN}_{source.stat().st_mtime_ns}{source.suffix}"
    )
    shutil.copy2(source, dest)
    if hasattr(mesh, "filename"):
        mesh.filename = str(dest.resolve())
    return mesh


def add_part_buttons(env):
    if HEADLESS:
        return
    env.add(swift.Label("Student candidate parts, batch 1"))
    for index, name in enumerate(PART_NAMES):
        env.add(
            swift.Button(
                lambda _, index=index: set_part_camera(env, index),
                desc=part_label(index, name),
            )
        )

def animation_pose(index, phase):
    # One loop: rise, rotate once while hovering, then lower.
    lift = LIFT_HEIGHT * np.sin(np.pi * phase)
    angle = 2.0 * np.pi * phase
    return grid_pose(index, z=lift, angle=angle)


def main():
    env = swift.Swift()
    env.launch(realtime=True, headless=HEADLESS)

    meshes = []
    for index, name in enumerate(PART_NAMES):
        mesh = part_mesh(name, pose=grid_pose(index))
        cache_bust_part_mesh(mesh, name)
        env.add(mesh)
        meshes.append(mesh)
        print(f"Loaded {part_label(index, name)} from {part_path(name)}")

    add_part_buttons(env)
    print("Animating student candidate parts batch 1 in Swift...")

    phases = np.linspace(0.0, 1.0, ANIMATION_STEPS, endpoint=False)
    for _ in range(ANIMATION_REPEATS):
        for phase in phases:
            for index, mesh in enumerate(meshes):
                mesh.T = animation_pose(index, phase).A
            env.step(STEP_SECONDS)

    for index, mesh in enumerate(meshes):
        mesh.T = grid_pose(index).A

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







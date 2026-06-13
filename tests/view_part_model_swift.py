"""Inspect one IR Support extra part in Swift.

Most convenient use from VS Code
--------------------------------
Run this file directly, for example with Ctrl+F5. Swift opens with one part
loaded. Use the dropdown in the Swift side panel to choose any packaged extra
part, then click "Load selected part". The selected part bobs up and down,
rotates about the vertical axis, and the camera buttons jump to useful
inspection views.

Command-line examples
---------------------
These examples assume the command line is using the same Python environment as
VS Code. If bare python points to another Python install, activate the project
virtual environment first or call that environment's Python executable directly.

List all part names grouped by category:

    python tests/view_part_model_swift.py --list

Open a particular part as the initial selection:

    python tests/view_part_model_swift.py --part Camera
    python tests/view_part_model_swift.py --part MilkCarton

The viewer copies mesh files to a temporary folder before loading them in Swift.
That avoids stale browser-cached DAE files while model geometry is being edited.
"""

import argparse
import shutil
import sys
import tempfile
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from spatialmath import SE3


HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
ANIMATION_STEPS = 120
ANIMATION_REPEATS = 100
STEP_SECONDS = 0.04
CACHE_BUST_SWIFT_MESHES = True
RUN_CACHE_TOKEN = time.time_ns()
DEFAULT_PART_NAME = "Apple"
DEFAULT_CAMERA_DISTANCE = 1.4
DETAIL_LINE_LIMIT = 12

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_PARTS_ROOT = REPO_ROOT / "ir_support_extra_parts"
for path in (REPO_ROOT, EXTRA_PARTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_parts.parts import (  # noqa: E402
    PART_CATEGORIES,
    part_mesh,
    part_names,
    part_path,
    part_reference_url,
)


MESH_CACHE_DIR = None


@dataclass(frozen=True)
class PartOption:
    name: str

    @property
    def label(self):
        return self.name


@dataclass(frozen=True)
class PartBounds:
    minimum: np.ndarray
    maximum: np.ndarray

    @property
    def center(self):
        return (self.minimum + self.maximum) / 2.0

    @property
    def extent(self):
        return np.maximum(self.maximum - self.minimum, 0.0)

    @property
    def max_extent(self):
        return float(max(np.max(self.extent), 1e-6))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Open one IR Support extra part in Swift. Run without arguments "
            "to use the Swift dropdown menu, or pass --part to choose the "
            "initial part."
        )
    )
    parser.add_argument(
        "--part",
        default=DEFAULT_PART_NAME,
        help="Initial part name to inspect, for example Camera or MilkCarton.",
    )
    parser.add_argument(
        "--repeats",
        default=ANIMATION_REPEATS,
        type=int,
        help="Number of repeated bob-and-spin animation cycles.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=HEADLESS,
        help="Run without opening a browser window.",
    )
    parser.add_argument(
        "--no-cache-bust",
        action="store_true",
        help="Load mesh files directly instead of copying them to a temporary path.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print available part names grouped by category and exit.",
    )
    return parser.parse_args(argv)


def available_part_names():
    return list(part_names())


def part_options():
    return [PartOption(name) for name in available_part_names()]


def resolve_part_name(name):
    return part_path(name).stem


def option_index_for(part_name):
    options = part_options()
    try:
        resolved = resolve_part_name(part_name)
    except ValueError:
        resolved = DEFAULT_PART_NAME if DEFAULT_PART_NAME in available_part_names() else options[0].name

    for index, option in enumerate(options):
        if option.name == resolved:
            return index
    return 0


def part_categories_for(part_name):
    resolved = resolve_part_name(part_name)
    categories = [
        category
        for category, names in PART_CATEGORIES.items()
        if resolved in names
    ]
    return categories or ["Uncategorised"]


def default_part_bounds():
    return PartBounds(
        np.array([-0.25, -0.25, 0.0], dtype=float),
        np.array([0.25, 0.25, 0.5], dtype=float),
    )


def _part_bounds_from_dae_positions(source):
    import xml.etree.ElementTree as ET

    root = ET.parse(source).getroot()
    point_sets = []
    for element in root.iter():
        if not element.tag.endswith("float_array"):
            continue
        label = " ".join(
            str(element.attrib.get(key, "")) for key in ("id", "name")
        ).lower()
        if "position" not in label:
            continue
        values = np.fromstring(element.text or "", dtype=float, sep=" ")
        if values.size < 3 or values.size % 3:
            continue
        points = values.reshape((-1, 3))
        if np.isfinite(points).all():
            point_sets.append(points)

    if not point_sets:
        raise ValueError("no DAE position arrays found")

    points = np.vstack(point_sets)
    minimum = points.min(axis=0)
    maximum = points.max(axis=0)
    if np.max(maximum - minimum) <= 0.0:
        raise ValueError("empty DAE position bounds")
    return PartBounds(minimum, maximum)


def estimate_part_bounds(part_name):
    source = part_path(part_name)
    try:
        import trimesh

        loaded = trimesh.load(str(source), force="scene")
        bounds = np.asarray(loaded.bounds, dtype=float)
        if bounds.shape != (2, 3) or not np.isfinite(bounds).all():
            raise ValueError("invalid mesh bounds")
        if np.max(bounds[1] - bounds[0]) <= 0.0:
            raise ValueError("empty mesh bounds")
        return PartBounds(bounds[0], bounds[1])
    except Exception:
        try:
            return _part_bounds_from_dae_positions(source)
        except Exception:
            return default_part_bounds()


def part_alignment_pose(bounds):
    center = bounds.center
    return SE3(-center[0], -center[1], -bounds.minimum[2])


def part_lift_height(bounds):
    return float(np.clip(bounds.max_extent * 0.75, 0.25, 1.0))


def build_part_motion_pose(bounds, phase):
    phase = float(phase) % 1.0
    lift = part_lift_height(bounds) * np.sin(np.pi * phase)
    angle = 2.0 * np.pi * phase
    return SE3(0.0, 0.0, lift) * SE3.Rz(angle) * part_alignment_pose(bounds)


def cache_bust_part_mesh(mesh, part_name, enabled=True):
    if not enabled:
        return mesh

    global MESH_CACHE_DIR
    if MESH_CACHE_DIR is None:
        MESH_CACHE_DIR = Path(tempfile.mkdtemp(prefix="ir_support_swift_part_"))
        print(f"Using Swift mesh cache-bust folder: {MESH_CACHE_DIR}")

    source = part_path(part_name)
    dest = (
        MESH_CACHE_DIR
        / f"{source.stem}_{RUN_CACHE_TOKEN}_{source.stat().st_mtime_ns}{source.suffix}"
    )
    shutil.copy2(source, dest)
    if hasattr(mesh, "filename"):
        mesh.filename = str(dest.resolve())
    return mesh


def format_length(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(value):
        return "-"
    if abs(value) < 5e-5:
        return "0"
    return f"{value:.3f}"


def format_bounds(bounds):
    extent = bounds.extent
    return (
        f"{format_length(extent[0])} x "
        f"{format_length(extent[1])} x "
        f"{format_length(extent[2])} m"
    )


def part_detail_lines(part_name, bounds):
    source = part_path(part_name)
    url = part_reference_url(part_name)
    size_mb = source.stat().st_size / (1024.0 * 1024.0)
    lines = [
        f"Part: {resolve_part_name(part_name)}",
        f"Category: {', '.join(part_categories_for(part_name))}",
        f"DAE file: {source.name}",
        f"File size: {size_mb:.2f} MB",
        f"Bounds: {format_bounds(bounds)}",
        f"Reference URL: {url or 'not set'}",
    ]
    return lines[:DETAIL_LINE_LIMIT]


def make_text_line(swift, text=" "):
    """Create compact read-only sidebar text using Swift's existing widgets."""
    return swift.Radio(lambda _: None, desc=text or " ", options=[], checked=[])


def set_text_line(line, text):
    if line is not None:
        line.desc = text or " "


def update_part_detail_labels(state):
    part_name = state.get("part_name")
    bounds = state.get("bounds")
    if part_name is None or bounds is None:
        return

    lines = part_detail_lines(part_name, bounds)
    detail_labels = state.get("detail_labels", [])
    for label, line in zip(detail_labels, lines):
        set_text_line(label, line)
    for label in detail_labels[len(lines):]:
        set_text_line(label, "")

    url = part_reference_url(part_name)
    state["reference_url"] = url
    button = state.get("reference_button")
    if button is not None:
        button.desc = "Reference URL: Open reference URL" if url else "Reference URL: not set"


def open_reference_url(state):
    url = state.get("reference_url")
    if url:
        webbrowser.open(url)
    else:
        print("No reference URL is set for the loaded part.")


def camera_target(bounds, view_name):
    height = max(float(bounds.extent[2]), 0.2)
    if view_name == "top":
        return np.array([0.0, 0.0, 0.0], dtype=float)
    return np.array([0.0, 0.0, height * 0.5], dtype=float)


def camera_direction(view_name):
    directions = {
        "isometric": np.array([1.0, -1.0, 0.65], dtype=float),
        "front": np.array([1.0, 0.0, 0.25], dtype=float),
        "side": np.array([0.0, -1.0, 0.25], dtype=float),
        "top": np.array([0.0, 0.0, 1.0], dtype=float),
        "close": np.array([0.85, -0.85, 0.45], dtype=float),
    }
    direction = directions[view_name]
    return direction / np.linalg.norm(direction)


def set_part_camera(env, bounds, view_name):
    target = camera_target(bounds, view_name)
    distance_factor = 1.4 if view_name == "close" else 2.4
    distance = max(DEFAULT_CAMERA_DISTANCE, bounds.max_extent * distance_factor)
    if view_name == "top":
        distance = max(DEFAULT_CAMERA_DISTANCE, bounds.max_extent * 2.2)
    position = target + camera_direction(view_name) * distance
    env.set_camera_pose(position, target)


def set_state_camera(env, state, view_name):
    bounds = state.get("bounds")
    if bounds is None:
        return
    set_part_camera(env, bounds, view_name)


def park_mesh_out_of_view(mesh, index=0):
    if mesh is None:
        return
    try:
        mesh.T = SE3(0.0, 0.0, -50.0 - 10.0 * index).A
    except Exception:
        pass


def load_part_option(env, option, cache_bust_enabled=True):
    name = resolve_part_name(option.name)
    bounds = estimate_part_bounds(name)
    mesh = part_mesh(name)
    cache_bust_part_mesh(mesh, name, enabled=cache_bust_enabled)
    mesh.T = build_part_motion_pose(bounds, 0.0).A
    env.add(mesh)
    set_part_camera(env, bounds, "isometric")

    source = part_path(name)
    print(
        f"Loaded {name}: {source.name}, "
        f"bounds {format_bounds(bounds)}, "
        f"size {source.stat().st_size / (1024.0 * 1024.0):.2f} MB"
    )

    return {
        "mesh": mesh,
        "part_name": name,
        "bounds": bounds,
        "step_index": 0,
    }


def replace_loaded_part(env, state, options, cache_bust_enabled=True):
    option = options[state["selected_index"]]
    retired = state.setdefault("retired_meshes", [])
    previous_mesh = state.get("mesh")
    if previous_mesh is not None:
        retired.append(previous_mesh)
        park_mesh_out_of_view(previous_mesh, len(retired))

    loaded = load_part_option(env, option, cache_bust_enabled=cache_bust_enabled)
    state.update(loaded)

    status_label = state.get("status_label")
    if status_label is not None:
        status_label.desc = f"Loaded part: {state['part_name']}"
    update_part_detail_labels(state)


def add_part_controls(env, swift, state, options, headless, cache_bust_enabled):
    if headless:
        return

    env.add(swift.Label("IR Support part viewer"))
    state["status_label"] = swift.Label("Loaded part details will appear here")
    env.add(state["status_label"])

    env.add(swift.Label("Part selection"))

    def on_select(index):
        state["selected_index"] = int(index)
        option = options[state["selected_index"]]
        state["status_label"].desc = f"Selected part: {option.label}"

    env.add(
        swift.Select(
            on_select,
            desc="Part",
            options=[option.label for option in options],
            value=state["selected_index"],
        )
    )
    env.add(
        swift.Button(
            lambda _: replace_loaded_part(env, state, options, cache_bust_enabled),
            desc="Load selected part",
        )
    )

    env.add(swift.Label("Camera views"))
    view_buttons = [
        ("isometric", "Isometric"),
        ("front", "Front"),
        ("side", "Side"),
        ("top", "Top"),
        ("close", "Close-up"),
    ]
    for view_name, button_label in view_buttons:
        env.add(
            swift.Button(
                lambda _, view_name=view_name: set_state_camera(env, state, view_name),
                desc=button_label,
            )
        )

    env.add(swift.Label("Part details"))
    state["detail_labels"] = []
    for _ in range(DETAIL_LINE_LIMIT):
        line = make_text_line(swift)
        state["detail_labels"].append(line)
        env.add(line)

    state["reference_button"] = swift.Button(
        lambda _: open_reference_url(state),
        desc="Reference URL: not set",
    )
    env.add(state["reference_button"])


def animate_current_part(state):
    mesh = state.get("mesh")
    bounds = state.get("bounds")
    if mesh is None or bounds is None:
        return

    index = state.get("step_index", 0)
    phase = (index % ANIMATION_STEPS) / float(ANIMATION_STEPS)
    mesh.T = build_part_motion_pose(bounds, phase).A
    state["step_index"] = index + 1


def print_part_lists():
    print("IR Support extra parts by category:")
    for category, names in PART_CATEGORIES.items():
        print(f"{category} ({len(names)}):")
        print("  " + ", ".join(names))

    uncategorised = sorted(set(part_names()) - {name for names in PART_CATEGORIES.values() for name in names})
    if uncategorised:
        print("Uncategorised:")
        print("  " + ", ".join(uncategorised))


def main(argv=None):
    args = parse_args(argv)
    if args.list:
        print_part_lists()
        return

    import swift

    options = part_options()
    selected_index = option_index_for(args.part)
    state = {"selected_index": selected_index, "retired_meshes": []}
    cache_bust_enabled = not args.no_cache_bust

    print(f"Python executable: {sys.executable}")

    env = swift.Swift()
    env.launch(realtime=True, headless=args.headless)
    add_part_controls(env, swift, state, options, args.headless, cache_bust_enabled)
    replace_loaded_part(env, state, options, cache_bust_enabled)

    print("Animating selected part in Swift...")
    print("Use the Swift side-panel dropdown to choose another part and click Load selected part.")

    total_steps = max(args.repeats, 1) * ANIMATION_STEPS
    for _ in range(total_steps):
        animate_current_part(state)
        env.step(STEP_SECONDS)

    mesh = state.get("mesh")
    bounds = state.get("bounds")
    if mesh is not None and bounds is not None:
        mesh.T = build_part_motion_pose(bounds, 0.0).A
        env.step(STEP_SECONDS)
    print("Animation complete.")

    if args.headless:
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




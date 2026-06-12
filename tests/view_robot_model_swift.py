"""Inspect one IR Support robot in Swift.

Most convenient use from VS Code
--------------------------------
Run this file directly, for example with Ctrl+F5. Swift opens with UR3e loaded.
Use the dropdown in the Swift side panel to choose any core or extra robot, then
click "Load selected robot". The currently loaded robot animates all joints and
the camera buttons jump to useful inspection views.

Command-line examples
---------------------
These examples assume the command line is using the same Python environment as VS Code. If bare python points to another Python install, activate the project virtual environment first or call that environment's Python executable directly.

List all robot names:

    python tests/view_robot_model_swift.py --list

Open a particular robot as the initial selection:

    python tests/view_robot_model_swift.py --package extra --robot DensoVP6242
    python tests/view_robot_model_swift.py --package core --robot UR3e

The viewer copies mesh files to a temporary folder before loading them in Swift.
That avoids stale browser-cached DAE files while model geometry is being edited.
"""

import argparse
import inspect
import shutil
import sys
import tempfile
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3


HEADLESS = False
WAIT_FOR_ENTER_BEFORE_CLOSING = True
ANIMATION_STEPS = 80
ANIMATION_REPEATS = 100
STEP_SECONDS = 0.03
CACHE_BUST_SWIFT_MESHES = True
RUN_CACHE_TOKEN = time.time_ns()
DETAIL_LINE_LIMIT = 20
REFERENCE_URL_ATTRIBUTES = ("manufacturer_url", "product_url", "reference_url", "documentation_url")

# These only choose the robot loaded when the file first starts. Once Swift is
# open, use the side-panel dropdown and "Load selected robot" button.
DEFAULT_ROBOT_NAME = "UR3e"
DEFAULT_PACKAGE = "auto"
CORE_NON_ROBOT_EXPORTS = {"schunk_UTS_v2_0", "DHRobot3D", "UTSMeshRobot"}

REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_ROBOTS_ROOT = REPO_ROOT / "ir_support_extra_robots"
for path in (REPO_ROOT, EXTRA_ROBOTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

MESH_CACHE_DIR = None


@dataclass(frozen=True)
class RobotOption:
    package: str
    name: str

    @property
    def label(self):
        return f"{self.package}: {self.name}"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Open a robot in Swift. Run without arguments to use the Swift "
            "dropdown menu, or pass --robot and --package to choose the "
            "initial robot."
        )
    )
    parser.add_argument(
        "--robot",
        default=DEFAULT_ROBOT_NAME,
        help="Initial robot class name to inspect, for example UR3e or DensoVP6242.",
    )
    parser.add_argument(
        "--package",
        default=DEFAULT_PACKAGE,
        choices=("auto", "core", "extra"),
        help="Where to find the initial robot. The Swift dropdown can still load any robot.",
    )
    parser.add_argument(
        "--repeats",
        default=ANIMATION_REPEATS,
        type=int,
        help="Number of repeated out-and-back motion cycles.",
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
        help="Print available core and extra robot names and exit.",
    )
    return parser.parse_args(argv)


def robot_modules():
    import ir_support.robots as core_robots
    import ir_support_extra_robots.robots as extra_robots

    return core_robots, extra_robots


def available_robot_names():
    core_robots, extra_robots = robot_modules()
    return {
        "core": [
            name for name in core_robots.__all__ if name not in CORE_NON_ROBOT_EXPORTS
        ],
        "extra": list(extra_robots.__all__),
    }


def robot_options():
    names = available_robot_names()
    return [
        *(RobotOption("core", name) for name in names["core"]),
        *(RobotOption("extra", name) for name in names["extra"]),
    ]


def option_index_for(robot_name, package_name=DEFAULT_PACKAGE):
    options = robot_options()
    for index, option in enumerate(options):
        if option.name == robot_name and package_name in ("auto", option.package):
            return index
    return option_index_for(DEFAULT_ROBOT_NAME, "core") if robot_name != DEFAULT_ROBOT_NAME else 0


def resolve_robot_factory(robot_name, package_name=DEFAULT_PACKAGE):
    core_robots, extra_robots = robot_modules()
    robot_name = robot_name.strip()
    candidates = []

    names = available_robot_names()

    if package_name in ("auto", "core") and robot_name in names["core"]:
        candidates.append((getattr(core_robots, robot_name), "core"))

    if package_name in ("auto", "extra") and robot_name in names["extra"]:
        candidates.append((getattr(extra_robots, robot_name), "extra"))

    if candidates:
        return candidates[0]

    core_list = ", ".join(names["core"])
    extra_list = ", ".join(names["extra"])
    raise ValueError(
        f"Unknown robot '{robot_name}' for package '{package_name}'.\n"
        f"Core robots: {core_list}\n"
        f"Extra robots: {extra_list}"
    )


def instantiate_robot(factory, base=None):
    base = SE3() if base is None else base
    signature = inspect.signature(factory)
    if "base" in signature.parameters:
        return factory(base=base)

    robot = factory()
    try:
        robot.base = base * robot.base
    except Exception:
        robot.base = base
    return robot


def robot_home_q(robot):
    home_q = getattr(robot, "home_q", None)
    if home_q is None:
        return np.zeros(robot.n)
    return np.asarray(home_q, dtype=float).reshape(robot.n)


def joint_limits(robot, index):
    qlim = getattr(robot, "qlim", None)
    if qlim is not None:
        qlim = np.asarray(qlim, dtype=float)
        if qlim.shape == (2, robot.n):
            return qlim[0, index], qlim[1, index]

    link_qlim = getattr(robot.links[index], "qlim", None)
    if link_qlim is not None:
        link_qlim = np.asarray(link_qlim, dtype=float).reshape(-1)
        if link_qlim.size == 2:
            return link_qlim[0], link_qlim[1]

    return np.nan, np.nan


def is_prismatic_link(robot, index):
    return bool(getattr(robot.links[index], "isprismatic", False))


def finite_joint_range(robot, index):
    lower, upper = joint_limits(robot, index)
    if np.isfinite(lower) and np.isfinite(upper) and upper > lower:
        return lower, upper, upper - lower
    return lower, upper, np.nan


def build_motion_delta(robot):
    delta = np.zeros(robot.n)
    for index in range(robot.n):
        lower, upper, joint_range = finite_joint_range(robot, index)
        if np.isfinite(joint_range):
            if joint_range < 1e-9:
                continue
            if is_prismatic_link(robot, index):
                amplitude = min(0.12, max(0.02, 0.20 * joint_range))
            else:
                amplitude = min(0.35, max(0.08, 0.20 * joint_range))
        else:
            amplitude = 0.08 if is_prismatic_link(robot, index) else 0.25

        direction = 1.0 if index % 2 == 0 else -1.0
        delta[index] = direction * amplitude

    return delta


def clamp_to_joint_limits(robot, q):
    q = np.asarray(q, dtype=float).copy()
    for index in range(robot.n):
        lower, upper, _ = finite_joint_range(robot, index)
        if not (np.isfinite(lower) and np.isfinite(upper)):
            continue
        if upper - lower < 1e-9:
            q[index] = lower
        else:
            q[index] = np.clip(q[index], lower, upper)
    return q


def build_motion_goal(robot):
    home_q = robot_home_q(robot)
    goal_q = clamp_to_joint_limits(robot, home_q + build_motion_delta(robot))
    if np.allclose(goal_q, home_q) and robot.n:
        goal_q[0] = home_q[0] + (0.06 if not is_prismatic_link(robot, 0) else 0.02)
        goal_q = clamp_to_joint_limits(robot, goal_q)
    return goal_q


def base_position(robot):
    try:
        return np.asarray(robot.base.t, dtype=float).reshape(3)
    except Exception:
        return np.zeros(3)


def fk_position(robot, q):
    return np.asarray(robot.fkine(q).t, dtype=float).reshape(3)


def estimate_robot_reach(robot, home_q, goal_q):
    origin = base_position(robot)
    samples = [home_q, goal_q, clamp_to_joint_limits(robot, 2.0 * home_q - goal_q)]
    distances = []
    for q in samples:
        try:
            distances.append(float(np.linalg.norm(fk_position(robot, q) - origin)))
        except Exception:
            pass

    dh_extent = 0.0
    for link in robot.links:
        for attr in ("a", "d"):
            value = getattr(link, attr, 0.0)
            try:
                value = float(value)
            except (TypeError, ValueError):
                value = 0.0
            if np.isfinite(value):
                dh_extent += abs(value)

    return min(max([0.6, dh_extent, *distances]), 8.0)


def format_model_value(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(value):
        return "-"
    if abs(value) < 5e-5:
        return "0"
    return f"{value:.3f}"


def robot_reference_url(robot):
    for attribute in REFERENCE_URL_ATTRIBUTES:
        value = getattr(robot, attribute, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def robot_dh_rows(robot):
    rows = []
    for index, link in enumerate(getattr(robot, "links", []), start=1):
        if not all(hasattr(link, attribute) for attribute in ("d", "a", "alpha")):
            return []
        offset = getattr(link, "offset", 0.0)
        rows.append(
            f"q{index}: d={format_model_value(link.d)} "
            f"a={format_model_value(link.a)} "
            f"alpha={format_model_value(link.alpha)} "
            f"off={format_model_value(offset)}"
        )
    return rows


def robot_detail_lines(robot, reach):
    url = robot_reference_url(robot)
    lines = [
        f"DOF: {robot.n}",
        f"Model reach estimate: {reach:.2f} m",
    ]
    if url:
        lines.append(f"Reference URL: {url}")
    else:
        lines.append("Reference URL: not set")

    dh_rows = robot_dh_rows(robot)
    if dh_rows:
        lines.append("DH parameters from model")
        lines.extend(dh_rows)
    else:
        lines.append("DH parameters: not available for this model type")

    return lines[:DETAIL_LINE_LIMIT]


def make_text_line(swift, text=" "):
    """Create compact read-only sidebar text using Swift's existing widgets."""
    return swift.Radio(lambda _: None, desc=text or " ", options=[], checked=[])


def set_text_line(line, text):
    if line is not None:
        line.desc = text or " "


def ensure_dh_row_labels(state, count):
    env = state.get("env")
    swift = state.get("swift")
    row_labels = state.setdefault("dh_row_labels", [])
    if env is None or swift is None:
        return row_labels

    while len(row_labels) < count:
        row_label = make_text_line(swift)
        row_labels.append(row_label)
        env.add(row_label)
    return row_labels


def update_robot_detail_labels(state):
    robot = state.get("robot")
    if robot is None:
        return

    reach = state.get("reach", 0.0)
    set_text_line(state.get("dof_label"), f"DOF: {robot.n}")
    set_text_line(state.get("reach_label"), f"Reach: {reach:.2f} m")

    url = robot_reference_url(robot)
    state["reference_url"] = url
    set_text_line(state.get("reference_url_label"), f"URL: {url or 'not set'}")
    button = state.get("reference_button")
    if button is not None:
        button.desc = "Reference URL: Open reference URL" if url else "Reference URL: not set"

    dh_rows = robot_dh_rows(robot)
    heading = state.get("dh_heading")
    if heading is not None:
        heading.desc = "DH parameters from model" if dh_rows else "DH parameters"

    if not dh_rows:
        row_labels = ensure_dh_row_labels(state, 1)
        if row_labels:
            set_text_line(row_labels[0], "not available for this model type")
        for row_label in row_labels[1:]:
            set_text_line(row_label, "")
        return

    row_labels = ensure_dh_row_labels(state, len(dh_rows))
    for row_label, row in zip(row_labels, dh_rows):
        set_text_line(row_label, row)
    for row_label in row_labels[len(dh_rows):]:
        set_text_line(row_label, "")


def open_reference_url(state):
    url = state.get("reference_url")
    if url:
        webbrowser.open(url)
    else:
        print("No reference URL is set for the loaded robot.")

def cache_bust_robot_meshes(robot, enabled=True):
    if not enabled:
        return

    links_3d = getattr(robot, "links_3d", [])
    if not links_3d:
        return

    global MESH_CACHE_DIR
    if MESH_CACHE_DIR is None:
        MESH_CACHE_DIR = Path(tempfile.mkdtemp(prefix="ir_support_swift_robot_"))
        print(f"Using Swift mesh cache-bust folder: {MESH_CACHE_DIR}")

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


def camera_target(robot, view_name):
    if view_name == "wrist":
        try:
            return fk_position(robot, robot.q)
        except Exception:
            pass
    origin = base_position(robot)
    return origin + np.array([0.0, 0.0, 0.45])


def camera_direction(view_name):
    directions = {
        "isometric": np.array([1.0, -1.0, 0.65]),
        "front": np.array([1.0, 0.0, 0.35]),
        "side": np.array([0.0, -1.0, 0.35]),
        "top": np.array([0.0, 0.0, 1.0]),
        "wrist": np.array([0.8, -0.8, 0.45]),
    }
    direction = directions[view_name]
    return direction / np.linalg.norm(direction)


def set_robot_camera(env, robot, view_name, reach):
    target = camera_target(robot, view_name)
    distance = max(1.2, reach * (2.4 if view_name != "wrist" else 1.4))
    position = target + camera_direction(view_name) * distance
    env.set_camera_pose(position, target)


def set_state_camera(env, state, view_name):
    robot = state.get("robot")
    if robot is None:
        return
    set_robot_camera(env, robot, view_name, state.get("reach", 1.0))


def add_robot_to_env(env, robot):
    """Add either an IR Support mesh robot or a Robotics Toolbox robot to Swift."""
    add_to_env = getattr(robot, "add_to_env", None)
    if callable(add_to_env):
        add_to_env(env)
        return "mesh"

    env.add(robot)
    return "robot"


def park_robot_out_of_view(robot, index=0):
    """Move a previously loaded robot away without using Swift.remove().

    Some Swift versions leave None placeholders in their internal object list
    after removing mesh shapes. The next env.step() can then fail while walking
    the scene tree. Parking old robots avoids that fragile removal path while
    still letting the selected robot be inspected on the ground plane.
    """
    if robot is None:
        return

    parked_base = SE3(0.0, 0.0, -50.0 - 10.0 * index)
    try:
        robot.base = parked_base
        robot.q = robot_home_q(robot)
        return
    except Exception:
        pass

    for mesh in getattr(robot, "links_3d", []):
        try:
            mesh.T = parked_base.A
        except Exception:
            pass


def load_robot_option(env, option, cache_bust_enabled=True):
    factory, package_name = resolve_robot_factory(option.name, option.package)
    robot = instantiate_robot(factory)
    home_q = robot_home_q(robot)
    goal_q = build_motion_goal(robot)
    reach = estimate_robot_reach(robot, home_q, goal_q)
    trajectory = np.vstack(
        (
            rtb.jtraj(home_q, goal_q, ANIMATION_STEPS).q,
            rtb.jtraj(goal_q, home_q, ANIMATION_STEPS).q,
        )
    )

    robot.q = home_q.copy()
    cache_bust_robot_meshes(robot, enabled=cache_bust_enabled)
    add_method = add_robot_to_env(env, robot)
    set_robot_camera(env, robot, "isometric", reach)

    print(
        f"Loaded {option.name} from {package_name}: "
        f"{robot.n} joints, {len(getattr(robot, 'links_3d', []))} meshes, added as {add_method}, "
        f"estimated reach {reach:.2f} m"
    )
    print(f"home_q = {np.array2string(home_q, precision=3)}")
    print(f"goal_q = {np.array2string(goal_q, precision=3)}")

    return {
        "robot": robot,
        "option": option,
        "home_q": home_q,
        "goal_q": goal_q,
        "reach": reach,
        "trajectory": trajectory,
        "trajectory_index": 0,
    }


def replace_loaded_robot(env, state, options, cache_bust_enabled=True):
    option = options[state["selected_index"]]
    retired = state.setdefault("retired_robots", [])
    previous_robot = state.get("robot")
    if previous_robot is not None:
        retired.append(previous_robot)
        park_robot_out_of_view(previous_robot, len(retired))
    loaded = load_robot_option(env, option, cache_bust_enabled=cache_bust_enabled)
    state.update(loaded)
    status_label = state.get("status_label")
    if status_label is not None:
        status_label.desc = f"Loaded: {option.package}: {option.name} ({state['robot'].n} joints)"
    update_robot_detail_labels(state)


def add_robot_controls(env, swift, state, options, headless, cache_bust_enabled):
    if headless:
        return

    env.add(swift.Label("IR Support robot viewer"))
    state["status_label"] = swift.Label("Loaded robot details will appear here")
    env.add(state["status_label"])

    env.add(swift.Label("Robot selection"))

    def on_select(index):
        state["selected_index"] = int(index)
        option = options[state["selected_index"]]
        state["status_label"].desc = f"Selected: {option.label}"

    env.add(
        swift.Select(
            on_select,
            desc="Robot",
            options=[option.label for option in options],
            value=state["selected_index"],
        )
    )
    env.add(
        swift.Button(
            lambda _: replace_loaded_robot(env, state, options, cache_bust_enabled),
            desc="Load selected robot",
        )
    )

    env.add(swift.Label("Camera views"))
    view_buttons = [
        ("isometric", "Isometric"),
        ("front", "Front"),
        ("side", "Side"),
        ("top", "Top"),
        ("wrist", "Wrist close-up"),
    ]
    for view_name, button_label in view_buttons:
        env.add(
            swift.Button(
                lambda _, view_name=view_name: set_state_camera(env, state, view_name),
                desc=button_label,
            )
        )

    state["env"] = env
    state["swift"] = swift

    env.add(swift.Label("Robot details"))
    state["dof_label"] = make_text_line(swift, "DOF: -")
    env.add(state["dof_label"])
    state["reach_label"] = make_text_line(swift, "Reach: -")
    env.add(state["reach_label"])

    state["reference_button"] = swift.Button(
        lambda _: open_reference_url(state),
        desc="Reference URL: not set",
    )
    env.add(state["reference_button"])
    state["reference_url_label"] = make_text_line(swift, "URL: not set")
    env.add(state["reference_url_label"])

    state["dh_heading"] = swift.Label("DH parameters")
    env.add(state["dh_heading"])
    state["dh_row_labels"] = []


def animate_current_robot(state):
    robot = state.get("robot")
    trajectory = state.get("trajectory")
    if robot is None or trajectory is None:
        return

    index = state.get("trajectory_index", 0) % trajectory.shape[0]
    robot.q = trajectory[index]
    state["trajectory_index"] = index + 1


def print_robot_lists():
    names = available_robot_names()
    print("Core robots:")
    print("  " + ", ".join(names["core"]))
    print("Extra robots:")
    print("  " + ", ".join(names["extra"]))


def main(argv=None):
    args = parse_args(argv)
    if args.list:
        print_robot_lists()
        return

    import swift

    options = robot_options()
    selected_index = option_index_for(args.robot, args.package)
    state = {"selected_index": selected_index, "retired_robots": []}
    cache_bust_enabled = not args.no_cache_bust

    print(f"Python executable: {sys.executable}")

    env = swift.Swift()
    env.launch(realtime=True, headless=args.headless)
    add_robot_controls(env, swift, state, options, args.headless, cache_bust_enabled)
    replace_loaded_robot(env, state, options, cache_bust_enabled)

    print("Animating all joints in Swift...")
    print("Use the Swift side-panel dropdown to choose another robot and click Load selected robot.")

    total_steps = max(args.repeats, 1) * ANIMATION_STEPS * 2
    for _ in range(total_steps):
        animate_current_robot(state)
        env.step(STEP_SECONDS)

    robot = state.get("robot")
    if robot is not None:
        robot.q = state["home_q"].copy()
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










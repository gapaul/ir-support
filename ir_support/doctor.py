"""Diagnose and patch known upstream environment issues for IR Support.

This module intentionally avoids importing Robotics Toolbox or Swift so it can
still run when one of those packages has a local syntax or version problem.
"""

from __future__ import annotations

import argparse
import importlib.metadata as metadata
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SWIFT_RELATIVE = Path("swift") / "Swift.py"
SWIFT_ROUTE_RELATIVE = Path("swift") / "SwiftRoute.py"
ROBOT_PLOT_RELATIVE = Path("roboticstoolbox") / "backends" / "PyPlot" / "RobotPlot.py"
MACHINEVISION_SOURCES_RELATIVE = Path("machinevisiontoolbox") / "Sources.py"

SWIFT_ROUTE_OLD = "self.path = urllib.parse.unquote(self.path[9:])"
SWIFT_ROUTE_NEW = "self.path = urllib.parse.unquote(self.path[10:])"
SWIFT_CONNECT_TIMEOUT_OLD = "            inq.get(timeout=10)"
SWIFT_CONNECT_TIMEOUT_NEW = '            inq.get(timeout=float(os.environ.get("IR_SUPPORT_SWIFT_CONNECT_TIMEOUT", "30")))'
SWIFT_ROUTE_JSON_DEFAULT_MARKER = "def _ir_support_json_default"
SWIFT_ROUTE_JSON_DEFAULT_ANCHOR = "from typing_extensions import Literal as L\n"
SWIFT_ROUTE_JSON_DEFAULT_BLOCK = """

def _ir_support_json_default(value):
    if hasattr(value, "tolist"):
        return value.tolist()
    raise TypeError(f"Object of type {value.__class__.__name__} is not JSON serializable")
"""
SWIFT_ROUTE_JSON_DUMPS_OLD = "json.dumps(msg)"
SWIFT_ROUTE_JSON_DUMPS_NEW = "json.dumps(msg, default=_ir_support_json_default)"
SWIFT_HTTP_RESET_MARKER = "except ConnectionResetError:"
SWIFT_HTTP_HANDLER_OLD = """            def __init__(self, *args, **kwargs):
                super(MyHttpRequestHandler, self).__init__(
                    *args, directory=str(root_dir), **kwargs
                )

            def log_message(self, format, *args):
"""
SWIFT_HTTP_HANDLER_NEW = """            def __init__(self, *args, **kwargs):
                super(MyHttpRequestHandler, self).__init__(
                    *args, directory=str(root_dir), **kwargs
                )

            def handle(self):
                try:
                    super().handle()
                except ConnectionResetError:
                    pass

            def log_message(self, format, *args):
"""

ROBOT_PLOT_FIXED_BLOCK = [
    "        if options is not None:",
    "            for key, value in options.items():",
    "                if isinstance(defaults[key], dict) and isinstance(options[key], dict):",
    "                    defaults[key] = {**defaults[key], **options[key]}",
    "                else:",
    "                    defaults[key] = options[key]",
]
ROBOT_PLOT_OPTIONS_START = "        if options is not None:"
ROBOT_PLOT_OPTIONS_END = "        self.options = defaults"
ROBOT_PLOT_OLD_MERGE = "defaults[key] = {**defaults[key], **options[key]}"

MACHINEVISION_OLD_IMPORT = "from numpy.char import array"
MACHINEVISION_NEW_IMPORT = "from numpy import array"

SWIFT_TIMEOUT_MARKER = "Timed out waiting for Swift browser response"
SWIFT_QUEUE_IMPORT_OLD = "from queue import Queue"
SWIFT_QUEUE_IMPORT_NEW = "from queue import Queue, Empty"
SWIFT_SEND_SOCKET_OLD = """    def _send_socket(self, code, data=None, expected=True):
        msg = [expected, [code, data]]

        self.outq.put(msg)

        if expected:
            return self.inq.get()
        else:
            return "0"
"""
SWIFT_SEND_SOCKET_NEW = """    def _send_socket(self, code, data=None, expected=True, timeout=None):
        msg = [expected, [code, data]]

        self.outq.put(msg)

        if expected:
            if timeout is None:
                timeout = getattr(self, "_ir_support_socket_timeout", 20.0)
            try:
                return self.inq.get(timeout=timeout)
            except Empty as exc:
                raise TimeoutError(
                    f"Timed out waiting for Swift browser response to {code!r}. "
                    "Check that the Swift browser page is open and connected."
                ) from exc
        else:
            return "0"
"""
SWIFT_SHAPE_MOUNT_OLD = """                while not int(self._send_socket("shape_mounted", [id, 1])):
                    time.sleep(0.1)
"""
SWIFT_SHAPE_MOUNT_NEW = """                mount_deadline = time.time() + getattr(self, "_ir_support_mount_timeout", 20.0)
                while not int(self._send_socket("shape_mounted", [id, 1])):
                    if time.time() > mount_deadline:
                        raise TimeoutError(
                            "Timed out waiting for Swift browser to mount shape. "
                            "Check that the Swift browser page is open and connected."
                        )
                    time.sleep(0.1)
"""
SWIFT_ROBOT_MOUNT_OLD = """                while not int(self._send_socket("shape_mounted", [id, len(robob)])):
                    time.sleep(0.1)
"""
SWIFT_ROBOT_MOUNT_NEW = """                mount_deadline = time.time() + getattr(self, "_ir_support_mount_timeout", 20.0)
                while not int(self._send_socket("shape_mounted", [id, len(robob)])):
                    if time.time() > mount_deadline:
                        raise TimeoutError(
                            "Timed out waiting for Swift browser to mount robot. "
                            "Check that the Swift browser page is open and connected."
                        )
                    time.sleep(0.1)
"""
SWIFT_SHAPE_UPDATE_MARKER = "Swift 1.1.0 browser bundle has no shape_update handler"
SWIFT_SHAPE_UPDATE_OLD = """        if shape._changed:
            shape._changed = False
            id = self.swift_objects.index(shape)
            self._send_socket("shape_update", [id, shape.to_dict()])
"""
SWIFT_SHAPE_UPDATE_NEW = """        if shape._changed:
            shape._changed = False
            # Swift 1.1.0 browser bundle has no shape_update handler.
            # Pose updates are sent below through shape_poses during render.
"""
SWIFT_HEADLESS_CLOSE_MARKER = 'hasattr(self, "server")'
SWIFT_STOP_THREADS_OLD = """    def _stop_threads(self):
        self._run_thread = False
        if not self.headless:
            self.socket.join(1)
        if not self._dev:
            self.server.join(1)
"""
SWIFT_STOP_THREADS_NEW = """    def _stop_threads(self):
        self._run_thread = False
        if not self.headless and hasattr(self, "socket"):
            self.socket.join(1)
        if not self.headless and not self._dev and hasattr(self, "server"):
            self.server.join(1)
"""
SWIFT_CANVAS_CHUNK_RELATIVE = Path("swift") / "out" / "_next" / "static" / "chunks" / "pages"
SWIFT_CANVAS_FIXED = "preserveDrawingBuffer:!0"
SWIFT_CANVAS_OLD = "gl:{antialias:!0}"
SWIFT_CANVAS_NEW = "gl:{antialias:!0,preserveDrawingBuffer:!0}"


@dataclass
class DoctorResult:
    name: str
    status: str
    detail: str


def _site_path_candidates(relative_path: Path) -> list[Path]:
    candidates: list[Path] = []
    seen: set[Path] = set()
    for entry in sys.path:
        if not entry:
            continue
        candidate = (Path(entry) / relative_path).resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            candidates.append(candidate)
    return candidates


def _first_site_path(relative_path: Path) -> Path | None:
    candidates = _site_path_candidates(relative_path)
    return candidates[0] if candidates else None


def _swift_canvas_chunk_path() -> Path | None:
    for chunk_dir in _site_path_candidates(SWIFT_CANVAS_CHUNK_RELATIVE):
        candidates = sorted(chunk_dir.glob("index-*.js"))
        if candidates:
            return candidates[0]
    return None


def _backup_file(path: Path) -> Path:
    backup = path.with_name(f"{path.name}.ir_support_backup")
    if not backup.exists():
        shutil.copy2(path, backup)
    return backup


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def check_websockets(patch: bool = False) -> DoctorResult:
    try:
        version = metadata.version("websockets")
    except metadata.PackageNotFoundError:
        return DoctorResult(
            "websockets",
            "ISSUE",
            "websockets is not installed; Swift will not run until it is installed.",
        )

    try:
        major = int(version.split(".", 1)[0])
    except ValueError:
        return DoctorResult(
            "websockets",
            "WARN",
            f"Installed websockets version is {version}; could not parse the major version.",
        )

    if major < 14:
        return DoctorResult(
            "websockets",
            "OK",
            f"Installed websockets version is {version}; this is compatible with the current Swift workaround.",
        )

    if not patch:
        return DoctorResult(
            "websockets",
            "ISSUE",
            f"Installed websockets version is {version}; Swift may raise 'no running event loop'. Run again with --patch to install websockets>=10.4,<14.0.",
        )

    command = [sys.executable, "-m", "pip", "install", "websockets>=10.4,<14.0"]
    completed = subprocess.run(command, check=False, text=True, capture_output=True)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "pip did not report a reason."
        return DoctorResult("websockets", "FAILED", f"Could not install compatible websockets package: {detail}")

    return DoctorResult("websockets", "PATCHED", "Installed websockets>=10.4,<14.0 in this Python environment.")


def check_swift_route(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_ROUTE_RELATIVE)
    if path is None:
        return DoctorResult("SwiftRoute.py", "SKIP", "Could not find swift/SwiftRoute.py in this Python environment.")

    text = _read_text(path)
    if SWIFT_ROUTE_NEW in text:
        return DoctorResult("SwiftRoute.py", "OK", f"Path fix is already present in {path}.")

    if SWIFT_ROUTE_OLD not in text:
        return DoctorResult("SwiftRoute.py", "WARN", f"Could not find the expected SwiftRoute.py line in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("SwiftRoute.py", "ISSUE", f"Windows path fix is not applied in {path}. Run again with --patch to change [9:] to [10:].")

    _backup_file(path)
    _write_text(path, text.replace(SWIFT_ROUTE_OLD, SWIFT_ROUTE_NEW, 1))
    return DoctorResult("SwiftRoute.py", "PATCHED", f"Applied Windows path fix in {path}.")


def check_swift_connect_timeout(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_ROUTE_RELATIVE)
    if path is None:
        return DoctorResult("Swift connect timeout", "SKIP", "Could not find swift/SwiftRoute.py in this Python environment.")

    text = _read_text(path)
    if SWIFT_CONNECT_TIMEOUT_NEW in text:
        return DoctorResult("Swift connect timeout", "OK", f"Swift browser connection timeout is configurable in {path}.")

    if SWIFT_CONNECT_TIMEOUT_OLD not in text:
        return DoctorResult("Swift connect timeout", "WARN", f"Could not recognise Swift's browser connection timeout in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift connect timeout", "ISSUE", f"Swift browser connection timeout is short in {path}. Run again with --patch to make it configurable.")

    _backup_file(path)
    _write_text(path, text.replace(SWIFT_CONNECT_TIMEOUT_OLD, SWIFT_CONNECT_TIMEOUT_NEW, 1))
    return DoctorResult("Swift connect timeout", "PATCHED", f"Made Swift browser connection timeout configurable in {path}.")


def check_swift_json_serialisation(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_ROUTE_RELATIVE)
    if path is None:
        return DoctorResult("Swift JSON", "SKIP", "Could not find swift/SwiftRoute.py in this Python environment.")

    text = _read_text(path)
    if SWIFT_ROUTE_JSON_DEFAULT_MARKER in text and SWIFT_ROUTE_JSON_DUMPS_NEW in text:
        return DoctorResult("Swift JSON", "OK", f"Swift JSON serialisation fix is already present in {path}.")

    if SWIFT_ROUTE_JSON_DEFAULT_ANCHOR not in text or SWIFT_ROUTE_JSON_DUMPS_OLD not in text:
        return DoctorResult("Swift JSON", "WARN", f"Could not recognise Swift's JSON send path in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift JSON", "ISSUE", f"Swift may fail to send NumPy scalar values to the browser in {path}. Run again with --patch to add a safe JSON encoder.")

    patched = text.replace(
        SWIFT_ROUTE_JSON_DEFAULT_ANCHOR,
        SWIFT_ROUTE_JSON_DEFAULT_ANCHOR + SWIFT_ROUTE_JSON_DEFAULT_BLOCK,
        1,
    )
    patched = patched.replace(SWIFT_ROUTE_JSON_DUMPS_OLD, SWIFT_ROUTE_JSON_DUMPS_NEW)
    _backup_file(path)
    _write_text(path, patched)
    return DoctorResult("Swift JSON", "PATCHED", f"Added safe Swift JSON serialisation in {path}.")


def check_swift_http_reset(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_ROUTE_RELATIVE)
    if path is None:
        return DoctorResult("Swift HTTP reset", "SKIP", "Could not find swift/SwiftRoute.py in this Python environment.")

    text = _read_text(path)
    if SWIFT_HTTP_RESET_MARKER in text:
        return DoctorResult("Swift HTTP reset", "OK", f"Swift HTTP reset handling is already present in {path}.")

    if SWIFT_HTTP_HANDLER_OLD not in text:
        return DoctorResult("Swift HTTP reset", "WARN", f"Could not recognise Swift's HTTP request handler in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift HTTP reset", "ISSUE", f"Swift may print HTTP ConnectionResetError noise during browser shutdown in {path}. Run again with --patch to suppress expected reset errors.")

    _backup_file(path)
    _write_text(path, text.replace(SWIFT_HTTP_HANDLER_OLD, SWIFT_HTTP_HANDLER_NEW, 1))
    return DoctorResult("Swift HTTP reset", "PATCHED", f"Suppressed expected Swift HTTP reset errors in {path}.")


def check_swift_canvas_buffer(patch: bool = False) -> DoctorResult:
    path = _swift_canvas_chunk_path()
    if path is None:
        return DoctorResult("Swift canvas", "SKIP", "Could not find Swift's bundled browser canvas script in this Python environment.")

    text = _read_text(path)
    if SWIFT_CANVAS_FIXED in text:
        return DoctorResult("Swift canvas", "OK", f"Swift canvas readback support is already present in {path}.")

    if SWIFT_CANVAS_OLD not in text:
        return DoctorResult("Swift canvas", "WARN", f"Could not recognise Swift's canvas renderer options in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift canvas", "ISSUE", f"Swift canvas readback may be unreliable in {path}. Run again with --patch to preserve the WebGL drawing buffer.")

    _backup_file(path)
    _write_text(path, text.replace(SWIFT_CANVAS_OLD, SWIFT_CANVAS_NEW, 1))
    return DoctorResult("Swift canvas", "PATCHED", f"Enabled Swift WebGL drawing-buffer preservation in {path}.")


def check_swift_headless_close(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_RELATIVE)
    if path is None:
        return DoctorResult("Swift headless close", "SKIP", "Could not find swift/Swift.py in this Python environment.")

    text = _read_text(path)
    if SWIFT_HEADLESS_CLOSE_MARKER in text:
        return DoctorResult("Swift headless close", "OK", f"Swift headless close fix is already present in {path}.")

    if SWIFT_STOP_THREADS_OLD not in text:
        return DoctorResult("Swift headless close", "WARN", f"Could not recognise Swift's _stop_threads block in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift headless close", "ISSUE", f"Swift headless close may fail in {path}. Run again with --patch to guard missing browser threads.")

    _backup_file(path)
    _write_text(path, text.replace(SWIFT_STOP_THREADS_OLD, SWIFT_STOP_THREADS_NEW, 1))
    return DoctorResult("Swift headless close", "PATCHED", f"Guarded missing Swift browser threads in {path}.")


def check_swift_shape_update(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_RELATIVE)
    if path is None:
        return DoctorResult("Swift shape update", "SKIP", "Could not find swift/Swift.py in this Python environment.")

    chunk_path = _swift_canvas_chunk_path()
    if chunk_path is not None and "shape_update" in _read_text(chunk_path):
        return DoctorResult("Swift shape update", "OK", f"Swift browser bundle already supports shape_update in {chunk_path}.")

    text = _read_text(path)
    if SWIFT_SHAPE_UPDATE_MARKER in text:
        return DoctorResult("Swift shape update", "OK", f"Unsupported Swift shape_update sends are already disabled in {path}.")

    if SWIFT_SHAPE_UPDATE_OLD not in text:
        return DoctorResult("Swift shape update", "WARN", f"Could not recognise Swift's shape_update send block in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift shape update", "ISSUE", f"Swift browser bundle does not handle shape_update messages from {path}. Run again with --patch to disable that unsupported send path.")

    _backup_file(path)
    _write_text(path, text.replace(SWIFT_SHAPE_UPDATE_OLD, SWIFT_SHAPE_UPDATE_NEW, 1))
    return DoctorResult("Swift shape update", "PATCHED", f"Disabled unsupported Swift shape_update sends in {path}.")


def check_swift_socket_timeouts(patch: bool = False) -> DoctorResult:
    path = _first_site_path(SWIFT_RELATIVE)
    if path is None:
        return DoctorResult("Swift.py", "SKIP", "Could not find swift/Swift.py in this Python environment.")

    text = _read_text(path)
    if SWIFT_TIMEOUT_MARKER in text:
        return DoctorResult("Swift.py", "OK", f"Swift socket timeout patch is already present in {path}.")

    required_snippets = [
        SWIFT_SEND_SOCKET_OLD,
        SWIFT_SHAPE_MOUNT_OLD,
        SWIFT_ROBOT_MOUNT_OLD,
    ]
    missing_snippets = [snippet for snippet in required_snippets if snippet not in text]
    if SWIFT_QUEUE_IMPORT_OLD not in text and SWIFT_QUEUE_IMPORT_NEW not in text:
        missing_snippets.append(SWIFT_QUEUE_IMPORT_OLD)
    if missing_snippets:
        return DoctorResult("Swift.py", "WARN", f"Could not recognise the expected Swift socket code in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("Swift.py", "ISSUE", f"Swift browser communication can hang indefinitely in {path}. Run again with --patch to add socket and mount timeouts.")

    patched = text
    if SWIFT_QUEUE_IMPORT_NEW not in patched:
        patched = patched.replace(SWIFT_QUEUE_IMPORT_OLD, SWIFT_QUEUE_IMPORT_NEW, 1)
    patched = patched.replace(SWIFT_SEND_SOCKET_OLD, SWIFT_SEND_SOCKET_NEW, 1)
    patched = patched.replace(SWIFT_SHAPE_MOUNT_OLD, SWIFT_SHAPE_MOUNT_NEW, 1)
    patched = patched.replace(SWIFT_ROBOT_MOUNT_OLD, SWIFT_ROBOT_MOUNT_NEW, 1)

    _backup_file(path)
    _write_text(path, patched)
    return DoctorResult("Swift.py", "PATCHED", f"Added Swift socket and mount timeouts in {path}.")


def _find_robot_plot_options_block(lines: list[str]) -> tuple[int, int] | None:
    start_index = None
    end_index = None

    for index, line in enumerate(lines):
        if line == ROBOT_PLOT_OPTIONS_START:
            start_index = index
            break

    if start_index is None:
        return None

    for index in range(start_index + 1, len(lines)):
        if lines[index] == ROBOT_PLOT_OPTIONS_END:
            end_index = index
            break

    if end_index is None:
        return None

    return start_index, end_index


def _replace_robot_plot_options_block(text: str) -> tuple[str, bool]:
    lines = text.splitlines()
    span = _find_robot_plot_options_block(lines)
    if span is None:
        return text, False

    start_index, end_index = span
    new_lines = lines[:start_index] + ROBOT_PLOT_FIXED_BLOCK + lines[end_index:]
    return "\n".join(new_lines) + "\n", True


def _robot_plot_block_status(text: str) -> tuple[bool, bool]:
    lines = text.splitlines()
    span = _find_robot_plot_options_block(lines)
    if span is None:
        return False, False

    start_index, end_index = span
    block = lines[start_index:end_index]
    stripped_statements = {line.strip() for line in block}
    block_has_tabs = any("\t" in line for line in block)
    block_is_fixed = all(
        statement in stripped_statements
        for statement in (
            "if options is not None:",
            "for key, value in options.items():",
            "if isinstance(defaults[key], dict) and isinstance(options[key], dict):",
            "defaults[key] = {**defaults[key], **options[key]}",
            "else:",
            "defaults[key] = options[key]",
        )
    )
    return block_is_fixed, block_has_tabs


def check_robot_plot(patch: bool = False) -> DoctorResult:
    path = _first_site_path(ROBOT_PLOT_RELATIVE)
    if path is None:
        return DoctorResult("RobotPlot.py", "SKIP", "Could not find roboticstoolbox/backends/PyPlot/RobotPlot.py in this Python environment.")

    text = _read_text(path)
    block_is_fixed, block_has_tabs = _robot_plot_block_status(text)
    if block_is_fixed and not block_has_tabs:
        return DoctorResult("RobotPlot.py", "OK", f"Scalar option fix is already present in {path}.")

    if block_is_fixed and block_has_tabs and not patch:
        return DoctorResult("RobotPlot.py", "WARN", f"Scalar option fix is present, but tabs were found in {path}. Run again with --patch to normalise the options block.")

    if ROBOT_PLOT_OLD_MERGE not in text and "isinstance(defaults[key], dict)" not in text:
        return DoctorResult("RobotPlot.py", "WARN", f"Could not recognise the PyPlot options merge block in {path}; leaving it unchanged.")

    if not patch:
        return DoctorResult("RobotPlot.py", "ISSUE", f"PyPlot scalar options may fail in {path}. Run again with --patch to update the options merge block.")

    new_text, replaced = _replace_robot_plot_options_block(text)
    if not replaced:
        return DoctorResult("RobotPlot.py", "FAILED", f"Could not replace the PyPlot options merge block in {path}.")

    _backup_file(path)
    _write_text(path, new_text)
    return DoctorResult("RobotPlot.py", "PATCHED", f"Updated PyPlot options merge block in {path}.")


def check_machinevision_sources(patch: bool = False) -> DoctorResult:
    path = _first_site_path(MACHINEVISION_SOURCES_RELATIVE)
    if path is None:
        return DoctorResult("MachineVision Sources.py", "SKIP", "Could not find machinevisiontoolbox/Sources.py in this Python environment.")

    text = _read_text(path)
    if MACHINEVISION_OLD_IMPORT not in text:
        return DoctorResult("MachineVision Sources.py", "OK", f"NumPy import issue is not present in {path}.")

    if not patch:
        return DoctorResult("MachineVision Sources.py", "ISSUE", f"Machine Vision Toolbox may fail with 'No module named numpy.char' in {path}. Run again with --patch to update the import.")

    _backup_file(path)
    _write_text(path, text.replace(MACHINEVISION_OLD_IMPORT, MACHINEVISION_NEW_IMPORT, 1))
    return DoctorResult("MachineVision Sources.py", "PATCHED", f"Updated NumPy import in {path}.")


COMMON_CHECKS_DESCRIPTION = "common Windows/lab setup fixes"
ADVANCED_SWIFT_CAPTURE_DESCRIPTION = "advanced Swift capture/headless fixes"


def run_checks(patch: bool = False, advanced_swift_capture: bool = False) -> list[DoctorResult]:
    common_results = [
        check_websockets(patch=patch),
        check_swift_route(patch=patch),
        check_swift_connect_timeout(patch=patch),
        check_swift_http_reset(patch=patch),
        check_swift_socket_timeouts(patch=patch),
        check_robot_plot(patch=patch),
        check_machinevision_sources(patch=patch),
    ]

    if not advanced_swift_capture:
        return common_results

    return common_results + [
        check_swift_json_serialisation(patch=patch),
        check_swift_canvas_buffer(patch=patch),
        check_swift_headless_close(patch=patch),
        check_swift_shape_update(patch=patch),
    ]


def _print_results(results: list[DoctorResult]) -> None:
    width = max(len(result.name) for result in results)
    for result in results:
        print(f"[{result.status:<7}] {result.name:<{width}}  {result.detail}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check and optionally patch known upstream Swift/PyPlot issues in the active Python environment.",
    )
    parser.add_argument(
        "--patch",
        action="store_true",
        help="Apply common Windows/lab setup patches to the active Python environment. Without this flag, only report issues.",
    )
    parser.add_argument(
        "--patch-advanced-swift-capture",
        action="store_true",
        help=(
            "Apply common patches plus additional Swift patches for browser screenshot, "
            "headless, and video-capture workflows."
        ),
    )
    args = parser.parse_args(argv)
    patch = args.patch or args.patch_advanced_swift_capture
    advanced_swift_capture = args.patch_advanced_swift_capture

    print("IR Support doctor")
    print(f"Python: {sys.executable}")
    if args.patch_advanced_swift_capture:
        mode = f"patch ({COMMON_CHECKS_DESCRIPTION} + {ADVANCED_SWIFT_CAPTURE_DESCRIPTION})"
    elif args.patch:
        mode = f"patch ({COMMON_CHECKS_DESCRIPTION})"
    else:
        mode = f"check only ({COMMON_CHECKS_DESCRIPTION})"
    print(f"Mode: {mode}")
    print()

    results = run_checks(patch=patch, advanced_swift_capture=advanced_swift_capture)
    _print_results(results)

    if not patch and any(result.status in {"ISSUE", "WARN"} for result in results):
        print()
        print("Run again with --patch to apply supported fixes, or use the manual instructions on the Canvas FAQ page.")
        print(
            "For Swift screenshot, headless browser, or video-capture workflows, "
            "run with --patch-advanced-swift-capture."
        )
    elif not advanced_swift_capture:
        print()
        print(
            "Advanced Swift capture checks were not run. Use --patch-advanced-swift-capture "
            "if you need Swift screenshot, headless browser, or video-capture support."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




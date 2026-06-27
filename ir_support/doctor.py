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


SWIFT_ROUTE_RELATIVE = Path("swift") / "SwiftRoute.py"
ROBOT_PLOT_RELATIVE = Path("roboticstoolbox") / "backends" / "PyPlot" / "RobotPlot.py"
MACHINEVISION_SOURCES_RELATIVE = Path("machinevisiontoolbox") / "Sources.py"

SWIFT_ROUTE_OLD = "self.path = urllib.parse.unquote(self.path[9:])"
SWIFT_ROUTE_NEW = "self.path = urllib.parse.unquote(self.path[10:])"

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


def run_checks(patch: bool = False) -> list[DoctorResult]:
    return [
        check_websockets(patch=patch),
        check_swift_route(patch=patch),
        check_robot_plot(patch=patch),
        check_machinevision_sources(patch=patch),
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
        help="Apply known safe patches to the active Python environment. Without this flag, only report issues.",
    )
    args = parser.parse_args(argv)

    print("IR Support doctor")
    print(f"Python: {sys.executable}")
    print(f"Mode: {'patch' if args.patch else 'check only'}")
    print()

    results = run_checks(patch=args.patch)
    _print_results(results)

    if not args.patch and any(result.status in {"ISSUE", "WARN"} for result in results):
        print()
        print("Run again with --patch to apply supported fixes, or use the manual instructions on the Canvas FAQ page.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())




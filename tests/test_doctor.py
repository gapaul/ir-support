import sys
import subprocess
import os
import shutil
import tempfile
import uuid
from pathlib import Path

import pytest
from ir_support import doctor


@pytest.fixture
def doctor_tmp_dir():
    base_dir = _writable_doctor_test_root()
    path = base_dir / f"case_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
        try:
            base_dir.rmdir()
        except OSError:
            pass


def _writable_doctor_test_root():
    candidates = []
    if os.environ.get("IR_SUPPORT_DOCTOR_TEST_TMP"):
        candidates.append(Path(os.environ["IR_SUPPORT_DOCTOR_TEST_TMP"]))
    candidates.extend(
        [
            Path("C:/robotics_41013_Python/tmp_ir_support_doctor_tests"),
            Path(tempfile.gettempdir()) / "ir_support_doctor_tests",
            Path(__file__).with_name("_doctor_tmp"),
        ]
    )

    for base_dir in candidates:
        try:
            probe = base_dir / f"probe_{uuid.uuid4().hex}" / "child"
            probe.mkdir(parents=True)
            shutil.rmtree(probe.parent, ignore_errors=True)
            return base_dir
        except OSError:
            continue

    raise RuntimeError("Could not create a writable scratch directory for doctor tests.")


def test_websockets_check_accepts_compatible_version(monkeypatch):
    monkeypatch.setattr(doctor.metadata, "version", lambda name: "13.1")

    result = doctor.check_websockets(patch=False)

    assert result.status == "OK"


def test_websockets_check_flags_newer_major_without_patch(monkeypatch):
    monkeypatch.setattr(doctor.metadata, "version", lambda name: "16.0")

    result = doctor.check_websockets(patch=False)

    assert result.status == "ISSUE"
    assert "websockets>=10.4,<14.0" in result.detail


def test_websockets_patch_installs_compatible_range(monkeypatch):
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(doctor.metadata, "version", lambda name: "16.0")
    monkeypatch.setattr(doctor.subprocess, "run", fake_run)

    result = doctor.check_websockets(patch=True)

    assert result.status == "PATCHED"
    assert commands == [[sys.executable, "-m", "pip", "install", "websockets>=10.4,<14.0"]]


def test_swift_route_patch_updates_old_windows_path_fix(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    route_path = swift_dir / "SwiftRoute.py"
    route_path.write_text(
        "self.path = urllib.parse.unquote(self.path[9:])\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_route(patch=True)

    assert result.status == "PATCHED"
    assert "self.path = urllib.parse.unquote(self.path[10:])" in route_path.read_text(encoding="utf-8")
    assert route_path.with_name("SwiftRoute.py.ir_support_backup").exists()


def test_robot_plot_patch_replaces_old_options_merge(doctor_tmp_dir, monkeypatch):
    plot_dir = doctor_tmp_dir / "roboticstoolbox" / "backends" / "PyPlot"
    plot_dir.mkdir(parents=True)
    plot_path = plot_dir / "RobotPlot.py"
    plot_path.write_text(
        "        if options is not None:\n"
        "            for key, value in options.items():\n"
        "                defaults[key] = {**defaults[key], **options[key]}\n"
        "        self.options = defaults\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_robot_plot(patch=True)

    text = plot_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "if isinstance(defaults[key], dict) and isinstance(options[key], dict):" in text
    assert "\t" not in text
    assert plot_path.with_name("RobotPlot.py.ir_support_backup").exists()


def test_robot_plot_patch_normalises_tabbed_manual_fix(doctor_tmp_dir, monkeypatch):
    plot_dir = doctor_tmp_dir / "roboticstoolbox" / "backends" / "PyPlot"
    plot_dir.mkdir(parents=True)
    plot_path = plot_dir / "RobotPlot.py"
    plot_path.write_text(
        "        if options is not None:\n"
        "            for key, value in options.items():\n"
        "                if isinstance(defaults[key], dict) and isinstance(options[key], dict):\n"
        "\t\t\t\t\tdefaults[key] = {**defaults[key], **options[key]}\n"
        "\t\t\t\telse:\n"
        "\t\t\t\t\tdefaults[key] = options[key]\n"
        "        self.options = defaults\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_robot_plot(patch=True)

    text = plot_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "\t" not in text
    assert "else:\n                    defaults[key] = options[key]" in text

def test_robot_plot_fixed_block_with_trailing_spaces_is_ok(doctor_tmp_dir, monkeypatch):
    plot_dir = doctor_tmp_dir / "roboticstoolbox" / "backends" / "PyPlot"
    plot_dir.mkdir(parents=True)
    plot_path = plot_dir / "RobotPlot.py"
    plot_path.write_text(
        "        if options is not None:\n"
        "            for key, value in options.items():\n"
        "                if isinstance(defaults[key], dict) and isinstance(options[key], dict):                \n"
        "                    defaults[key] = {**defaults[key], **options[key]}\n"
        "                else:\n"
        "                    defaults[key] = options[key]\n"
        "        self.options = defaults\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_robot_plot(patch=False)

    assert result.status == "OK"

def test_machinevision_sources_patch_replaces_numpy_char_import(doctor_tmp_dir, monkeypatch):
    sources_dir = doctor_tmp_dir / "machinevisiontoolbox"
    sources_dir.mkdir()
    sources_path = sources_dir / "Sources.py"
    sources_path.write_text(
        "from numpy.char import array\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_machinevision_sources(patch=True)

    assert result.status == "PATCHED"
    assert "from numpy import array" in sources_path.read_text(encoding="utf-8")
    assert sources_path.with_name("Sources.py.ir_support_backup").exists()


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


def test_run_checks_uses_common_checks_by_default(monkeypatch):
    called = []

    def fake_check(name):
        def _check(patch=False):
            called.append((name, patch))
            return doctor.DoctorResult(name, "OK", "ok")

        return _check

    checks = {
        "check_websockets": "websockets",
        "check_swift_route": "swift_route",
        "check_swift_connect_timeout": "swift_connect_timeout",
        "check_swift_http_reset": "swift_http_reset",
        "check_swift_socket_timeouts": "swift_socket_timeouts",
        "check_robot_plot": "robot_plot",
        "check_machinevision_sources": "machinevision",
        "check_swift_json_serialisation": "swift_json",
        "check_swift_canvas_buffer": "swift_canvas",
        "check_swift_headless_close": "swift_headless_close",
        "check_swift_shape_update": "swift_shape_update",
    }
    for function_name, check_name in checks.items():
        monkeypatch.setattr(doctor, function_name, fake_check(check_name))

    results = doctor.run_checks(patch=True)

    assert [result.name for result in results] == [
        "websockets",
        "swift_route",
        "swift_connect_timeout",
        "swift_http_reset",
        "swift_socket_timeouts",
        "robot_plot",
        "machinevision",
    ]
    assert all(patch is True for _, patch in called)
    assert "swift_json" not in {name for name, _ in called}
    assert "swift_canvas" not in {name for name, _ in called}


def test_run_checks_includes_advanced_swift_capture_checks_when_requested(monkeypatch):
    called = []

    def fake_check(name):
        def _check(patch=False):
            called.append((name, patch))
            return doctor.DoctorResult(name, "OK", "ok")

        return _check

    checks = {
        "check_websockets": "websockets",
        "check_swift_route": "swift_route",
        "check_swift_connect_timeout": "swift_connect_timeout",
        "check_swift_http_reset": "swift_http_reset",
        "check_swift_socket_timeouts": "swift_socket_timeouts",
        "check_robot_plot": "robot_plot",
        "check_machinevision_sources": "machinevision",
        "check_swift_json_serialisation": "swift_json",
        "check_swift_canvas_buffer": "swift_canvas",
        "check_swift_headless_close": "swift_headless_close",
        "check_swift_shape_update": "swift_shape_update",
    }
    for function_name, check_name in checks.items():
        monkeypatch.setattr(doctor, function_name, fake_check(check_name))

    results = doctor.run_checks(patch=True, advanced_swift_capture=True)

    assert [result.name for result in results] == [
        "websockets",
        "swift_route",
        "swift_connect_timeout",
        "swift_http_reset",
        "swift_socket_timeouts",
        "robot_plot",
        "machinevision",
        "swift_json",
        "swift_canvas",
        "swift_headless_close",
        "swift_shape_update",
    ]
    assert all(patch is True for _, patch in called)


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


def test_swift_connect_timeout_patch_makes_wait_configurable(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    route_path = swift_dir / "SwiftRoute.py"
    route_path.write_text(
        "try:\n"
        "            inq.get(timeout=10)\n"
        "except Empty:\n"
        "    raise\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_connect_timeout(patch=True)

    text = route_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert 'IR_SUPPORT_SWIFT_CONNECT_TIMEOUT' in text
    assert route_path.with_name("SwiftRoute.py.ir_support_backup").exists()


def test_swift_json_patch_handles_numpy_scalars(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    route_path = swift_dir / "SwiftRoute.py"
    route_path.write_text(
        doctor.SWIFT_ROUTE_JSON_DEFAULT_ANCHOR
        + "channel.send(json.dumps(msg))\n"
        + "await websocket.send(json.dumps(msg))\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_json_serialisation(patch=True)

    text = route_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "def _ir_support_json_default" in text
    assert "json.dumps(msg, default=_ir_support_json_default)" in text
    assert "json.dumps(msg))" not in text
    assert route_path.with_name("SwiftRoute.py.ir_support_backup").exists()


def test_swift_http_reset_patch_suppresses_shutdown_noise(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    route_path = swift_dir / "SwiftRoute.py"
    route_path.write_text(doctor.SWIFT_HTTP_HANDLER_OLD, encoding="utf-8")
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_http_reset(patch=True)

    text = route_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "def handle(self):" in text
    assert "except ConnectionResetError:" in text
    assert route_path.with_name("SwiftRoute.py.ir_support_backup").exists()


def test_swift_canvas_patch_preserves_webgl_buffer(doctor_tmp_dir, monkeypatch):
    chunk_dir = doctor_tmp_dir / "swift" / "out" / "_next" / "static" / "chunks" / "pages"
    chunk_dir.mkdir(parents=True)
    chunk_path = chunk_dir / "index-test.js"
    chunk_path.write_text(
        'M.createElement(uV,{gl:{antialias:!0},id:"threeCanvas"})',
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_canvas_buffer(patch=True)

    text = chunk_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "gl:{antialias:!0,preserveDrawingBuffer:!0}" in text
    assert chunk_path.with_name("index-test.js.ir_support_backup").exists()


def test_swift_headless_close_patch_guards_missing_server(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    swift_path = swift_dir / "Swift.py"
    swift_path.write_text(doctor.SWIFT_STOP_THREADS_OLD, encoding="utf-8")
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_headless_close(patch=True)

    text = swift_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert 'hasattr(self, "socket")' in text
    assert 'hasattr(self, "server")' in text
    assert swift_path.with_name("Swift.py.ir_support_backup").exists()


def test_swift_socket_timeout_patch_updates_current_swift_layout(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    swift_path = swift_dir / "Swift.py"
    swift_path.write_text(
        doctor.SWIFT_QUEUE_IMPORT_OLD
        + "\n\n"
        + doctor.SWIFT_SEND_SOCKET_OLD
        + "\n"
        + doctor.SWIFT_SHAPE_MOUNT_OLD
        + "\n"
        + doctor.SWIFT_ROBOT_MOUNT_OLD,
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_socket_timeouts(patch=True)

    text = swift_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "from queue import Queue, Empty" in text
    assert "Timed out waiting for Swift browser response" in text
    assert "mount_deadline = time.time()" in text
    assert swift_path.with_name("Swift.py.ir_support_backup").exists()


def test_swift_shape_update_patch_disables_unsupported_send(doctor_tmp_dir, monkeypatch):
    swift_dir = doctor_tmp_dir / "swift"
    swift_dir.mkdir()
    swift_path = swift_dir / "Swift.py"
    swift_path.write_text(doctor.SWIFT_SHAPE_UPDATE_OLD, encoding="utf-8")
    chunk_dir = doctor_tmp_dir / "swift" / "out" / "_next" / "static" / "chunks" / "pages"
    chunk_dir.mkdir(parents=True)
    (chunk_dir / "index-test.js").write_text("shape_mounted:function(e){}", encoding="utf-8")
    monkeypatch.setattr(sys, "path", [str(doctor_tmp_dir), *sys.path])

    result = doctor.check_swift_shape_update(patch=True)

    text = swift_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "shape_update handler" in text
    assert 'self._send_socket("shape_update"' not in text
    assert swift_path.with_name("Swift.py.ir_support_backup").exists()


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


import sys
from pathlib import Path

from ir_support import doctor


def test_swift_route_patch_updates_old_windows_path_fix(tmp_path, monkeypatch):
    swift_dir = tmp_path / "swift"
    swift_dir.mkdir()
    route_path = swift_dir / "SwiftRoute.py"
    route_path.write_text(
        "self.path = urllib.parse.unquote(self.path[9:])\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(tmp_path), *sys.path])

    result = doctor.check_swift_route(patch=True)

    assert result.status == "PATCHED"
    assert "self.path = urllib.parse.unquote(self.path[10:])" in route_path.read_text(encoding="utf-8")
    assert route_path.with_name("SwiftRoute.py.ir_support_backup").exists()


def test_robot_plot_patch_replaces_old_options_merge(tmp_path, monkeypatch):
    plot_dir = tmp_path / "roboticstoolbox" / "backends" / "PyPlot"
    plot_dir.mkdir(parents=True)
    plot_path = plot_dir / "RobotPlot.py"
    plot_path.write_text(
        "        if options is not None:\n"
        "            for key, value in options.items():\n"
        "                defaults[key] = {**defaults[key], **options[key]}\n"
        "        self.options = defaults\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(tmp_path), *sys.path])

    result = doctor.check_robot_plot(patch=True)

    text = plot_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "if isinstance(defaults[key], dict) and isinstance(options[key], dict):" in text
    assert "\t" not in text
    assert plot_path.with_name("RobotPlot.py.ir_support_backup").exists()


def test_robot_plot_patch_normalises_tabbed_manual_fix(tmp_path, monkeypatch):
    plot_dir = tmp_path / "roboticstoolbox" / "backends" / "PyPlot"
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
    monkeypatch.setattr(sys, "path", [str(tmp_path), *sys.path])

    result = doctor.check_robot_plot(patch=True)

    text = plot_path.read_text(encoding="utf-8")
    assert result.status == "PATCHED"
    assert "\t" not in text
    assert "else:\n                    defaults[key] = options[key]" in text

def test_robot_plot_fixed_block_with_trailing_spaces_is_ok(tmp_path, monkeypatch):
    plot_dir = tmp_path / "roboticstoolbox" / "backends" / "PyPlot"
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
    monkeypatch.setattr(sys, "path", [str(tmp_path), *sys.path])

    result = doctor.check_robot_plot(patch=False)

    assert result.status == "OK"

def test_machinevision_sources_patch_replaces_numpy_char_import(tmp_path, monkeypatch):
    sources_dir = tmp_path / "machinevisiontoolbox"
    sources_dir.mkdir()
    sources_path = sources_dir / "Sources.py"
    sources_path.write_text(
        "from numpy.char import array\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "path", [str(tmp_path), *sys.path])

    result = doctor.check_machinevision_sources(patch=True)

    assert result.status == "PATCHED"
    assert "from numpy import array" in sources_path.read_text(encoding="utf-8")
    assert sources_path.with_name("Sources.py.ir_support_backup").exists()


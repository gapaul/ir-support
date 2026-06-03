from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Iterable, Sequence


Rgba = tuple[float, float, float, float]


def rgba_text(rgba: Rgba) -> str:
    return " ".join(f"{component:.6g}" for component in rgba)


def scaled_rgb_text(rgba: Rgba, scale: float, minimum: float = 0.0) -> str:
    red, green, blue, alpha = rgba
    scaled = (
        max(red * scale, minimum),
        max(green * scale, minimum),
        max(blue * scale, minimum),
        alpha,
    )
    return rgba_text(scaled)


def _replace_shader_colour(text: str, tag: str, value: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"(<{tag}\b[^>]*>\s*<color\b[^>]*>)([^<]*)(</color>\s*</{tag}>)",
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.subn(rf"\g<1>{value}\g<3>", text)


def _replace_shininess(text: str, value: str = "20") -> str:
    pattern = re.compile(
        r"(<shininess\b[^>]*>\s*<float\b[^>]*>)([^<]*)(</float>\s*</shininess>)",
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub(rf"\g<1>{value}\g<3>", text)


def _effect_library(diffuse: Rgba) -> str:
    ambient = scaled_rgb_text(diffuse, 0.45, minimum=0.015)
    return f"""
  <library_effects>
    <effect id="ir_support_material_effect" name="ir_support_material_effect">
      <profile_COMMON>
        <technique sid="common">
          <phong>
            <emission><color>0 0 0 1</color></emission>
            <ambient><color>{ambient}</color></ambient>
            <diffuse><color>{rgba_text(diffuse)}</color></diffuse>
            <specular><color>0.12 0.12 0.12 1</color></specular>
            <shininess><float>20</float></shininess>
          </phong>
        </technique>
      </profile_COMMON>
    </effect>
  </library_effects>
  <library_materials>
    <material id="ir_support_material" name="ir_support_material">
      <instance_effect url="#ir_support_material_effect"/>
    </material>
  </library_materials>
"""


def ensure_single_material(path: Path, diffuse: Rgba) -> None:
    """Set or add a simple Collada material without touching mesh coordinates."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    updated = text

    if "<library_effects" not in updated:
        updated = updated.replace("</asset>", "</asset>" + _effect_library(diffuse), 1)

    diffuse_text = rgba_text(diffuse)
    ambient_text = scaled_rgb_text(diffuse, 0.45, minimum=0.015)
    updated, diffuse_count = _replace_shader_colour(updated, "diffuse", diffuse_text)
    updated, _ = _replace_shader_colour(updated, "ambient", ambient_text)
    updated, _ = _replace_shader_colour(updated, "specular", "0.12 0.12 0.12 1")
    updated = _replace_shininess(updated)

    if diffuse_count == 0:
        updated = updated.replace("</asset>", "</asset>" + _effect_library(diffuse), 1)

    if 'material="ir_support_material"' not in updated and "ir_support_material" in updated:
        updated = re.sub(
            r"<triangles\b(?![^>]*\bmaterial=)",
            '<triangles material="ir_support_material"',
            updated,
            count=1,
        )
        updated = re.sub(
            r'(<instance_geometry\b[^>]*)\s*/>',
            r"""\1>
          <bind_material>
            <technique_common>
              <instance_material symbol="ir_support_material" target="#ir_support_material"/>
            </technique_common>
          </bind_material>
        </instance_geometry>""",
            updated,
            count=1,
        )

    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")


def copy_link_dae_set(
    source_dir: Path,
    source_names: Sequence[str],
    dest_dir: Path,
    dest_stem: str,
    colours: Sequence[Rgba] | None = None,
) -> list[Path]:
    """Copy a numbered link DAE set and optionally set one material per link."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for index, source_name in enumerate(source_names):
        source = source_dir / source_name
        dest = dest_dir / f"{dest_stem}Link{index}.dae"
        shutil.copy2(source, dest)
        if colours is not None:
            ensure_single_material(dest, colours[index])
        output_paths.append(dest)
    return output_paths


def rename_link_dae_stem(
    robot_dir: Path,
    old_stem: str,
    new_stem: str,
    count: int,
    colours: Sequence[Rgba] | None = None,
) -> list[Path]:
    """Rename existing link DAEs to a new stem and optionally recolour them."""
    output_paths: list[Path] = []
    for index in range(count):
        old_path = robot_dir / f"{old_stem}Link{index}.dae"
        new_path = robot_dir / f"{new_stem}Link{index}.dae"
        if not old_path.exists() and new_path.exists():
            path = new_path
        else:
            old_path.rename(new_path)
            path = new_path
        if colours is not None:
            ensure_single_material(path, colours[index])
        output_paths.append(path)
    return output_paths


def remove_link_dae_set(robot_dir: Path, stem: str, count: int) -> None:
    for index in range(count):
        path = robot_dir / f"{stem}Link{index}.dae"
        if path.exists():
            path.unlink()


def replace_mesh_stem(class_file: Path, old_stem: str, new_stem: str) -> None:
    text = class_file.read_text(encoding="utf-8")
    updated = text.replace(f'f"{old_stem}Link{{i}}"', f'f"{new_stem}Link{{i}}"')
    if updated != text:
        class_file.write_text(updated, encoding="utf-8", newline="\n")


def dae_total_size(paths: Iterable[Path]) -> float:
    return sum(path.stat().st_size for path in paths) / (1024 * 1024)

"""Helpers for preparing robot visual assets for Swift.

Mesh porting checklist:
- Prefer DAE assets with double-sided materials so thin or open robot panels do
  not disappear when viewed from the back side.
- Check each mesh bounding box after conversion. If a robot link is hundreds or
  thousands of units across, it is probably still in millimetres while the DH
  model is in metres. If it is tiny, it may have been scaled twice.
- Compare the total visual mesh envelope with the DH reach and with typical
  industrial robot dimensions. Small cobots are usually below about 1.5 m
  reach; medium industrial arms are a few metres; anything wildly outside that
  range needs scale or frame investigation before being accepted.
- Decide whether meshes are link-local or global-at-home before changing DH
  parameters. Use meshes_are_global_at_home=True for assets that were exported
  already assembled in the home pose.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable, Iterable, Sequence


Rgba = tuple[float, float, float, float]


@dataclass(frozen=True)
class DaeComponent:
    """Summary of a disconnected triangle component in a Collada mesh."""

    index: int
    face_count: int
    vertex_count: int
    minimum: tuple[float, float, float]
    maximum: tuple[float, float, float]
    extent: tuple[float, float, float]


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


def _double_sided_extra() -> str:
    return """
      <extra>
        <technique profile="GOOGLEEARTH">
          <double_sided>1</double_sided>
        </technique>
      </extra>"""


def _ensure_double_sided_text(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        effect = match.group(0)
        if "double_sided" in effect.lower():
            return effect
        return effect.replace("</effect>", _double_sided_extra() + "\n    </effect>")

    return re.sub(
        r"<effect\b[^>]*>.*?</effect>",
        replace,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )


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
        <extra>
          <technique profile="GOOGLEEARTH">
            <double_sided>1</double_sided>
          </technique>
        </extra>
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

    updated = _ensure_double_sided_text(updated)

    diffuse_text = rgba_text(diffuse)
    ambient_text = scaled_rgb_text(diffuse, 0.45, minimum=0.015)
    updated, diffuse_count = _replace_shader_colour(updated, "diffuse", diffuse_text)
    updated, _ = _replace_shader_colour(updated, "ambient", ambient_text)
    updated, _ = _replace_shader_colour(updated, "specular", "0.12 0.12 0.12 1")
    updated = _replace_shininess(updated)

    if diffuse_count == 0:
        updated = updated.replace("</asset>", "</asset>" + _effect_library(diffuse), 1)
        updated = _ensure_double_sided_text(updated)

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


def rotation_matrix(axis: str, angle_radians: float) -> tuple[tuple[float, float, float], ...]:
    """Return a 3x3 rotation matrix for simple mesh-coordinate repairs."""
    c = math.cos(angle_radians)
    s = math.sin(angle_radians)
    axis = axis.lower()
    if axis == "x":
        return ((1.0, 0.0, 0.0), (0.0, c, -s), (0.0, s, c))
    if axis == "y":
        return ((c, 0.0, s), (0.0, 1.0, 0.0), (-s, 0.0, c))
    if axis == "z":
        return ((c, -s, 0.0), (s, c, 0.0), (0.0, 0.0, 1.0))
    raise ValueError("axis must be 'x', 'y', or 'z'")


def transform_dae_positions(
    path: Path,
    *,
    scale: float | Sequence[float] = 1.0,
    rotation: tuple[tuple[float, float, float], ...] | None = None,
    translation: Sequence[float] = (0.0, 0.0, 0.0),
) -> None:
    """Apply a simple coordinate transform to position arrays in a Collada file."""
    text = path.read_text(encoding="utf-8", errors="ignore")

    if isinstance(scale, (int, float)):
        sx = sy = sz = float(scale)
    else:
        sx, sy, sz = (float(value) for value in scale)
    tx, ty, tz = (float(value) for value in translation)
    matrix = rotation or ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))

    def replace(match: re.Match[str]) -> str:
        open_tag, values, close_tag = match.groups()
        tag_lower = open_tag.lower()
        if "position" not in tag_lower:
            return match.group(0)

        numbers = [float(value) for value in values.split()]
        if len(numbers) % 3 != 0:
            return match.group(0)

        output: list[str] = []
        for index in range(0, len(numbers), 3):
            x = numbers[index] * sx
            y = numbers[index + 1] * sy
            z = numbers[index + 2] * sz
            rx = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + tx
            ry = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + ty
            rz = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + tz
            output.extend((f"{rx:.9g}", f"{ry:.9g}", f"{rz:.9g}"))

        return open_tag + " ".join(output) + close_tag

    updated = re.sub(
        r"(<float_array\b[^>]*>)([^<]*)(</float_array>)",
        replace,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")


def remove_dae_components_where(
    path: Path,
    predicate: Callable[[DaeComponent], bool],
) -> list[DaeComponent]:
    """Remove disconnected triangle components selected by a bounding-box predicate."""
    namespace = "http://www.collada.org/2005/11/COLLADASchema"
    ET.register_namespace("", namespace)
    ns = {"c": namespace}

    tree = ET.parse(path)
    root = tree.getroot()
    removed: list[DaeComponent] = []

    for mesh in root.findall(".//c:mesh", ns):
        float_array = None
        for candidate in mesh.findall(".//c:float_array", ns):
            if "position" in (candidate.get("id") or "").lower():
                float_array = candidate
                break
        if float_array is None:
            continue

        numbers = [float(value) for value in (float_array.text or "").split()]
        if len(numbers) % 3 != 0:
            continue
        positions = [
            (numbers[index], numbers[index + 1], numbers[index + 2])
            for index in range(0, len(numbers), 3)
        ]

        face_vertices: list[tuple[int, int, int]] = []
        triangle_groups = []
        for triangles in mesh.findall("c:triangles", ns):
            inputs = triangles.findall("c:input", ns)
            vertex_inputs = [item for item in inputs if item.get("semantic") == "VERTEX"]
            if not vertex_inputs:
                continue

            stride = max(int(item.get("offset", "0")) for item in inputs) + 1
            vertex_offset = int(vertex_inputs[0].get("offset", "0"))
            values = [int(value) for value in (triangles.find("c:p", ns).text or "").split()]
            count = int(triangles.get("count", "0"))
            chunks = [
                values[index * 3 * stride : (index + 1) * 3 * stride]
                for index in range(count)
            ]

            global_indices: list[int] = []
            for chunk in chunks:
                vertices = tuple(chunk[axis * stride + vertex_offset] for axis in range(3))
                global_indices.append(len(face_vertices))
                face_vertices.append(vertices)

            triangle_groups.append((triangles, chunks, global_indices))

        vertex_to_faces: dict[int, list[int]] = defaultdict(list)
        for face_index, vertices in enumerate(face_vertices):
            for vertex in vertices:
                vertex_to_faces[vertex].append(face_index)

        seen = [False] * len(face_vertices)
        face_to_component: dict[int, DaeComponent] = {}
        for start in range(len(face_vertices)):
            if seen[start]:
                continue

            stack = [start]
            seen[start] = True
            component_faces: list[int] = []
            component_vertices: set[int] = set()
            while stack:
                face_index = stack.pop()
                component_faces.append(face_index)
                for vertex in face_vertices[face_index]:
                    component_vertices.add(vertex)
                    for neighbour in vertex_to_faces[vertex]:
                        if not seen[neighbour]:
                            seen[neighbour] = True
                            stack.append(neighbour)

            xs, ys, zs = zip(*(positions[vertex] for vertex in component_vertices))
            minimum = (min(xs), min(ys), min(zs))
            maximum = (max(xs), max(ys), max(zs))
            component = DaeComponent(
                index=len(removed) + len({summary for summary in face_to_component.values()}),
                face_count=len(component_faces),
                vertex_count=len(component_vertices),
                minimum=minimum,
                maximum=maximum,
                extent=tuple(maximum[axis] - minimum[axis] for axis in range(3)),
            )
            for face_index in component_faces:
                face_to_component[face_index] = component

        components = []
        for component in face_to_component.values():
            if component not in components:
                components.append(component)
        components.sort(key=lambda item: item.face_count, reverse=True)
        component_indices = {id(component): index for index, component in enumerate(components)}
        normalized_components = {
            component: DaeComponent(
                index=component_indices[id(component)],
                face_count=component.face_count,
                vertex_count=component.vertex_count,
                minimum=component.minimum,
                maximum=component.maximum,
                extent=component.extent,
            )
            for component in components
        }

        remove_faces: set[int] = set()
        for face_index, component in face_to_component.items():
            normalized = normalized_components[component]
            if predicate(normalized):
                remove_faces.add(face_index)
        removed.extend(
            component
            for component in normalized_components.values()
            if predicate(component)
        )

        if not remove_faces:
            continue

        for triangles, chunks, global_indices in triangle_groups:
            kept_chunks = [
                chunk
                for chunk, face_index in zip(chunks, global_indices)
                if face_index not in remove_faces
            ]
            if kept_chunks:
                triangles.set("count", str(len(kept_chunks)))
                triangles.find("c:p", ns).text = " ".join(
                    str(value) for chunk in kept_chunks for value in chunk
                )
            else:
                mesh.remove(triangles)

    if removed:
        tree.write(path, encoding="utf-8", xml_declaration=True)

    return removed


def write_cylinder_dae(
    path: Path,
    *,
    radius: float,
    length: float,
    colour: Rgba,
    axis: str = "z",
    segments: int = 32,
) -> None:
    """Write a small Collada cylinder for replacing student end-effectors."""
    axis = axis.lower()
    if axis not in {"x", "y", "z"}:
        raise ValueError("axis must be 'x', 'y', or 'z'")

    def point(a: float, b: float, c: float) -> tuple[float, float, float]:
        if axis == "x":
            return (c, a, b)
        if axis == "y":
            return (a, c, b)
        return (a, b, c)

    half = length / 2.0
    vertices: list[tuple[float, float, float]] = []
    for z in (-half, half):
        for i in range(segments):
            theta = 2.0 * math.pi * i / segments
            vertices.append(point(radius * math.cos(theta), radius * math.sin(theta), z))

    bottom_center = len(vertices)
    vertices.append(point(0.0, 0.0, -half))
    top_center = len(vertices)
    vertices.append(point(0.0, 0.0, half))

    faces: list[tuple[int, int, int]] = []
    for i in range(segments):
        j = (i + 1) % segments
        faces.append((i, j, segments + j))
        faces.append((i, segments + j, segments + i))
        faces.append((bottom_center, j, i))
        faces.append((top_center, segments + i, segments + j))

    position_text = " ".join(f"{coord:.9g}" for vertex in vertices for coord in vertex)
    index_text = " ".join(str(index) for face in faces for index in face)
    path.write_text(
        f'''<?xml version="1.0" encoding="utf-8"?>
<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
  <asset>
    <unit name="meter" meter="1"/>
    <up_axis>Z_UP</up_axis>
  </asset>
  {_effect_library(colour)}
  <library_geometries>
    <geometry id="mesh" name="mesh">
      <mesh>
        <source id="mesh-positions">
          <float_array id="mesh-positions-array" count="{len(vertices) * 3}">{position_text}</float_array>
          <technique_common>
            <accessor source="#mesh-positions-array" count="{len(vertices)}" stride="3">
              <param name="X" type="float"/>
              <param name="Y" type="float"/>
              <param name="Z" type="float"/>
            </accessor>
          </technique_common>
        </source>
        <vertices id="mesh-vertices">
          <input semantic="POSITION" source="#mesh-positions"/>
        </vertices>
        <triangles material="ir_support_material" count="{len(faces)}">
          <input semantic="VERTEX" source="#mesh-vertices" offset="0"/>
          <p>{index_text}</p>
        </triangles>
      </mesh>
    </geometry>
  </library_geometries>
  <library_visual_scenes>
    <visual_scene id="Scene" name="Scene">
      <node id="Cylinder" name="Cylinder">
        <instance_geometry url="#mesh">
          <bind_material>
            <technique_common>
              <instance_material symbol="ir_support_material" target="#ir_support_material"/>
            </technique_common>
          </bind_material>
        </instance_geometry>
      </node>
    </visual_scene>
  </library_visual_scenes>
  <scene>
    <instance_visual_scene url="#Scene"/>
  </scene>
</COLLADA>
''',
        encoding="utf-8",
        newline="\n",
    )

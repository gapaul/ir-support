import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_PARTS_ROOT = REPO_ROOT / "ir_support_extra_parts"
for path in (REPO_ROOT, EXTRA_PARTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_parts.parts import part_mesh, part_names, part_path  # noqa: E402


STUDENT_PARTS = [
    "TrafficCone",
    "BeerBottle",
    "SpiritBottle",
    "SafetyRailing",
    "LegoMan",
    "SafetyPerson",
    "StencilPlate",
    "Toolbox",
    "GreenBin",
    "RedBin",
    "Tray",
    "WateringCan",
    "FireBlanket",
    "BarcodeScanner",
    "FoodTrayBlue",
    "JuiceBoxOrange",
    "Lunchbox",
    "Monitor",
    "SafetyLight",
    "WallShelf",
]


def test_student_candidate_parts_are_packaged():
    available = set(part_names())
    missing = sorted(name for name in STUDENT_PARTS if name not in available)
    assert not missing


def test_student_candidate_parts_load_as_meshes():
    for name in STUDENT_PARTS:
        path = part_path(name)
        assert path.exists()
        mesh = part_mesh(name)
        assert getattr(mesh, "filename", None)

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRA_PARTS_ROOT = REPO_ROOT / "ir_support_extra_parts"
for path in (REPO_ROOT, EXTRA_PARTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ir_support_extra_parts.parts import PART_CATEGORIES, part_names  # noqa: E402


def test_all_extra_parts_are_categorised_once():
    available = set(part_names())
    categorised = [
        part for category_parts in PART_CATEGORIES.values() for part in category_parts
    ]

    assert sorted(categorised) == sorted(set(categorised))
    assert set(categorised) == available


def test_extra_part_categories_are_not_empty():
    for category, category_parts in PART_CATEGORIES.items():
        assert category
        assert category_parts

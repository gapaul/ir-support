import numpy as np

from tests.view_part_model_swift import (
    build_part_motion_pose,
    estimate_part_bounds,
    option_index_for,
    part_categories_for,
    part_detail_lines,
    part_options,
    resolve_part_name,
)
from ir_support_extra_parts.parts import part_reference_url


PART_NAME = "Apple"


def test_named_part_model_resolves_and_has_category_details():
    resolved = resolve_part_name(PART_NAME)
    options = part_options()
    selected = options[option_index_for(PART_NAME)]
    bounds = estimate_part_bounds(PART_NAME)
    detail_lines = part_detail_lines(PART_NAME, bounds)

    assert resolved == PART_NAME
    assert selected.name == PART_NAME
    assert part_categories_for(PART_NAME)
    assert any(line.startswith("Part: Apple") for line in detail_lines)
    assert any(line.startswith("Category:") for line in detail_lines)
    assert any(line.startswith("Bounds:") for line in detail_lines)


def test_part_motion_pose_is_finite_and_moves_up():
    bounds = estimate_part_bounds(PART_NAME)
    ground_pose = build_part_motion_pose(bounds, 0.0).A
    lifted_pose = build_part_motion_pose(bounds, 0.5).A

    assert ground_pose.shape == (4, 4)
    assert lifted_pose.shape == (4, 4)
    assert np.isfinite(ground_pose).all()
    assert np.isfinite(lifted_pose).all()
    assert lifted_pose[2, 3] > ground_pose[2, 3]


def test_part_reference_url_defaults_to_none_when_not_known():
    assert part_reference_url(PART_NAME) is None

##  @file
#   @brief Find the intersection between a line segment and a plane.
#   @author Gavin Paul
#   @date May 29, 2026

import numpy as np
from typing import Union, List, Tuple

def line_plane_intersection(plane_normal:Union[np.ndarray, List[float]],
                            point_on_plane:Union[np.ndarray, List[float]],
                            point1_on_line:Union[np.ndarray, List[float]],
                            point2_on_line:Union[np.ndarray, List[float]],)->Tuple[np.ndarray, int]:
    """
    Given a plane (normal and point) and two points that make up another line, get the intersection
    - Check == 0 if there is no intersection
    - Check == 1 if there is a line plane intersection between the two points
    - Check == 2 if the segment lies in the plane (always intersecting)
    - Check == 3 if there is intersection point which lies outside line segment

    Parameters
    ----------
    plane_normal : np.ndarray
        Normal vector of the plane
    point_on_plane : np.ndarray
        Point on the plane
    point1_on_line : np.ndarray
        First point on the line
    point2_on_line : np.ndarray
        Second point on the line
    """

    plane_normal = np.asarray(plane_normal, dtype=float)
    point_on_plane = np.asarray(point_on_plane, dtype=float)
    point1_on_line = np.asarray(point1_on_line, dtype=float)
    point2_on_line = np.asarray(point2_on_line, dtype=float)

    intersection_point = np.zeros(3)
    line_vector = point2_on_line - point1_on_line
    plane_to_line = point1_on_line - point_on_plane
    denominator = np.dot(plane_normal, line_vector)
    numerator = -np.dot(plane_normal, plane_to_line)
    check = 0

    if np.abs(denominator) < 1e-7:                      # The segment is parallel to plane
        if np.isclose(numerator, 0):                    # The segment lies in plane
            check = 2
            return intersection_point, check
        else:
            return intersection_point, check            # No intersection

    # Compute the intersection parameter
    segment_fraction = numerator / denominator
    intersection_point = point1_on_line + segment_fraction * line_vector

    if segment_fraction < 0 or segment_fraction > 1:
        check = 3                                       # The intersection point lies outside the segment, so there is no intersection
    else:
        check = 1

    return intersection_point, check

def test_public_function_imports():
    from ir_support import (  # noqa: F401
        clean_SE2,
        draw_possible_ellipse_given_foci,
        line_plane_intersection,
        make_ellipsoid,
        orthogonalize_rotation,
        tranimate_custom,
    )


def test_public_class_imports():
    from ir_support import (  # noqa: F401
        CylindricalDHRobotPlot,
        EllipsoidRobot,
        RectangularPrism,
    )


def test_public_ply_imports():
    from ir_support import (  # noqa: F401
        RobotCow,
        SwiftParrotQuadrotor,
        SwiftUFOFleet,
        UFOFLeet,
        place_fence,
        place_object,
        transform_vertices,
    )


def test_public_robot_imports():
    from ir_support.robots import (  # noqa: F401
        DensoVS060,
        LinearUR3,
        LinearUR5,
        UR3,
        UR5,
        schunk_UTS_v2_0,
    )

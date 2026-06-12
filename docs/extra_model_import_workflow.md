# Importing Extra Robot and Part Models

This note records the repeatable process for moving useful student-created models into the optional IR Support model packages. It is intended for maintainers who need to review a new assignment cohort without keeping the temporary batch scripts that were used during the first large import.

## Package Targets

Use the packages consistently:

- `ir_support`: core package for code and lab-required models.
- `ir_support_extra_robots`: optional robot models that are useful but not required for lab exercises.
- `ir_support_extra_parts`: optional parts, props, fixtures, safety items, and workcell objects.
- `ir_support_full`: meta-package that installs the core package and both extra model packages.

Avoid adding one-off assignment review scripts to the package permanently. Keep reusable inspection tools in `tests/` and put repeatable mesh-processing utilities in `tools/`.

## Source Audit

Search only the explicitly named assignment folders. Do not search upward from a OneDrive or network parent folder because that can accidentally hydrate cloud-only files or traverse thousands of unrelated files.

For robots, shortlist only models that are likely to be real commercial, educational, or open-source robot arms. Reject custom student-invented arms unless there is a strong reason to keep them. Also reject duplicates that are already available in Peter Corke's Robotics Toolbox, core `ir_support`, or `ir_support_extra_robots`, unless the new mesh is clearly better.

For parts, search common mesh types such as `.dae`, `.ply`, `.stl`, `.obj`, and `.blend`, but reject robot link meshes, whole environments, scene layouts, and objects that are too specific to one assignment. Prefer useful industrial robotics objects: workcell fixtures, safety equipment, controls and sensors, packaging, and manipulable objects.

Record accepted and rejected models in the relevant `MODEL_PROVENANCE.md` file so future maintainers do not re-check the same poor candidates.

## Candidate Checks

For each candidate, check:

- The name identifies the actual make and model where possible.
- The model is unique compared with the existing core and extra packages.
- Meshes have useful geometry and are not only simple placeholder cylinders or boxes.
- Meshes have sensible colours or materials, or can be recoloured without too much hand work.
- Dimensions are plausible in metres.
- The total DAE size is reasonable: aim for less than about 15 MB for a robot and less than about 4 MB for a single part.
- The object or robot sits on the ground plane in the expected orientation.
- Triangles render from both sides where the model would otherwise appear hollow.

If a mesh is invisible, extremely large, or tiny in Swift, inspect its vertex bounding box. Many student meshes are in millimetres and need a `0.001` scale conversion.

## Robot Model Checks

Before accepting a robot:

1. Confirm the robot appears to be a real model from a manufacturer or recognised open-source project.
2. Check the expected number of joints and broad reach against manufacturer information or a trusted model.
3. Compare DH parameters with similar robots already in the library.
4. Load the model in Swift and animate all joints, not only the first three.
5. Check the base pose, link order, joint axes, wrist links, and end-effector mounting face.
6. Remove non-standard grippers, suction cups, linear rails, or assignment tools unless they are part of the standard robot.
7. Add an explicit warning in the model docstring and provenance if a robot is useful but has a known visual limitation.

Use the general viewer for a single robot:

```bash
python tests/view_robot_model_swift.py --package extra --robot DensoVP6242
python tests/view_robot_model_swift.py --package core --robot UR3e
```

The viewer can be run with no arguments and then used through the Swift side-panel dropdown, or started with --package and --robot to choose an initial model. It cache-busts DAE files, animates every joint, prints basic diagnostics, and adds camera buttons for isometric, front, side, top, and wrist views.

## Part Model Checks

Before accepting a part:

1. Check the object is generally useful for industrial robotics teaching or assignments.
2. Check the bounding box is plausible in metres.
3. Put the object on the ground plane in its normal resting orientation.
4. Recolour plain white objects with simple, believable materials.
5. Put labels on the actual surface of the object, not floating nearby.
6. For labelled boxes and bottles, check the text is not mirrored or upside down from the main viewing directions.
7. Use double-sided geometry where thin signs, labels, cartons, or people appear hollow from one side.
8. Add the accepted object to `parts/categories.py` so it appears in the category viewer.

Use the category viewer for review:

```bash
python tests/view_extra_parts_by_category_swift.py --category "Safety Objects"
python tests/view_extra_parts_by_category_swift.py --category "Controls And Sensors"
```

## Blender and Mesh Processing

The most common Blender cleanup tasks are:

- Convert `.ply` or `.stl` files to `.dae` when Swift needs a Collada mesh.
- Scale millimetre models to metres.
- Apply transforms before export so the mesh origin and local axes are meaningful.
- Move each robot link mesh close to its own local joint frame.
- Remove assignment-specific grippers, rails, fixtures, or floating labels.
- Decimate large meshes until the visual quality is acceptable and the file size is reasonable.
- Recalculate normals and add double-sided faces where Swift shows see-through triangles.
- Use simple material colours rather than high-frequency noisy vertex colours.

STL files usually do not contain colour. If an STL import looks plain grey or white, recolour it manually or use manufacturer/reference images for guidance.

## Swift Review Notes

Swift and the browser can cache DAE assets. When reviewing edited meshes, use viewers that copy the meshes to a temporary cache-bust folder before adding them to Swift. This makes file names unique for each run and avoids old geometry appearing after a mesh has been fixed.

For efficient review, add camera buttons beside the viewer. A useful minimum set is isometric, front, side, top, and wrist or close-up. Move robots through repeated joint-space trajectories so disconnected links, wrong joint axes, and bad mesh origins become obvious.

## Provenance and Documentation

For every accepted model:

- Add the source and review notes to `MODEL_PROVENANCE.md`.
- Add the model to the package `__init__.py` or category registry.
- Update the relevant package README when the public list or category counts change.
- Update the Canvas simulated models page when the student-facing catalogue changes.

For every rejected model that took meaningful review time, add a short rejected note so it is not revisited later.

## Validation Before Commit

Run the relevant tests from the repository root:

```bash
python -m pytest tests/test_extra_robots.py tests/test_extra_parts.py tests/test_extra_part_categories.py tests/test_named_robot_model.py
```

Then visually inspect any newly imported models with the Swift viewers. Keep the final commit focused on accepted package assets, provenance, documentation, reusable tools, and tests. Do not commit temporary batch review scripts or screenshots.


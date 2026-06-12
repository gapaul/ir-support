# IR Support tests

This folder contains the automated test suite for `ir-support`.

The tests focus on public behaviour used in 41013 lab solutions, exercises,
quizzes, and Python Wiki examples. They should be safe to run before committing
changes and in GitHub Actions before merging a pull request or publishing to
PyPI.

Run locally from the repository root with:

```bash
python -m pytest
```

If `pytest` is not installed in your environment, install the development
dependencies first:

```bash
python -m pip install -r requirements-dev.txt
```

## Visual model review helpers

The long-running student import batches are not kept as permanent test files.
Use the reusable viewers instead. From a terminal, make sure python is the same virtual environment selected in VS Code, or activate the project environment first:

```bash
python tests/view_robot_model_swift.py
python tests/view_robot_model_swift.py --package extra --robot DensoVP6242
python tests/view_robot_model_swift.py --package core --robot UR3e
python tests/view_part_model_swift.py
python tests/view_part_model_swift.py --part Camera
python tests/view_extra_robots_swift.py
python tests/view_extra_parts_by_category_swift.py --category "Safety Objects"
python tests/view_extra_parts_swift.py
```

`view_robot_model_swift.py` is intended for detailed single-robot inspection.
Run it with no arguments to open UR3e, then use the Swift side-panel dropdown to
choose any core or extra robot and click `Load selected robot`. It copies meshes
to a temporary cache-bust folder, animates every joint, and adds camera buttons
for common views. The package-wide viewers are useful when checking that the
installed catalogues still load together.

`view_part_model_swift.py` is intended for detailed single-part inspection. Run
it with no arguments to open a default part, then use the Swift side-panel
dropdown to choose any packaged extra part and click `Load selected part`. It
uses the same cache-busting approach, bobs and spins the selected mesh, and adds
camera buttons plus compact part details. The category and package-wide part
viewers are still useful when checking multiple objects together.

The model import process is documented in `docs/extra_model_import_workflow.md`.

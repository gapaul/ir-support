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

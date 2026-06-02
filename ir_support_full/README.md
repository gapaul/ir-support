# ir-support-full

`ir-support-full` is a small meta-package for 41013 Industrial Robotics at UTS. It installs the core `ir-support` package plus the optional robot and parts model packs:

- `ir-support`
- `ir-support-extra-robots`
- `ir-support-extra-parts`

Use this when you want the complete local model library rather than only the lab-required core package.

```powershell
python -m pip install ir-support-full
```

The installed importable packages remain `ir_support`, `ir_support_extra_robots`, and `ir_support_extra_parts`.

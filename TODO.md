# Future Work

- Decide whether `rvc3python` should be an explicit `ir-support` dependency, or a documented optional install target, so a fresh student environment can install IR Support without separately remembering the Robotics Toolbox stack. This should be handled together with the planned dependency/Python-version modernisation work.
- Review `Files/Labs/bagreader.py`: it imports `bagpy`, but `bagpy==0.5` pins `Jinja2<3.1` and conflicts with the current Flask/Open3D stack. Keep it out of the standard student install unless we replace or isolate that bag-reading workflow.

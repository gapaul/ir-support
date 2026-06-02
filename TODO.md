# Future Work

- Review dependency pins and supported Python versions together, with a target of moving beyond Python 3.10 once the Robotics Toolbox/Open3D/Swift stack is verified.
- Review `Files/Labs/bagreader.py`: it imports `bagpy`, but `bagpy==0.5` pins `Jinja2<3.1` and conflicts with the current Flask/Open3D stack. Keep it out of the standard student install unless we replace or isolate that bag-reading workflow.

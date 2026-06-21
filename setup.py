# Kept for tools that still inspect setup.py metadata.
# For package metadata and release builds, prefer pyproject.toml/Poetry.
from setuptools import setup, find_packages

setup(
    name="ir_support",
    version="1.4.0",
    description="Python package including some classes & functions supporting the subject 41013 Industrial Robotics at UTS, along with the Robotics Toolbox for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10,<3.13",
    packages=find_packages(include=["ir_support", "ir_support.*"]),
    install_requires=[
        "rvc3python>=0.9.2,<0.10.0",
        "numpy>=1.26.4,<2.0.0",
        "pandas>=2.2.3,<3.0.0",
        "trimesh>=4.4.3,<5.0.0",
        "plyfile>=1.1.0,<2.0.0",
        "keyboard>=0.13.5",
        "scikit-image>=0.25.2,<0.26.0",
        "more-itertools>=10.5.0,<11.0.0",
        "open3d>=0.19.0,<0.20.0",
        "spatialmath-python>=1.1.16,<1.2.0",
        "matplotlib>=3.10.0,<3.11.0",
        "pygame>=2.6.1,<3.0.0",
        "line_profiler>=5.0.0,<6.0.0",
    ],
    url="https://github.com/gapaul/ir-support",
    author="Quang Ngo",
    author_email="quang.ngohominh@gmail.com",
)

from setuptools import setup, find_packages     # type: ignore
#   no type problems in .toml...

setup(
    name="mazegen",             # Package name
    version="1.0.0",            # Current package version
    author="kimendon, sukerl",
    packages=find_packages(),
         # Purpose: tells setuptools which Python modules and packages to
         # include in your distribution: find_packages() automatically scans
         # your project directory and finds all folders containing __init__.py.
    python_requires=">=3.10",   # Package works with version 3.10 or higher
)

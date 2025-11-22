from setuptools import setup, find_packages
import os
import re


setup(
    name='tfl',
    version='v0.1',
    description="A layer ontop of the TFL Unified API",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="GL/JW/MH",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # e.g. "numpy>=1.22"
    ],
    include_package_data=True,
)

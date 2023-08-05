#!/usr/bin/env python3
""" setup.py """

import pathlib
from setuptools import setup

# The directory containing the readme file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="OptivolutionPy",
    version="1.0.0",
    description="A flexible genetic algorithm library written in Python3.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Mhmd-Hisham/OptivolutionPy",
    author="Mohamed Hisham",
    author_email="Mohamed00Hisham@Gmail.com",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=["optivolution"]
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" setup instructions for OptivolutionPy """

import codecs
import os
import sys

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    README = '\n' + fh.read()

setup(
    name="OptivolutionPy",
    version="1.0.1",
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
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=["optivolution"]
)

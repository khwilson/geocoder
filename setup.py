#!/usr/bin/env python
import os
from setuptools import find_packages, setup
import warnings


def parse_requirements(filename):
    """ Parse a requirements file ignoring comments and -r inclusions of other files """
    reqs = []
    with open(filename, 'r') as f:
        for line in f:
            hash_idx = line.find('#')
            if hash_idx >= 0:
                line = line[:hash_idx]
            line = line.strip()
            if line:
                reqs.append(line)
    return reqs


with open(os.path.join('geocoder', 'VERSION'), 'r') as f:
    version = f.read().strip()


with open('README.md', 'r') as f:
    readme = f.read().strip()


setup(
    name="geocoder",
    version=version,
    url="https://github.com/khwilson/geocoder",
    author="Kevin Wilson",
    author_email="khwilson@gmail.com",
    license="Apache v2.0",
    packages=find_packages(),
    package_data={'geocoder': ['VERSION']},
    install_requires=parse_requirements('requirements.in'),
    tests_require=parse_requirements('requirements.testing.in'),
    description="A little app to pull geocodes from Google's API",
    entry_points="""
    [console_scripts]
    geocoder=geocoder.cli:cli
    """,
    long_description="\n" + readme
)

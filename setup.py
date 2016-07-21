#!/usr/bin/env python
from setuptools import find_packages, setup


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


setup(
    name="geocoder",
    version='0.1',
    url="https://github.com/khwilson/geocoder",
    author="Kevin Wilson",
    author_email="khwilson@gmail.com",
    license="Apache v2.0",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.in'),
    tests_require=parse_requirements('requirements.testing.in'),
    description="A little app to pull geocodes from Google's API",
    long_description="\n" + open('README.md', 'r').read()
)

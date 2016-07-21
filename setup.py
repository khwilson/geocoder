#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name="geocoder",
    version='0.1',
    url="https://github.com/khwilson/geocoder",
    author="Kevin Wilson",
    author_email="khwilson@gmail.com",
    license="Apache v2.0",
    packages=find_packages(),
    description="A little app to pull geocodes from Google's API",
    long_description="\n" + open('README.md').read()
)

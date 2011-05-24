#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = (0, 8)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name='magma',
    version='0.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages = find_packages(
        where = '.',
        exclude='docs',
    ),
)


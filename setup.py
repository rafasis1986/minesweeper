#!/usr/bin/env python
from setuptools import find_packages, setup


PROJECT_NAME = "minesweeper_api"
VERSION = "0.1"

setup(
    name=PROJECT_NAME,
    version=VERSION,
    description="An minesweeper api",
    author="Rafael Torres",
    author_email="rdtr.sis@gmail.com",
    url="https://github.com/rafasis1986/minesweeper-API",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    package_data={PROJECT_NAME: ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'])

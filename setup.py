#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    6/15/18
"""
from os import path
from setuptools import find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "LICENSE"), encoding="utf-8") as f:
    full_license = f.read()

with open(path.join(here, "src/metapype/VERSION.txt"), encoding="utf-8") as f:
    version = f.read()


setup(
    name='metapype',
    version=version,
    description='Metapype: science metadata manipulation library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Environmental Data Initiative",
    url="https://github.com/PASTAplus/metapype-eml",
    license=full_license,
    packages=find_packages(where="src", include=["metapype", "metapype.eml", "metapype.model"]),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=" == 3.8.*",
    install_requires=["click==8.0.3", "daiquiri==3.0.0",  "lxml==4.7.1", "rfc3986==1.5.0"],
    classifiers=["License :: OSI Approved :: Apache Software License",],
)


def main():
    return 0


if __name__ == "__main__":
    main()

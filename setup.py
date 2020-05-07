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

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'LICENSE'), encoding='utf-8') as f:
    full_license = f.read()


setup(
    name='metapype',
    version='2020.05.07',
    description='Metapype for EML', long_description=long_description,
    long_description_content_type="text/markdown",
    author='EDI',
    url='https://github.com/PASTAplus/metapype-eml',
    license=full_license,
    packages=find_packages(where="src"),
    include_package_data=True,
    exclude_package_data={"": ["settings.py, properties.py, config.py"],},
    package_dir={"": "src"},
    python_requires=">3.8.*",
    entry_points={"console_scripts": ["rendere=rendere.render:main"]},
    classifiers=['License :: OSI Approved :: Apache Software License', ],
    # install_requires=SEE environment.yml or requirements.txt
)


def main():
    return 0


if __name__ == "__main__":
    main()

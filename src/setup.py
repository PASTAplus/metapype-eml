#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla

:Created:
    6/15/18
"""
import setuptools

setuptools.setup(name='metapype',
                 version='2019.2.15',
                 description='Metapype for EML',
                 author='EDI',
                 url='https://github.com/PASTAplus/metapype-eml',
                 license='Apache License, Version 2.0',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 exclude_package_data={
                     '': ['settings.py, properties.py, config.py'],
                 }, )


def main():
    return 0


if __name__ == "__main__":
    main()

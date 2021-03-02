#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: __init__

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    1/16/19
"""
import importlib.resources


version = importlib.resources.read_text("metapype", "VERSION.txt")
__version__ = version.strip()

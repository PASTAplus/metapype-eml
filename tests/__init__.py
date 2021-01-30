#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: __init__

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    5/7/20
"""
import logging
import os
import sys

import daiquiri


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/tests.log"
daiquiri.setup(level=logging.DEBUG,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)


sys.path.insert(0, os.path.abspath("../src"))

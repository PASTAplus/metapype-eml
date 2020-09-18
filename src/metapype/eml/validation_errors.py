#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: evaluate.py

:Synopsis:

:Author:
    ide

:Created:
    6/23/20
"""
from enum import Enum, auto


class ValidationError(Enum):
    ATTRIBUTE_EXPECTED_ENUM = auto()
    ATTRIBUTE_REQUIRED = auto()
    ATTRIBUTE_UNRECOGNIZED = auto()
    CHILD_NOT_ALLOWED = auto()
    CONTENT_EXPECTED_EMPTY = auto()
    CONTENT_EXPECTED_ENUM = auto()
    CONTENT_EXPECTED_FLOAT = auto()
    CONTENT_EXPECTED_NONEMPTY = auto()
    CONTENT_EXPECTED_RANGE = auto()
    CONTENT_EXPECTED_STRING = auto()
    CONTENT_EXPECTED_TIME_FORMAT = auto()
    CONTENT_EXPECTED_YEAR_FORMAT = auto()
    MAX_OCCURRENCE_EXCEEDED = auto()
    MIN_OCCURRENCE_UNMET = auto()
    UNKNOWN_ATTRIBUTE = auto()
    UNKNOWN_NODE = auto()
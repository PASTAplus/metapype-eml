#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: exceptions

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    6/5/18
"""
import daiquiri


logger = daiquiri.getLogger("exceptions: " + __name__)


class MetapypeRuleError(Exception):
    pass


class AttributeExpectedEnumError(MetapypeRuleError):
    pass


class AttributeRequiredError(MetapypeRuleError):
    pass


class AttributeUnrecognizedError(MetapypeRuleError):
    pass


class ChildNotAllowedError(MetapypeRuleError):
    pass


class ContentExpectedEmptyError(MetapypeRuleError):
    pass


class ContentExpectedEnumError(MetapypeRuleError):
    pass


class ContentExpectedFloatError(MetapypeRuleError):
    pass


class ContentExpectedNonemptyError(MetapypeRuleError):
    pass


class ContentExpectedRangeError(MetapypeRuleError):
    pass


class ContentExpectedStringError(MetapypeRuleError):
    pass


class ContentExpectedTimeFormatError(MetapypeRuleError):
    pass


class ContentExpectedDateFormatError(MetapypeRuleError):
    pass


class ContentExpectedYearFormatError(MetapypeRuleError):
    pass


class ContentExpectedUriError(MetapypeRuleError):
    pass


class MaxOccurrenceExceededError(MetapypeRuleError):
    pass


class MinOccurrenceUnmetError(MetapypeRuleError):
    pass


class StrContentUnicodeError(MetapypeRuleError):
    pass


class UnknownAttributeError(MetapypeRuleError):
    pass


class UnknownContentRuleError(MetapypeRuleError):
    pass


class UnknownNodeError(MetapypeRuleError):
    pass

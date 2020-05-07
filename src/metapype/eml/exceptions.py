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


logger = daiquiri.getLogger('exceptions: ' + __name__)


class MetapypeRuleError(Exception):
    pass


def main():
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: views

:Synopsis:

:Author:
    servilla

:Created:
    6/4/18
"""
import daiquiri

logger = daiquiri.getLogger('views: ' + __name__)


def graph(node, level):
    indent = '  ' * level
    type = node.rank
    if node.content is not None:
        type += ': {}'.format(node.content)
    if len(node.attributes) > 0:
        type += ' ' + str(node.attributes)
    if level == 0:
        print(type)
    else:
        print(indent + '\u2570\u2500 ' + type)
    for child in node.children:
       graph(child, level + 1)


def main():
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: validate

:Synopsis:

:Author:
    servilla

:Created:
    6/5/18
"""
import daiquiri

from metapype.eml2_1_1.exceptions import MetapypeRuleError
from metapype.eml2_1_1.rules import rules
from metapype.model.node import Node


logger = daiquiri.getLogger('validate: ' + __name__)


def node(node: Node):
    if node.name not in rules:
        msg = 'Unknown node rank: {}'.format(node.name)
        raise MetapypeRuleError(msg)
    else:
        rules[node.name](node)


def tree(root: Node):
    try:
        node(root)
    except MetapypeRuleError as e:
        logger.error(e)
    for child in root.children:
        tree(child)


def main():
    return 0


if __name__ == "__main__":
    main()

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

from metapype.eml2_1_1.exceptions import MPLRuleError
from metapype.eml2_1_1.rules import rules
from metapype.model.node import Node


logger = daiquiri.getLogger('validate: ' + __name__)


def node(node: Node):
    if node.rank not in rules:
        msg = 'Unknown node rank: {}'.format(node.rank)
        raise MPLRuleError(msg)
    else:
        rules[node.rank](node)


def tree(root: Node):
    try:
        node(root)
    except MPLRuleError as e:
        logger.error(e)
    for child in root.children:
        tree(child)


def main():
    return 0


if __name__ == "__main__":
    main()

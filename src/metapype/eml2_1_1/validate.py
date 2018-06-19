#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: validate

:Synopsis:
    Node instance validation processing, including node sub-tree.

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


def node(node: Node) -> None:
    '''
    Evaluates a given node for rule compliance.

    Args:
        node: Node instance to be evaluated

    Returns:
        None

    Raises:
        MetapypeRuleError: An unknown type of node for EML 2.1.1
    '''
    if node.name not in rules:
        msg = 'Unknown node: {}'.format(node.name)
        raise MetapypeRuleError(msg)
    else:
        rules[node.name](node)


def tree(root: Node) -> None:
    '''
    Recursively walks from the root node and evaluates
    each child node for rule compliance.

    Args:
        root: Node instance of root for evaluation

    Returns:
        None
    '''
    node(root)
    for child in root.children:
        tree(child)


def main():
    return 0


if __name__ == "__main__":
    main()

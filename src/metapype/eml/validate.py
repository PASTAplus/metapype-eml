#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: validate

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    7/10/18
"""
import daiquiri

from metapype.eml.exceptions import MetapypeRuleError
from metapype.eml import rule
from metapype.model.node import Node


logger = daiquiri.getLogger('validate: ' + __name__)


def node(node: Node) -> None:
    '''
    Validates a given node for rule compliance.

    Args:
        node: Node instance to be validated

    Returns:
        None

    Raises:
        MetapypeRuleError: An unknown type of node for EML 2.1.1
    '''
    if node.name not in rule.node_mappings:
        msg = 'Unknown node: {}'.format(node.name)
        raise MetapypeRuleError(msg)
    else:
        node_rule = rule.get_rule(node.name)
        node_rule.validate_rule(node)


def tree(root: Node) -> None:
    '''
    Recursively walks from the root node and validates
    each child node for rule compliance.

    Args:
        root: Node instance of root for validates

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

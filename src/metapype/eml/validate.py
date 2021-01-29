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

from metapype.eml import rule
from metapype.eml.exceptions import MetapypeRuleError
from metapype.eml.validation_errors import ValidationError
from metapype.model.node import Node


logger = daiquiri.getLogger("validate: " + __name__)


def node(node: Node, errs: list = None) -> None:
    """
    Validates a given node for rule compliance.

    Args:
        node: Node instance to be validated
        errs: List container for validation errors (fail fast if None)

    Returns:
        None

    Raises:
        MetapypeRuleError: An unknown type of node for EML
    """
    if node.name not in rule.node_mappings:
        msg = f"Unknown node rule type: {node.name}"
        if errs is None:
            raise MetapypeRuleError(msg)
        else:
            errs.append((ValidationError.UNKNOWN_NODE, msg, node))
    else:
        node_rule = rule.get_rule(node.name)
        node_rule.validate_rule(node, errs)


def tree(root: Node, errs: list = None) -> None:
    """
    Recursively walks from the root node and validates
    each child node for rule compliance.

    Args:
        root: Node instance of root for validates

    Returns:
        None
    """
    # print(root.name)
    node(root, errs)
    for child in root.children:
        tree(child, errs)

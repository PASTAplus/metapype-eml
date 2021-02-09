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
from metapype.eml.exceptions import MetapypeRuleError, UnknownNodeError
from metapype.eml.validation_errors import ValidationError
from metapype.model.node import Node


logger = daiquiri.getLogger("validate: " + __name__)


def node(n: Node, errs: list = None) -> None:
    """
    Validates a given node for rule compliance.

    Args:
        n: Node instance to be validated
        errs: List container for validation errors (fail fast if None)

    Returns:
        None

    Raises:
        MetapypeRuleError: An unknown type of node for EML
    """
    if n.name not in rule.node_mappings:
        msg = f"Unknown node rule type: {n.name}"
        if errs is None:
            raise UnknownNodeError(msg)
        else:
            errs.append((ValidationError.UNKNOWN_NODE, msg, n))
    else:
        node_rule = rule.get_rule(n.name)
        node_rule.validate_rule(n, errs)


def prune(n: Node) -> list:
    """
    Prune in place all non-valid nodes from the tree

    Args:
        n: Node

    Returns: List of pruned nodes

    Side-effects: Non-valid nodes are pruned from the tree

    """
    pruned = list()
    if n.name != "metadata":
        try:
            node(n)
        except MetapypeRuleError:
            for child in n.children:
                try:
                    node(child)
                except UnknownNodeError:
                    pruned.append(child)
            for child in pruned:
                n.remove_child(child)
                Node.delete_node_instance(child.id)
        for child in n.children:
            pruned += prune(child)
    return pruned


def tree(n: Node, errs: list = None) -> None:
    """
    Recursively walks from the root node and validates
    each child node for rule compliance.

    Args:
        n: Node instance of root for validates
        errs: List container for validation errors (fail fast if None)

    Returns:
        None
    """
    node(n, errs)
    if n.name != "metadata":
        for child in n.children:
            tree(child, errs)

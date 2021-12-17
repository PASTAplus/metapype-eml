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
from metapype.eml.exceptions import MetapypeRuleError, UnknownNodeError, ChildNotAllowedError
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


def prune(n: Node, strict: bool = False) -> list:
    """
    Prune in place all non-valid nodes from the tree

    Args:
        n: Node
        strict:

    Returns: List of pruned nodes

    Side-effects: Non-valid nodes are pruned from the tree

    """
    pruned = list()
    if n.name != "metadata":
        try:
            node(n)
        except UnknownNodeError as ex:
            logger.debug(f"Pruning: {n.name}")
            pruned.append((n, str(ex)))
            if n.parent is not None:
                n.parent.remove_child(n)
            Node.delete_node_instance(n.id)
            return pruned
        except ChildNotAllowedError as ex:
            r = rule.get_rule(n.name)
            children = n.children.copy()
            for child in children:
                if not r.is_allowed_child(child.name):
                    logger.debug(f"Pruning: {child.name}")
                    pruned.append((child, str(ex)))
                    n.remove_child(child)
                    Node.delete_node_instance(child.id)
        except MetapypeRuleError as ex:
            logger.info(ex)
        children = n.children.copy()
        for child in children:
            pruned += prune(child, strict)
            if strict and child not in pruned:
                try:
                    node(child)
                except MetapypeRuleError as ex:
                    logger.debug(f"Pruning: {child.name}")
                    pruned.append((child, str(ex)))
                    n.remove_child(child)
                    Node.delete_node_instance(child.id)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: evaluate

:Synopsis:

:Author:
    servilla

:Created:
    6/21/18
"""
import daiquiri

from metapype.eml2_1_1.exceptions import MetapypeRuleError
from metapype.eml2_1_1 import names
from metapype.model.node import Node

logger = daiquiri.getLogger('evaluate: ' + __name__)

PASS = 'PASS'


# ==================== Begin of rules section ====================


def _individual_name_rule(node: Node) -> str:
    givename = False
    surname = False
    for child in node.children:
        if child.name == names.GIVENNAME: givename = True
        if child.name == names.SURNAME: surname = True
    if givename and surname:
        evaluation = PASS
    else:
        _ = 'Should have both a "{0}" and "{1}"'
        evaluation = _.format(names.GIVENNAME, names.SURNAME)
    return evaluation


def _title_rule(node: Node) -> str:
    evaluation = PASS
    title = node.content
    if title is not None:
        length = len(title.split(' '))
        if length < 20:
            _ = ('"{0}" is too short, should '
                 'have at least 10 words')
            evaluation = _.format(title)
    return evaluation


# ===================== End of rules section =====================


def node(node: Node):
    '''
    Evaluates a given node for rule compliance.

    Args:
        node: Node instance to be evaluated

    Returns:
        None or evaluation dict
    '''
    evaluation = None
    if node.name in rules:
        evaluation = '({0}) {1}'.format(node.name, rules[node.name](node))
    return evaluation


def tree(root: Node, e: dict):
    '''
    Recursively walks from the root node and evaluates
    each child node for rule compliance.

    Args:
        root: Node instance of root for evaluation

    Returns:
        None
    '''
    evaluation = node(root)
    if evaluation is not None:
        e[root.id] = evaluation
    for child in root.children:
        tree(child, e)


# Rule function pointers
rules = {
    names.INDIVIDUALNAME: _individual_name_rule,
    names.TITLE: _title_rule,
}

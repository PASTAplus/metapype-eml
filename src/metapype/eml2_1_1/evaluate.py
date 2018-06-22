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
from  metapype.eml2_1_1 import names
from metapype.model.node import Node


logger = daiquiri.getLogger('evaluate: ' + __name__)

PASS = 'PASS'

def title_rule(node: Node) -> str:
    evaluation = PASS
    title = node.content
    if title is not None:
        length = len(title.split(' '))
        if length < 10:
            evaluation = 'Length of title "{0}" too short'.format(title)
    return evaluation


def individual_name_rule(node: Node) -> str:
    givename = False
    surname = False
    for child in node.children:
        if child.name == names.GIVENNAME: givename = True
        if child.name == names.SURNAME: surname = True
    if givename and surname:
        evaluation = PASS
    else:
        evaluation = 'Should have both "{0}" and "{1}"'.format(names.GIVENNAME, names.SURNAME)
    return evaluation


#===================== End of rules section =====================


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
        evaluation = {}
        _ = '{0}: {1}'.format(node.name, rules[node.name](node))
        evaluation[node.node_id] = _
    return evaluation


def tree(root: Node, e: list):
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
        e.append(evaluation)
    for child in root.children:
        tree(child, e)




# Rule function pointers
rules = {
    names.INDIVIDUALNAME: individual_name_rule,
    names.TITLE: title_rule,
}
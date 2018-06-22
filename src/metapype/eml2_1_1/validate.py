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
from metapype.eml2_1_1 import names
from metapype.model.node import Node


logger = daiquiri.getLogger('validate: ' + __name__)

REQUIRED = True
OPTIONAL = False
INFINITY = None


def access_rule(node: Node):
    if 'order' in node.attributes:
        allowed = ['allowFirst', 'denyFirst']
        if node.attributes['order'] not in allowed:
            msg = '"{0}:order" attribute must be one of "{1}"'.format(node.name,
                                                                      allowed)
            raise MetapypeRuleError(msg)
    attributes = {
        'id': OPTIONAL,
        'system': OPTIONAL,
        'scope': OPTIONAL,
        'order': OPTIONAL,
        'authSystem': REQUIRED
    }
    process_attributes(attributes, node)
    children = [
        ['allow', 'deny', 1, INFINITY]
    ]
    process_children(children, node)


def additional_metadata_rule(node: Node):
    attributes = {
        'id': OPTIONAL
    }
    process_attributes(attributes, node)
    children = [
        ['describes', 0, INFINITY],
        ['metadata', 1, 1]
    ]
    process_children(children, node)


def allow_rule(node: Node):
    children = [
        ['principal', 1, INFINITY],
        ['permission', 1, INFINITY]
    ]
    process_children(children, node)


def any_name_rule(node: Node):
    '''
    Generic rule for names.

    This is a generic rule for evaluating name-based metadata like
    surName, givenName, or salutations.

    Args:
        node: Node instance being evaluated

    Returns:
        None

    Raises:
        MetapypeRuleError: If content is not string or if without child and
        content is empty
    '''
    if node.content is not None and type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(
            node.name, type(node.content))
        raise MetapypeRuleError(msg)
    if len(node.children) == 0 and node.content is None:
        msg = 'Node "{0}" content should not be empty'.format(node.name)
        raise MetapypeRuleError(msg)
    attributes = {
        'lang': OPTIONAL
    }
    process_attributes(attributes, node)
    children = [
        ['value', 0, INFINITY]
    ]
    process_children(children, node)


def dataset_rule(node: Node):
    pass


def deny_rule(node: Node):
    children = [
        ['principal', 1, INFINITY],
        ['permission', 1, INFINITY]
    ]
    process_children(children, node)


def eml_rule(node: Node):
    attributes = {
        'packageId': REQUIRED,
        'system': REQUIRED,
        'scope': OPTIONAL,
        'lang': OPTIONAL
    }
    process_attributes(attributes, node)
    children = [
        ['access', 0, 1],
        ['dataset', 'citation', 'software', 'protocol', 1, 1],
        ['additionalMetadata', 0, INFINITY]
    ]
    process_children(children, node)


def individual_name_rule(node: Node):
    children = [
        ['salutation', 0, INFINITY],
        ['givenName', 0, INFINITY],
        ['surName', 1, 1]
    ]
    process_children(children, node)


def metadata_rule(node: Node):
    if len(node.children) != 0:
        msg = 'Node "{0}" should not have children'.format(node.name)
        raise MetapypeRuleError(msg)
    if type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(
            node.name, type(node.content))
        raise MetapypeRuleError(msg)


def permission_rule(node: Node):
    if len(node.children) != 0:
        msg = 'Node "{0}" should not have children'.format(node.name)
        raise MetapypeRuleError(msg)
    allowed = ['read', 'write', 'changePermission', 'all']
    if node.content not in allowed:
        msg = 'Node "{0}" content should be one of "{1}", not "{2}"'.format(
            node.name, allowed, node.content)
        raise MetapypeRuleError(msg)


def principal_rule(node: Node):
    if len(node.children) != 0:
        msg = 'Node "{0}" should not have children'.format(node.name)
        raise MetapypeRuleError(msg)
    if type(node.content) is not str:
        msg = 'Node content should be type string, not "{0}"'.format(
            type(node.content))
        raise MetapypeRuleError(msg)


def responsible_party_rule(node: Node) -> None:
    '''
    Generic rule for any responsibleParty type of metadata like creator or
    contact.

    Args:
        node: Node instance being evaluated

    Returns:
        None
    '''
    attributes = {
        'id': OPTIONAL,
        'system': OPTIONAL,
        'scope': OPTIONAL
    }
    process_attributes(attributes, node)
    children = [
        ['individualName', 'organizationName', 'positionName', 1, INFINITY],
        ['address', 0, INFINITY],
        ['phone', 0, INFINITY],
        ['electronicMailAddress', 0, INFINITY],
        ['onlineUrl', 0, INFINITY],
        ['userId', 0, INFINITY]
    ]
    process_children(children, node)


def title_rule(node: Node):
    if node.content is not None and type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(
            node.name, type(node.content))
        raise MetapypeRuleError(msg)
    attributes = {
        'lang': OPTIONAL
    }
    process_attributes(attributes, node)
    children = [
        ['value', 0, INFINITY]
    ]
    process_children(children, node)


def value_rule(node: Node):
    if node.content is None:
        msg = 'Node "{0}" content cannot be empty'.format(node.name)
        raise MetapypeRuleError(msg)
    if type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(
            node.name, type(node.content))
        raise MetapypeRuleError(msg)
    attributes = {
        'xml:lang': REQUIRED,
    }
    process_attributes(attributes, node)


#===================== End of rules section =====================


def process_attributes(attributes: dict, node: Node) -> None:
    '''
    Validates node attributes for rule compliance.

    Iterates through the dict of attribute rules and validates whether
    the node instance complies with the rule.

    Args:
        attributes: dict of rule attributes
        node: Node instance to be validates

    Returns:
        None

    Raises:
        MetapypeRuleError: Illegal attribute or missing required attribute
    '''
    for attribute in attributes:
        required = attributes[attribute]
        if required and attribute not in node.attributes:
            msg = '"{0}" is a required attribute of node "{1}"'.format(
                attribute, node.name)
            raise MetapypeRuleError(msg)
    for attribute in node.attributes:
        if attribute not in attributes:
            msg = '"{0}" is not a recognized attributes of node "{1}"'.format(
                attribute, node.name)
            raise MetapypeRuleError(msg)


def process_children(children: list, node: Node) -> None:
    '''
    Validates node children for rule compliance.

    Iterates through the list children rules and validates whether
    the node instance complies with the rules.

    Args:
        children: list of lists containing children
        node: Node instance to be validated

    Returns:
        None

    Raises:
        MetapypeRuleError: Illegal child, bad sequence or choice, missing
        child, or wrong child cardinality
    '''
    i = 0
    max_i = len(node.children)
    for child in children:
        name = child[:-2]
        min = child[-2]
        max = child[-1]
        cnt = 0
        while i < max_i:
            child_name = node.children[i].name
            if child_name in name:
                cnt += 1
                if max is not INFINITY and cnt > max:
                    msg = 'Maximum occurrence of "{0}" exceeded for "{1}"'.format(
                        name, node.name)
                    raise MetapypeRuleError(msg)
                i += 1
            else:
                break
        if cnt < min:
            msg = 'Minimum occurrence of "{0}" not met for "{1}"'.format(name,
                                                                         node.name)
            raise MetapypeRuleError(msg)
    if i < max_i:
        child_name = node.children[i].name
        msg = 'Child "{0}" not allowed  for "{1}"'.format(child_name, node.name)
        raise MetapypeRuleError(msg)


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
    if node.name not in rules:
        msg = 'Unknown node: {}'.format(node.name)
        raise MetapypeRuleError(msg)
    else:
        rules[node.name](node)


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


# Rule function pointers
rules = {
    names.ACCESS: access_rule,
    names.ADDITIONALMETADATA: additional_metadata_rule,
    names.ALLOW: allow_rule,
    names.CONTACT: responsible_party_rule,
    names.CREATOR: responsible_party_rule,
    names.DATASET: dataset_rule,
    names.DENY: deny_rule,
    names.EML: eml_rule,
    names.GIVENNAME: any_name_rule,
    names.INDIVIDUALNAME: individual_name_rule,
    names.METADATA: metadata_rule,
    names.ORGANIZATIONNAME: any_name_rule,
    names.PERMISSION: permission_rule,
    names.POSITIONNAME: any_name_rule,
    names.PRINCIPAL: principal_rule,
    names.SALUTATION: any_name_rule,
    names.SURNAME: any_name_rule,
    names.TITLE: title_rule,
    names.VALUE: value_rule,
}
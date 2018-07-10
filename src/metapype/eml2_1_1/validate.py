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

TYPE_NONE = None
TYPE_STR = 'str'
TYPE_INT = 'int'
TYPE_FLOAT = 'float'
TYPE_DATETIME = 'datetime'

PERMISSIONS = ('read', 'write', 'changePermission', 'all')


class rule(object):
    @staticmethod
    def list_attributes(attributes: dict):
        for attribute in attributes:
            print(attribute, attributes[attribute])

    @staticmethod
    def child_nodes(children: list):
        for child in children:
            print(child[0:-2])


# ==================== Begin of rules section ====================

class accessRule(rule):
    attributes = {
        'id': [OPTIONAL],
        'system': [OPTIONAL],
        'scope': [OPTIONAL],
        'order': [OPTIONAL, 'allowFirst', 'denyFirst'],
        'authSystem': [REQUIRED]
    }
    children = [
        ['allow', 'deny', 1, INFINITY]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(accessRule.attributes, node)
        _children(accessRule.children, node)


class additionalMetadataRule(rule):
    attributes = {
        'id': [OPTIONAL]
    }
    children = [
        ['describes', 0, INFINITY],
        ['metadata', 1, 1]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(additionalMetadataRule.attributes, node)
        _children(additionalMetadataRule.children, node)


class allowRule(rule):
    attributes = {}
    children = [
        ['principal', 1, INFINITY],
        ['permission', 1, INFINITY]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(allowRule.attributes, node)
        _children(allowRule.children, node)


class anyNameRule(rule):
    '''
    Generic rule for names.

    This is a generic rule for evaluating name-based metadata like
    surName, givenName, or salutations.

    Raises:
        MetapypeRuleError: If content is not string or if without child and
        content is empty
    '''
    attributes = {
        'lang': [OPTIONAL]
    }
    children = [
        ['value', 0, INFINITY]
    ]
    content = TYPE_STR

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        if len(node.children) == 0 and node.content is None:
            msg = f'Node "{node.name}" content should not be empty'
            raise MetapypeRuleError(msg)
        _attributes(anyNameRule.attributes, node)
        _children(anyNameRule.children, node)


class datasetRule(rule):
    # TODO: complete rule
    attributes = {}
    children = []
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        # _attributes_list(datasetRule.attributes, node)
        # _children(datasetRule.children, node)


class denyRule(rule):
    attributes = {}
    children = [
        ['principal', 1, INFINITY],
        ['permission', 1, INFINITY]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(denyRule.attributes, node)
        _children(denyRule.children, node)


class emlRule(rule):
    attributes = {
        'packageId': [REQUIRED],
        'system': [REQUIRED],
        'scope': [OPTIONAL],
        'lang': [OPTIONAL]
    }
    children = [
        ['access', 0, 1],
        ['dataset', 'citation', 'software', 'protocol', 1, 1],
        ['additionalMetadata', 0, INFINITY]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(emlRule.attributes, node)
        _children(emlRule.children, node)


class individualNameRule(rule):
    attributes = {}
    children = [
        ['salutation', 0, INFINITY],
        ['givenName', 0, INFINITY],
        ['surName', 1, 1]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(individualNameRule.attributes, node)
        _children(individualNameRule.children, node)


class metadataRule(rule):
    attributes = {}
    children = []
    content = TYPE_STR

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        _attributes(metadataRule.attributes, node)
        _children(metadataRule.children, node)


class permissionRule(rule):
    attributes = {}
    children = []
    content = TYPE_STR

    @staticmethod
    def validate_rule(node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        if node.content not in PERMISSIONS:
            msg = f'Node "{node.name}" content should be one of "{PERMISSIONS}", not "{node.content}"'
            raise MetapypeRuleError(msg)
        _attributes(permissionRule.attributes, node)
        _children(permissionRule.children, node)


class principalRule(rule):
    attributes = {}
    children = []
    content = TYPE_STR

    @staticmethod
    def validate_rule(node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        _attributes(principalRule.attributes, node)
        _children(principalRule.children, node)


class responsiblePartyRule(rule):
    '''
    Generic rule for any responsibleParty type of metadata like creator or
    contact.
    '''
    attributes = {
        'id': [OPTIONAL],
        'system': [OPTIONAL],
        'scope': [OPTIONAL]
    }
    children = [
        ['individualName', 'organizationName', 'positionName', 1, INFINITY],
        ['address', 0, INFINITY],
        ['phone', 0, INFINITY],
        ['electronicMailAddress', 0, INFINITY],
        ['onlineUrl', 0, INFINITY],
        ['userId', 0, INFINITY]
    ]
    content = TYPE_NONE

    @staticmethod
    def validate_rule(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        _attributes(responsiblePartyRule.attributes, node)
        _children(responsiblePartyRule.children, node)


class valueRule(rule):
    attributes = {
        'xml:lang': [REQUIRED]
    }
    children = []
    content = TYPE_STR

    @staticmethod
    def validate_rule(node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        _attributes(valueRule.attributes, node)
        _children(valueRule.children, node)


# ===================== End of rules section =====================

def _attributes(attributes: dict, node: Node) -> None:
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
        required = attributes[attribute][0]
        # Test for required attributes
        if required and attribute not in node.attributes:
            msg = f'"{attribute}" is a required attribute of node "{node.name}"'
            raise MetapypeRuleError(msg)
    for attribute in node.attributes:
        # Test for non-allowed attribute
        if attribute not in attributes:
            msg = f'"{attribute}" is not a recognized attributes of node "{node.name}"'
            raise MetapypeRuleError(msg)
        else:
            # Test for enumerated list of allowed values
            if len(attributes[attribute]) > 1 and node.attributes[
                attribute] not in attributes[attribute][1:]:
                msg = f'Node "{node.name}" attribute "{attribute}" must be one of the following: "{attributes[attribute][1:]}"'
                raise MetapypeRuleError(msg)


def _children(children: list, node: Node) -> None:
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
                    msg = f'Maximum occurrence of "{name}" exceeded for "{node.name}"'
                    raise MetapypeRuleError(msg)
                i += 1
            else:
                break
        if cnt < min:
            msg = f'Minimum occurrence of "{name}" not met for "{node.name}"'
            raise MetapypeRuleError(msg)
    if i < max_i:
        child_name = node.children[i].name
        msg = f'Child "{child_name}" not allowed  for "{node.name}"'
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
    names.ACCESS: accessRule.validate_rule,
    names.ADDITIONALMETADATA: additionalMetadataRule.validate_rule,
    names.ALLOW: allowRule.validate_rule,
    names.CONTACT: responsiblePartyRule.validate_rule,
    names.CREATOR: responsiblePartyRule.validate_rule,
    names.DATASET: datasetRule.validate_rule,
    names.DENY: denyRule.validate_rule,
    names.EML: emlRule.validate_rule,
    names.GIVENNAME: anyNameRule.validate_rule,
    names.INDIVIDUALNAME: individualNameRule.validate_rule,
    names.METADATA: metadataRule.validate_rule,
    names.ORGANIZATIONNAME: anyNameRule.validate_rule,
    names.PERMISSION: permissionRule.validate_rule,
    names.POSITIONNAME: anyNameRule.validate_rule,
    names.PRINCIPAL: principalRule.validate_rule,
    names.SALUTATION: anyNameRule.validate_rule,
    names.SURNAME: anyNameRule.validate_rule,
    names.TITLE: anyNameRule.validate_rule,
    names.VALUE: valueRule.validate_rule,
}

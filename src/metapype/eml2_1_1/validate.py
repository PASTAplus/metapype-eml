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
    def __init__(self):
        self._attributes = {}
        self._children = []
        self._content = None

    def _validate_content(self, content, node: Node):
        pass

    def validate_rule(self, node: Node):
        self._validate_content(self._content, node)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)

    @property
    def attributes(self):
        return self._attributes

    @property
    def children(self):
        return self._children

    @property
    def content(self):
        return self._content


# ==================== Begin of rules section ====================

class accessRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {
            'id': [OPTIONAL],
            'system': [OPTIONAL],
            'scope': [OPTIONAL],
            'order': [OPTIONAL, 'allowFirst', 'denyFirst'],
            'authSystem': [REQUIRED]
        }
        self._children = [
            ['allow', 'deny', 1, INFINITY]
        ]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class additionalMetadataRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {
            'id': [OPTIONAL]
        }
        self._children = [
            ['describes', 0, INFINITY],
            ['metadata', 1, 1]
        ]
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class allowRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = [
            ['principal', 1, INFINITY],
            ['permission', 1, INFINITY]
        ]
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class anyNameRule(rule):
    '''
    Generic rule for names.

    This is a generic rule for evaluating name-based metadata like
    surName, givenName, or salutations.

    Raises:
        MetapypeRuleError: If content is not string or if without child and
        content is empty
    '''
    def __init__(self):
        super().__init__()
        self._attributes = {
            'lang': [OPTIONAL]
        }
        self._children = [
            ['value', 0, INFINITY]
        ]
        self._content = TYPE_STR

    def validate_rule(self, node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        if len(node.children) == 0 and node.content is None:
            msg = f'Node "{node.name}" content should not be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class datasetRule(rule):
    # TODO: complete rule
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        # _attributes_list(self._attributes, node)
        # _children(self._children, node)


class denyRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = [
            ['principal', 1, INFINITY],
            ['permission', 1, INFINITY]
        ]
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class emlRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {
            'packageId': [REQUIRED],
            'system': [REQUIRED],
            'scope': [OPTIONAL],
            'lang': [OPTIONAL]
        }
        self._children = [
            ['access', 0, 1],
            ['dataset', 'citation', 'software', 'protocol', 1, 1],
            ['additionalMetadata', 0, INFINITY]
        ]
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class individualNameRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = [
            ['salutation', 0, INFINITY],
            ['givenName', 0, INFINITY],
            ['surName', 1, 1]
        ]
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class metadataRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_STR

    def validate_rule(self, node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class permissionRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_STR

    def validate_rule(self, node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        if node.content not in PERMISSIONS:
            msg = f'Node "{node.name}" content should be one of "{PERMISSIONS}", not "{node.content}"'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class principalRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_STR

    def validate_rule(self, node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class responsiblePartyRule(rule):
    '''
    Generic rule for any responsibleParty type of metadata like creator or
    contact.
    '''
    def __init__(self):
        super().__init__()
        self._attributes = {
            'id': [OPTIONAL],
            'system': [OPTIONAL],
            'scope': [OPTIONAL]
        }
        self._children = [
            ['individualName', 'organizationName', 'positionName', 1, INFINITY],
            ['address', 0, INFINITY],
            ['phone', 0, INFINITY],
            ['electronicMailAddress', 0, INFINITY],
            ['onlineUrl', 0, INFINITY],
            ['userId', 0, INFINITY]
        ]
        self._content = TYPE_NONE

    def validate_rule(self, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


class valueRule(rule):
    def __init__(self):
        super().__init__()
        self._attributes = {
            'xml:lang': [REQUIRED]
        }
        self._children = []
        self._content = TYPE_STR

    def validate_rule(self, node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        validate_attributes(self._attributes, node)
        validate_children(self._children, node)


# ===================== End of rules section =====================

def validate_attributes(attributes: dict, node: Node) -> None:
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


def validate_children(children: list, node: Node) -> None:
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
    names.ACCESS: accessRule(),
    names.ADDITIONALMETADATA: additionalMetadataRule(),
    names.ALLOW: allowRule(),
    names.CONTACT: responsiblePartyRule(),
    names.CREATOR: responsiblePartyRule(),
    names.DATASET: datasetRule(),
    names.DENY: denyRule(),
    names.EML: emlRule(),
    names.GIVENNAME: anyNameRule(),
    names.INDIVIDUALNAME: individualNameRule(),
    names.METADATA: metadataRule(),
    names.ORGANIZATIONNAME: anyNameRule(),
    names.PERMISSION: permissionRule(),
    names.POSITIONNAME: anyNameRule(),
    names.PRINCIPAL: principalRule(),
    names.SALUTATION: anyNameRule(),
    names.SURNAME: anyNameRule(),
    names.TITLE: anyNameRule(),
    names.VALUE: valueRule(),
}

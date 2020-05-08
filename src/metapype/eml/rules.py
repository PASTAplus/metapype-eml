#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: rules

:Synopsis:
    EML node rule declarations.

:Author:
    servilla
    costa
    ide

:Created:
    6/5/18
"""
import daiquiri

from metapype.eml.exceptions import MetapypeRuleError
from metapype.eml import names
from metapype.model.node import Node


logger = daiquiri.getLogger("validate: " + __name__)


REQUIRED = True
OPTIONAL = False
INFINITY = None

TYPE_NONE = None
TYPE_STR = "str"
TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_DATETIME = "datetime"

PERMISSIONS = ("read", "write", "changePermission", "all")


class Rule(object):
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


class Accessrule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {
            "id": [OPTIONAL],
            "system": [OPTIONAL],
            "scope": [OPTIONAL],
            "order": [OPTIONAL, "allowFirst", "denyFirst"],
            "authSystem": [REQUIRED],
        }
        self._children = [["allow", "deny", 1, INFINITY]]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class Additionalmetadatarule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {"id": [OPTIONAL]}
        self._children = [["describes", 0, INFINITY], ["metadata", 1, 1]]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class Allowrule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = [
            ["principal", 1, INFINITY],
            ["permission", 1, INFINITY],
        ]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class Anynamerule(Rule):
    """
    Generic rule for names.

    This is a generic rule for evaluating name-based metadata like
    surName, givenName, or salutations.

    Raises:
        MetapypeRuleError: If content is not string or if without child and
        content is empty
    """

    def __init__(self):
        super().__init__()
        self._attributes = {"lang": [OPTIONAL]}
        self._children = [["value", 0, INFINITY]]
        self._content = TYPE_STR

    def _validate_content(self, content, node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        if len(node.children) == 0 and node.content is None:
            msg = f'Node "{node.name}" content should not be empty'
            raise MetapypeRuleError(msg)


class DatasetRule(Rule):
    # TODO: complete rule
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)

    # Temporary override for null rule
    def validate_rule(self, node: Node):
        pass


class DenyRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = [
            ["principal", 1, INFINITY],
            ["permission", 1, INFINITY],
        ]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class EmlRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {
            "packageId": [REQUIRED],
            "system": [REQUIRED],
            "scope": [OPTIONAL],
            "lang": [OPTIONAL],
        }
        self._children = [
            ["access", 0, 1],
            ["dataset", "citation", "software", "protocol", 1, 1],
            ["additionalMetadata", 0, INFINITY],
        ]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class IndividualNameRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = [
            ["salutation", 0, INFINITY],
            ["givenName", 0, INFINITY],
            ["surName", 1, 1],
        ]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class MetadataRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_STR

    def _validate_content(self, content, node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)


class PermissionRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_STR

    def _validate_content(self, content, node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)
        if node.content not in PERMISSIONS:
            msg = f'Node "{node.name}" content should be one of "{PERMISSIONS}", not "{node.content}"'
            raise MetapypeRuleError(msg)


class PrincipalRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {}
        self._children = []
        self._content = TYPE_STR

    def _validate_content(self, content, node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)


class ResponsiblePartyRule(Rule):
    """
    Generic rule for any responsibleParty type of metadata like creator or
    contact.
    """

    def __init__(self):
        super().__init__()
        self._attributes = {
            "id": [OPTIONAL],
            "system": [OPTIONAL],
            "scope": [OPTIONAL],
        }
        self._children = [
            [
                "individualName",
                "organizationName",
                "positionName",
                1,
                INFINITY,
            ],
            ["address", 0, INFINITY],
            ["phone", 0, INFINITY],
            ["electronicMailAddress", 0, INFINITY],
            ["onlineUrl", 0, INFINITY],
            ["userId", 0, INFINITY],
        ]
        self._content = TYPE_NONE

    def _validate_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)


class ValueRule(Rule):
    def __init__(self):
        super().__init__()
        self._attributes = {"xml:lang": [REQUIRED]}
        self._children = []
        self._content = TYPE_STR

    def _validate_content(self, content, node: Node):
        if node.content is None or type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)


# ===================== End of rules section =====================


def validate_attributes(attributes: dict, node: Node) -> None:
    """
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
    """
    for attribute in attributes:
        required = attributes[attribute][0]
        # Test for required attributes
        if required and attribute not in node.attributes:
            msg = (
                f'"{attribute}" is a required attribute of node "{node.name}"'
            )
            raise MetapypeRuleError(msg)
    for attribute in node.attributes:
        # Test for non-allowed attribute
        if attribute not in attributes:
            msg = f'"{attribute}" is not a recognized attributes of node "{node.name}"'
            raise MetapypeRuleError(msg)
        else:
            # Test for enumerated list of allowed values
            if (
                len(attributes[attribute]) > 1
                and node.attributes[attribute] not in attributes[attribute][1:]
            ):
                msg = f'Node "{node.name}" attribute "{attribute}" must be one of the following: "{attributes[attribute][1:]}"'
                raise MetapypeRuleError(msg)


def validate_children(children: list, node: Node) -> None:
    """
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
    """
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


dispatcher = {
    names.ACCESS: Accessrule(),
    names.ADDITIONALMETADATA: Additionalmetadatarule(),
    names.ALLOW: Allowrule(),
    names.CONTACT: ResponsiblePartyRule(),
    names.CREATOR: ResponsiblePartyRule(),
    names.DATASET: DatasetRule(),
    names.DENY: DenyRule(),
    names.EML: EmlRule(),
    names.GIVENNAME: Anynamerule(),
    names.INDIVIDUALNAME: IndividualNameRule(),
    names.METADATA: MetadataRule(),
    names.ORGANIZATIONNAME: Anynamerule(),
    names.PERMISSION: PermissionRule(),
    names.POSITIONNAME: Anynamerule(),
    names.PRINCIPAL: PrincipalRule(),
    names.SALUTATION: Anynamerule(),
    names.SURNAME: Anynamerule(),
    names.TITLE: Anynamerule(),
    names.VALUE: ValueRule(),
}

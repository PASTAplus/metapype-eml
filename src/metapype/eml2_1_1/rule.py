#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: rule

:Synopsis:
    EML 2.1.1 node rules processing

:Author:
    servilla
    costa

:Created:
    7/10/18
"""
import daiquiri
import json

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

def load_rules():
    '''
    Load rules from the JSON file into the rules dict
    '''
    with open('eml2_1_1/rules.json') as fh:
        rules_dict = json.load(fh)
    fh.close()
    return (rules_dict)


rules_dict = load_rules()


class Rule(object):
    '''
    The Rule class holds rule content for a specific rule as well as the logic for
    processing content validation.
    '''
    def __init__(self, node_name=None):
        self._attributes = {}
        self._children = []
        self._content = None

        # Initialize rule content for this instance from the rules dict
        rule_data = rules_dict[node_name]
        self._attributes = rule_data[0]
        self._children = rule_data[1]
        self._content = rule_data[2]
        self._content_rules = rule_data[3]

    def validate_rule(self, node: Node):
        '''
        Validates a node for rule compliance by validating the node's
        content, attributes, and children.

        Args:
            node: Node instance to be validates

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        '''
        self._validate_content(self._content, node)
        self._validate_attributes(self._attributes, node)
        self._validate_children(self._children, node)

    def _validate_content(self, content, node: Node):
        '''
        Validates node content for rule compliance.
        For each of the content rules configured for this rule,
        validates the node content to see if its content complies 
        with the content that this rule expects.

        Args:
            content: the type of content which this rule expects
            node: Node instance to be validated

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        '''
        for content_rule in self._content_rules:
            if content_rule == 'emptyContent':
                self._validate_empty_content(content, node)
            elif content_rule == 'nonEmptyContent':
                self._validate_non_empty_content(content, node)
            elif content_rule == 'permissionsContent':
                self._validate_permissions_content(content, node)
            elif content_rule == 'strContent':
                self._validate_str_content(content, node)

    def _validate_empty_content(self, content, node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)

    def _validate_non_empty_content(self, content, node: Node):
        if len(node.children) == 0 and node.content is None:
            msg = f'Node "{node.name}" content should not be empty'
            raise MetapypeRuleError(msg)

    def _validate_permissions_content(self, content, node: Node):
        if node.content not in PERMISSIONS:
            msg = f'Node "{node.name}" content should be one of "{PERMISSIONS}", not "{node.content}"'
            raise MetapypeRuleError(msg)

    def _validate_str_content(self, content, node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)

    def _validate_attributes(self, attributes: dict, node: Node) -> None:
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


    def _validate_children(self, children: list, node: Node) -> None:
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

    @property
    def attributes(self):
        return self._attributes

    @property
    def children(self):
        return self._children

    @property
    def content(self):
        return self._content


# Named constants for EML 2.1.1 metadata rules
RULE_ACCESS = 'accessRule'
RULE_ADDITIONALMETADATA = 'additionalMetadataRule'
RULE_ALLOW = 'allowRule'
RULE_ANYNAME = 'anyNameRule'
RULE_DATASET = 'datasetRule'
RULE_DENY = 'denyRule'
RULE_EML = 'emlRule'
RULE_INDIVIDUALNAME = 'individualNameRule'
RULE_METADATA = 'metadataRule'
RULE_PERMISSION = 'permissionRule'
RULE_PRINCIPAL = 'principalRule'
RULE_RESPONSIBLEPARTY = 'responsiblePartyRule'
RULE_VALUE = 'valueRule'


# Maps node names to their corresponding metadata rule names
node_mappings = {
    names.ACCESS: RULE_ACCESS,
    names.ADDITIONALMETADATA: RULE_ADDITIONALMETADATA,
    names.ALLOW: RULE_ALLOW,
    names.CONTACT: RULE_RESPONSIBLEPARTY,
    names.CREATOR: RULE_RESPONSIBLEPARTY,
    names.DATASET: RULE_DATASET,
    names.DENY: RULE_DENY,
    names.EML: RULE_EML,
    names.GIVENNAME: RULE_ANYNAME,
    names.INDIVIDUALNAME: RULE_INDIVIDUALNAME,
    names.METADATA: RULE_METADATA,
    names.ORGANIZATIONNAME: RULE_ANYNAME,
    names.PERMISSION: RULE_PERMISSION,
    names.POSITIONNAME: RULE_ANYNAME,
    names.PRINCIPAL: RULE_PRINCIPAL,
    names.SALUTATION: RULE_ANYNAME,
    names.SURNAME: RULE_ANYNAME,
    names.TITLE: RULE_ANYNAME,
    names.VALUE: RULE_VALUE,
}


def get_rule_name(node_name: str):
    '''
    Helper function.
    For a given node name, return its corresponding rule name
    '''
    return node_mappings.get(node_name)


def get_rule(node_name: str):
    '''
    Helper function.
    For a given node name, instantiate its corresponding rule object and return it
    '''
    rule_name = get_rule_name(node_name)
    return Rule(rule_name)


def main():
    eml_rule = Rule('emlRule')
    print(eml_rule)


if __name__ == "__main__":
    main()

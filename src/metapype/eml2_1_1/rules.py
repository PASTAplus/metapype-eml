#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: rules

:Synopsis:

:Author:
    servilla

:Created:
    6/4/18
"""
import daiquiri

from metapype.eml2_1_1.exceptions import MPLRuleError
from metapype.model.node import Node


logger = daiquiri.getLogger('rules: ' + __name__)

REQUIRED = True
OPTIONAL = False
INFINITY = None


def access_rule(node: Node):
    rules = [
        ['allow', 'deny', 1, INFINITY]
    ]
    process_rules(rules, node)
    attributes = {
        'id': OPTIONAL,
        'system': OPTIONAL,
        'scope': OPTIONAL,
        'order': OPTIONAL,
        'authSystem': REQUIRED
    }
    process_attributes(attributes, node)
    if 'order' in node.attributes:
        allowed = ['allowFirst', 'denyFirst']
        if node.attributes['order'] not in allowed:
            msg = '"{0}:order" attribute must be one of "{1}"'.format(node.rank, allowed)
            raise MPLRuleError(msg)


def additional_metadata_rule(node: Node):
    rules = [
        ['describes', 0, INFINITY],
        ['metadata', 1, 1]
    ]
    process_rules(rules, node)
    attributes = {
        'id': OPTIONAL
    }
    process_attributes(attributes, node)


def allow_rule(node: Node):
    rules = [
        ['principal', 1, INFINITY],
        ['permission', 1, INFINITY]
    ]
    process_rules(rules, node)


def any_name_rule(node: Node):
    rules = [
        ['value', 0, INFINITY]
    ]
    process_rules(rules, node)
    attributes = {
        'lang': OPTIONAL
    }
    process_attributes(attributes, node)
    if node.content is not None and type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(node.rank, type(node.content))
        raise MPLRuleError(msg)
    if len(node.children) == 0 and node.content is None:
        msg = 'Node "{0}" content should not be empty'.format(node.rank)
        raise MPLRuleError(msg)

def dataset_rule(node: Node):
    pass


def deny_rule(node: Node):
    rules = [
        ['principal', 1, INFINITY],
        ['permission', 1, INFINITY]
    ]
    process_rules(rules, node)


def eml_rule(node: Node):
    rules = [
        ['access', 0, 1],
        ['dataset', 'citation', 'software', 'protocol', 1, 1],
        ['additionalMetadata', 0, INFINITY]
    ]
    process_rules(rules, node)
    attributes = {
        'packageId': REQUIRED,
        'system': REQUIRED,
        'scope': OPTIONAL,
        'lang': OPTIONAL
    }
    process_attributes(attributes, node)


def individual_name_rule(node: Node):
    rules = [
        ['salutation', 0, INFINITY],
        ['givenName', 0, INFINITY],
        ['surName', 1, 1]
    ]
    process_rules(rules, node)


def metadata_rule(node: Node):
    if len(node.children) != 0:
        msg = 'Node "{0}" should not have children'.format(node.rank)
        raise MPLRuleError(msg)
    if type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(node.rank, type(node.content))
        raise MPLRuleError(msg)


def permission_rule(node: Node):
    if len(node.children) != 0:
        msg = 'Node "{0}" should not have children'.format(node.rank)
        raise MPLRuleError(msg)
    allowed = ['read', 'write', 'changePermission', 'all']
    if node.content not in allowed:
        msg = 'Node "{0}" content should be one of "{1}", not "{2}"'.format(node.rank, allowed, node.content)
        raise MPLRuleError(msg)


def principal_rule(node: Node):
    if len(node.children) != 0:
        msg = 'Node "{0}" should not have children'.format(node.rank)
        raise MPLRuleError(msg)
    if type(node.content) is not str:
        msg = 'Node content should be type string, not "{0}"'.format(type(node.content))
        raise MPLRuleError(msg)


def responsible_party_rule(node: Node):
    rules = [
        ['individualName', 'organizationName', 'positionName', 1, INFINITY],
        ['address', 0, INFINITY],
        ['phone', 0, INFINITY],
        ['electronicMailAddress', 0, INFINITY],
        ['onlineUrl', 0, INFINITY],
        ['userId', 0, INFINITY]
    ]
    process_rules(rules, node)
    attributes = {
        'id': OPTIONAL,
        'system': OPTIONAL,
        'scope': OPTIONAL
    }
    process_attributes(attributes, node)


def title_rule(node: Node):
    if node.content is not None and type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(node.rank, type(node.content))
        raise MPLRuleError(msg)
    rules = [
        ['value', 0, INFINITY]
    ]
    process_rules(rules, node)
    attributes = {
        'lang': OPTIONAL
    }
    process_attributes(attributes, node)


def value_rule(node: Node):
    if node.content is None:
        msg = 'Node "{0}" content cannot be empty'.format(node.rank)
        raise MPLRuleError(msg)
    if type(node.content) is not str:
        msg = 'Node "{0}" content should be type string, not "{1}"'.format(node.rank, type(node.content))
        raise MPLRuleError(msg)
    attributes = {
        'xml:lang': REQUIRED,
    }
    process_attributes(attributes, node)


def process_rules(rules, node: Node):
    i = 0
    max_i = len(node.children)
    for rule in rules:
        rank = rule[:-2]
        min = rule[-2]
        max = rule[-1]
        cnt = 0
        while i < max_i:
            child_rank = node.children[i].rank
            if child_rank in rank:
                cnt += 1
                if max is not INFINITY and cnt > max:
                    msg = 'Maximum occurrence of "{0}" exceeded for "{1}"'.format(rank, node.rank)
                    raise MPLRuleError(msg)
                i += 1
            else: break
        if cnt < min:
            msg = 'Minimum occurrence of "{0}" not met for "{1}"'.format(rank, node.rank)
            raise MPLRuleError(msg)
    if i < max_i:
        child_rank = node.children[i].rank
        msg = 'Child "{0}" not allowed  for "{1}"'.format(child_rank, node.rank)
        raise MPLRuleError(msg)


def  process_attributes(attributes, node: Node):
    for attribute in attributes:
        required = attributes[attribute]
        if required and attribute not in node.attributes:
            msg = '"{0}" is a required attribute of node "{1}"'.format(attribute, node.rank)
            raise MPLRuleError(msg)
    for attribute in node.attributes:
        if attribute not in attributes:
            msg = '"{0}" is not a recognized attributes of node "{1}"'.format(attribute, node.rank)
            raise MPLRuleError(msg)



rules = {
    'access': access_rule,
    'additionalMetadata': additional_metadata_rule,
    'allow': allow_rule,
    'contact': responsible_party_rule,
    'creator': responsible_party_rule,
    'dataset': dataset_rule,
    'deny': deny_rule,
    'eml': eml_rule,
    'givenName': any_name_rule,
    'individualName': individual_name_rule,
    'metadata': metadata_rule,
    'organizationName': any_name_rule,
    'permission': permission_rule,
    'positionName': any_name_rule,
    'principal': principal_rule,
    'salutation': any_name_rule,
    'surName': any_name_rule,
    'title': title_rule,
    'value': value_rule,
}


def main():
    return 0


if __name__ == "__main__":
    main()

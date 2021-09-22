#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: rule

:Synopsis:
    EML node rules processing

:Author:
    servilla
    costa
    ide

:Created:
    7/10/18
"""
import datetime
from datetime import time
import importlib.resources
import json
from typing import Optional

import daiquiri
from rfc3986 import uri_reference, validators
from rfc3986.exceptions import (
    InvalidComponentsError,
    MissingComponentError,
    UnpermittedComponentError
)

from metapype.eml.exceptions import (
    ChildNotAllowedError,
    MaxOccurrenceExceededError,
    MetapypeRuleError,
    MinOccurrenceUnmetError,
    ContentExpectedUriError,
    StrContentUnicodeError,
    UnknownContentRuleError,
)
from metapype.eml import names
from metapype.eml.validation_errors import ValidationError
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
TYPE_YEARDATE = "yearDate"


def load_rules():
    """
    Load rules from the JSON file into the rules dict
    """

    rules = importlib.resources.read_text("metapype.eml", "rules.json")
    _rules_dict = json.loads(rules)
    return _rules_dict


rules_dict = load_rules()


class Rule(object):
    """
    The Rule class holds rule content for a specific rule as well as the logic for
    processing content validation.
    """

    def __init__(self, rule_name):
        self._name = rule_name
        rule_data = rules_dict[rule_name]
        self._attributes = rule_data[0]
        self._children = rule_data[1]
        self._content = rule_data[2]
        self._rule_children_names = self._get_rule_children_names(self._children)
        self._depth = 0

    @staticmethod
    def child_list_node_names(child_list: list):
        if list is None or len(child_list) < 3:
            raise MetapypeRuleError(
                "Child list must contain at least 3 elements"
            )
        node_names = child_list[:-2]
        return node_names

    @staticmethod
    def child_list_min_occurrences(child_list: list):
        if list is None or len(child_list) < 3:
            raise MetapypeRuleError(
                "Child list must contain at least 3 elements"
            )
        min_occurrences = child_list[-2]
        return min_occurrences

    @staticmethod
    def child_list_max_occurrences(child_list: list):
        if list is None or len(child_list) < 3:
            raise MetapypeRuleError(
                "Child list must contain at least 3 elements"
            )
        max_occurrences = child_list[-1]
        return max_occurrences

    @staticmethod
    def is_float(val: str = None):
        """
        Boolean to determine whether node content is
        (or can be converted to) a valid float value.
        """
        is_valid = False
        if val is None:
            return False
        try:
            __ = float(val)
            is_valid = True
        except ValueError:
            pass
        return is_valid

    @staticmethod
    def is_int(val: str = None):
        """
        Boolean to determine whether node content is
        (or can be converted to) a valid int value.
        """
        is_valid = False
        if val:
            try:
                __ = int(val)
                is_valid = True
            except ValueError:
                pass
        return is_valid

    @staticmethod
    def is_yeardate(val: str = None):
        """
        Boolean to determine whether node content is a valid yearDate value.
        """
        is_valid = False
        if val and type(val) is str:
            for yeardate_format in ["%Y", "%Y-%m-%d"]:
                try:
                    datetime.datetime.strptime(val, yeardate_format)
                    is_valid = True
                    break
                except ValueError as ex:
                    logger.debug(ex)
        return is_valid

    @staticmethod
    def is_uri(val: str = None) -> bool:
        """
        Boolean to determine whether node content is a valid uri.
        Args:
            val: String value of uri

        Returns: boolean

        """
        is_valid = False
        validator = validators.Validator().allow_schemes(
            "http", "https", "ftp"
        ).require_presence_of(
            "scheme", "host"
        ).check_validity_of(
            "scheme", "host", "path"
        )
        uri = uri_reference(val)
        try:
            validator.validate(uri)
            is_valid = True
        except (InvalidComponentsError, MissingComponentError, UnpermittedComponentError) as ex:
            logger.debug(ex)
        return is_valid

    @staticmethod
    def is_time(val: str = None):
        """
        Boolean to determine whether node content is a valid time value.
        """
        is_valid = False
        if val and type(val) is str:
            try:
                time.fromisoformat(val)
                is_valid = True
            except ValueError as ex:
                logger.debug(ex)
        return is_valid

    def child_insert_index(self, parent: Node, new_child: Node) -> int:
        """
        Determines the index location of a new child node in a given parent node
        based on the parent node's rule type. Note that only a legal position in
        the list of possible children is guaranteed; parent node validity may be
        based on other constraint of the rule type.

        Args:
            parent: Parent node of which to be adding child node
            new_child: Child node to be added

        Returns:
            int: Index location of new child node

        """
        try:
            new_child_index = self._rule_children_names.index(new_child.name)
        except ValueError as e:
            msg = f"Child '{new_child.name}' not allowed in parent '{parent.name}'"
            raise ChildNotAllowedError(msg)
        for index, child in enumerate(parent.children):
            parent_child_index = self._rule_children_names.index(child.name)
            if parent_child_index > new_child_index:
                return index
        index = len(parent.children)
        return index

    @staticmethod
    def _is_in_path(rule_children: list, node: Node) -> bool:
        is_in_path = False
        if Rule._is_rule_child(rule_children):
            return rule_children[0] == node.name
        elif Rule._is_sequence(rule_children):
            for child in rule_children:
                is_in_path = Rule._is_in_path(child, node)
                if is_in_path:
                    break
        else:
            for child in rule_children[:-2]:
                is_in_path = Rule._is_in_path(child, node)
                if is_in_path:
                    break
        return is_in_path

    def is_required_attribute(self, attribute: str):
        if attribute in self._attributes:
            return self._attributes[attribute][0]
        else:
            raise Exception(f"Unknown attribute {attribute}")

    def is_allowed_child(self, child_name: str):
        return child_name in self._rule_children_names

    def allowed_attribute_values(self, attribute: str):
        values = []
        if attribute in self._attributes:
            if len(self._attributes[attribute]) > 1:
                values = self._attributes[attribute][1:]
        else:
            raise Exception(f"Unknown attribute {attribute}")
        return values

    def has_enum_content(self):
        return "content_enum" in self._content

    def validate_rule(self, node: Node, errs: list = None):
        """
        Validates a node for rule compliance by validating the node's
        content, attributes, and children.

        Args:
            node: Node instance to be validated
            errs: List of validation errors

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        """
        if self.name in (RULE_TEXT, RULE_ANYNAME):
            is_mixed_content = True
        else:
            is_mixed_content = False

        self._validate_content(node, is_mixed_content, errs)
        self._validate_attributes(node, errs)
        self._validate_children(node, is_mixed_content, errs)

    def _validate_content(self, node: Node, is_mixed_content: bool, errs: list = None):
        """
        Validates node content for rule compliance.
        For each of the content rules configured for this rule,
        validates the node to see if its content complies
        with the content that this rule expects.

        Args:
            node: Node instance to be validated

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        """
        for content_rule in self._content["content_rules"]:
            if content_rule == "emptyContent":
                self._validate_empty_content(node, errs)
            elif content_rule == "floatContent":
                self._validate_float_content(node, errs)
            elif content_rule == "floatRangeContent_EW":
                self._validate_float_range_ew_content(node, errs)
            elif content_rule == "floatRangeContent_NS":
                self._validate_float_range_ns_content(node, errs)
            elif content_rule == "floatContent_Nonnegative":
                self._validate_float_content_nonnegative(node, errs)
            elif content_rule == "intContent":
                self._validate_int_content(node, errs)
            elif content_rule == "nonEmptyContent":
                self._validate_non_empty_content(node, is_mixed_content, errs)
            elif content_rule == "strContent":
                self._validate_str_content(node, errs)
            elif content_rule == "timeContent":
                self._validate_time_content(node, errs)
            elif content_rule == 'uriContent':
                self._validate_uri_content(node, errs)
            elif content_rule == "yearDateContent":
                self._validate_yeardate_content(node, errs)
            elif content_rule == "anyContent":
                pass
            else:
                msg = f"Node {node.name} content type rule {content_rule} not recognized"
                if errs is None:
                    raise UnknownContentRuleError(msg)
                else:
                    errs.append(
                        (
                            ValidationError.UNKNOWN_CONTENT_RULE,
                            msg,
                            node,
                        )
                    )

        if self.has_enum_content():
            enum_values = self._content["content_enum"]
            self._validate_enum_content(node, enum_values, errs)

    @staticmethod
    def _validate_empty_content(node: Node, errs: list = None):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_EMPTY,
                        msg,
                        node,
                        node.content,
                    )
                )

    @staticmethod
    def _validate_enum_content(
        node: Node, enum_values: list, errs: list = None
    ):
        if node.content not in enum_values:
            msg = f'Node "{node.name}" content should be one of "{enum_values}", not "{node.content}"'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_ENUM,
                        msg,
                        node,
                        enum_values,
                        node.content,
                    )
                )

    @staticmethod
    def _validate_int_content(node: Node, errs: list = None):
        val = node.content
        if val is not None and not Rule.is_int(val):
            msg = f'Node "{node.name}" content should be type "{TYPE_INT}", not "{type(node.content)}"'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_INT,
                        msg,
                        node,
                        type(node.content),
                    )
                )

    @staticmethod
    def _validate_float_content(node: Node, errs: list = None):
        val = node.content
        if val is not None and not Rule.is_float(val):
            msg = f'Node "{node.name}" content should be type "{TYPE_FLOAT}", not "{type(node.content)}"'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_FLOAT,
                        msg,
                        node,
                        type(node.content),
                    )
                )

    def _validate_float_range_content(
        self, node: Node, minmax, errs: list = None
    ):
        self._validate_float_content(node, errs)
        float_val = float(node.content)
        if float_val < minmax[0] or float_val > minmax[1]:
            msg = f'Node "{node.name}" content should be in range {minmax}'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_RANGE,
                        msg,
                        node,
                        minmax[0],
                        minmax[1],
                        float_val,
                    )
                )

    def _validate_float_nonnegative(
        self, node: Node, errs: list = None
    ):
        self._validate_float_content(node, errs)
        float_val = float(node.content)
        if float_val < 0:
            msg = f'Node "{node.name}" content should be non-negative'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_RANGE,
                        msg,
                        node,
                        0,
                        None,
                        float_val,
                    )
                )

    def _validate_float_range_ew_content(self, node: Node, errs: list = None):
        self._validate_float_range_content(node, (-180.0, 180.0), errs)

    def _validate_float_range_ns_content(self, node: Node, errs: list = None):
        self._validate_float_range_content(node, (-90.0, 90.0), errs)

    def _validate_float_content_nonnegative(self, node: Node, errs: list = None):
        self._validate_float_nonnegative(node, errs)

    @staticmethod
    def _validate_non_empty_content(node: Node, is_mixed_content: bool, errs: list = None):
        if node.content is None or len(str(node.content)) == 0:
            if (is_mixed_content and len(node.children) == 0) or not is_mixed_content:
                msg = f'Node "{node.name}" content should not be empty'
                if errs is None:
                    raise MetapypeRuleError(msg)
                else:
                    errs.append(
                        (ValidationError.CONTENT_EXPECTED_NONEMPTY, msg, node)
                    )

    @staticmethod
    def _validate_str_content(node: Node, errs: list = None):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_STRING,
                        msg,
                        node,
                        type(node.content),
                    )
                )
        if node.content is not None:
            try:
                node.content.encode(encoding="utf-8", errors="strict")
            except UnicodeError as ex:
                msg = f'Node "{node.name}" content contains non-unicode character(s)'
                if errs is None:
                    raise StrContentUnicodeError(msg)
                else:
                    errs.append(
                        (
                            ValidationError.CONTENT_EXPECTED_STRING,
                            msg,
                            node,
                            type(node.content),
                        )
                    )

    @staticmethod
    def _validate_time_content(node: Node, errs: list = None):
        val = node.content
        if val is not None and not Rule.is_time(val):
            msg = f'Node "{node.name}" format should be time ("HH:MM:SS" or "HH:MM:SS.f")'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_TIME_FORMAT,
                        msg,
                        node,
                        node.content,
                    )
                )

    @staticmethod
    def _validate_uri_content(node: Node, errs: list = None):
        uri = node.content
        if uri is not None and not Rule.is_uri(uri):
            msg = f'Node "{node.name}" uri content "{uri}" is not valid'
            if errs is None:
                raise ContentExpectedUriError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_URI,
                        msg,
                        node,
                        node.content,
                    )
                )

    @staticmethod
    def _validate_yeardate_content(node: Node, errs: list = None):
        val = node.content
        if val is not None and not Rule.is_yeardate(val):
            msg = f'Node "{node.name}" format should be year ("YYYY") or date ("YYYY-MM-DD")'
            if errs is None:
                raise MetapypeRuleError(msg)
            else:
                errs.append(
                    (
                        ValidationError.CONTENT_EXPECTED_YEAR_FORMAT,
                        msg,
                        node,
                        node.content,
                    )
                )

    def _validate_attributes(self, node: Node, errs: list = None) -> None:
        """
        Validates node attributes for rule compliance.

        Iterates through the dict of attribute rules and validates whether
        the node instance complies with the rule.

        Args:
            node: Node instance to be validated

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        """
        for attribute in self._attributes:
            required = self._attributes[attribute][0]
            # Test for required attributes
            if required and attribute not in node.attributes:
                msg = f'"{attribute}" is a required attribute of node "{node.name}"'
                if errs is None:
                    raise MetapypeRuleError(msg)
                else:
                    errs.append(
                        (
                            ValidationError.ATTRIBUTE_REQUIRED,
                            msg,
                            node,
                            attribute,
                        )
                    )
        for attribute in node.attributes:
            # Test for non-allowed attribute
            if attribute not in self._attributes:
                msg = f'"{attribute}" is not a recognized attribute of node "{node.name}"'
                if errs is None:
                    raise MetapypeRuleError(msg)
                else:
                    errs.append(
                        (
                            ValidationError.ATTRIBUTE_UNRECOGNIZED,
                            msg,
                            node,
                            attribute,
                        )
                    )
            else:
                # Test for enumerated list of allowed values
                if (
                    len(self._attributes[attribute]) > 1
                    and node.attributes[attribute]
                    not in self._attributes[attribute][1:]
                ):
                    msg = f'Node "{node.name}" attribute "{attribute}" must be one of the following: "{self._attributes[attribute][1:]}"'
                    if errs is None:
                        raise MetapypeRuleError(msg)
                    else:
                        errs.append(
                            (
                                ValidationError.ATTRIBUTE_EXPECTED_ENUM,
                                msg,
                                node,
                                attribute,
                                self._attributes[attribute][1:],
                            )
                        )

    def _validate_children(self, node: Node, is_mixed_content: bool, errs: list = None) -> None:
        """
        Validates node children for rule compliance.

        1. Ignores validation of children if parent node is "metadata"
        2. Ensures children are valid for node
        3. Iterates through the list children rules and validates whether
           the node instance complies with the rules.

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal child, bad sequence or choice, missing
            child, or wrong child cardinality
        """
        self._node = node
        self._node_children_names = []
        self._node_index = 0

        if self._node.name == names.METADATA:
            # Metadata nodes may contain any type of child node, but only one such node
            if len(self._node.children) > 1:
                msg = f"Maximum occurrence of 1 child exceeded in parent '{names.METADATA}'"
                if errs is None:
                    raise MaxOccurrenceExceededError(msg)
                else:
                    errs.append((ValidationError.MAX_OCCURRENCE_EXCEEDED, msg, self._node))

        else:
            for node_child in self._node.children:
                self._node_children_names.append(node_child.name)

            # Test for non-valid children
            for node_child_name in self._node_children_names:
                if not self.is_allowed_child(node_child_name):
                    msg = f"Child '{node_child_name}' not allowed in parent '{self._node.name}'"
                    if errs is None:
                        raise ChildNotAllowedError(msg)
                    else:
                        errs.append((ValidationError.CHILD_NOT_ALLOWED, msg, self._node, node_child_name))

            if len(self._children) > 0:
                # Begin validation of children
                modality = Rule._get_children_modality(self._children)
                if modality == "sequence":
                    self._validate_sequence(self._children, is_mixed_content, errs)
                else:
                    self._validate_choice(self._children, is_mixed_content, errs)

            if self._node_index != len(self._node_children_names):
                msg = (
                    f"Child '{self._node_children_names[self._node_index]}' "
                    f"is not allowed in this position for parent '{self._node.name}'"
                )
                if errs is None:
                    raise ChildNotAllowedError(msg)
                else:
                    errs.append(
                        (
                            ValidationError.CHILD_NOT_ALLOWED,
                            msg,
                            self._node,
                            self._node_children_names[self._node_index],
                        )
                    )

    def _validate_sequence(self, rule_children: list, is_mixed_content: bool, errs: list = None):
        for rule_child in rule_children:
            if Rule._get_children_modality(rule_child) == "choice":
                self._validate_choice(rule_child, is_mixed_content, errs)
            else:
                self._validate_rule_child(rule_child, False, errs)

    def _validate_choice(self, rule_children: list, is_mixed_content: bool, errs: list = None):
        choice_min = rule_children[-2]
        choice_max = rule_children[-1]
        choice_occurrence = 0

        while (
                self._node_index < len(self._node_children_names) and
                self._node_children_names[self._node_index] in self._get_rule_children_names(rule_children)
        ):
            for rule_child in rule_children[:-2]:
                if self._node_index == len(self._node_children_names):
                    break
                modality = Rule._get_children_modality(rule_child)
                if modality == "sequence":
                    if self._node_children_names[self._node_index] in self._get_rule_children_names(rule_child):
                        self._validate_sequence(rule_child, is_mixed_content, errs)
                        choice_occurrence += 1
                elif modality == "choice":
                    if self._node_children_names[self._node_index] in self._get_rule_children_names(rule_child):
                        self._validate_choice(rule_child, is_mixed_content, errs)
                        choice_occurrence += 1
                else:
                    if self._node_children_names[self._node_index] == rule_child[0]:
                        self._validate_rule_child(rule_child, True, errs)
                        choice_occurrence += 1
        if choice_max is not INFINITY and choice_occurrence > choice_max:
            msg = f"Maximum occurrence of '{choice_max}' exceeded for choice in parent '{self._node.name}'"
            if errs is None:
                raise MaxOccurrenceExceededError(msg)
            else:
                errs.append(
                    (
                        ValidationError.MAX_CHOICE_EXCEEDED,
                        msg,
                        self._node,
                        self._node.name,
                        choice_max,
                    )
                )
        if choice_occurrence < choice_min and not is_mixed_content:
            msg = f"Minimum occurrence of '{choice_min}' not met for choice in parent '{self._node.name}'"
            if errs is None:
                raise MinOccurrenceUnmetError(msg)
            else:
                errs.append(
                    (
                        ValidationError.MIN_CHOICE_UNMET,
                        msg,
                        self._node,
                        self._node.name,
                        choice_min,
                    )
                )

    def _validate_rule_child(self, rule_child: list, limit_max: bool, errs: list = None):
        rule_child_name = rule_child[0]
        rule_child_min = rule_child[-2]
        rule_child_max = rule_child[-1]
        occurrence = 0
        while (
                self._node_index < len(self._node_children_names) and
                rule_child_name == self._node_children_names[self._node_index]
        ):
            occurrence += 1
            self._node_index += 1
            if limit_max and occurrence == rule_child_max:
                return None
            if rule_child_max is not INFINITY and occurrence > rule_child_max:
                msg = (
                    f"Maximum occurrence of '{rule_child_max}' "
                    f"exceeded for child '{self._node_children_names[self._node_index]}' in parent "
                    f"'{self._node.name}'"
                )
                if errs is None:
                    raise MaxOccurrenceExceededError(msg)
                else:
                    errs.append(
                        (
                            ValidationError.MAX_OCCURRENCE_EXCEEDED,
                            msg,
                            self._node,
                            None if self._node_index >= len(self._node_children_names)
                            else self._node_children_names[self._node_index],
                            rule_child_max,
                        )
                    )
        if occurrence < rule_child_min:
            msg = (
                f"Minimum occurrence of '{rule_child_min}' "
                f"not met for child '{rule_child_name}' in parent '{self._node.name}'"
            )
            if errs is None:
                raise MinOccurrenceUnmetError(msg)
            else:
                errs.append(
                    (
                        ValidationError.MIN_OCCURRENCE_UNMET,
                        msg,
                        self._node,
                        rule_child_name,
                        # None if self._node_index >= len(self._node_children_names)
                        # else self._node_children_names[self._node_index],
                        rule_child_min,
                    )
                )

    @staticmethod
    def _get_children_modality(rule_children: list) -> str:
        if Rule._is_rule_child(rule_children):
            mode = "child_rule"
        elif Rule._is_sequence(rule_children):
            mode = "sequence"
        elif Rule._is_choice(rule_children):
            mode = "choice"
        else:
            msg = f"Unknown modality for {rule_children}"
            raise ValueError(msg)
        return mode

    @staticmethod
    def _is_rule_child(rule_children: list) -> bool:
        # of the form ["str", int, int|None]
        is_rule_child = False
        if isinstance(rule_children[0], str):
            is_rule_child = True
        return is_rule_child

    @staticmethod
    def _is_sequence(rule_children: list) -> bool:
        # of the form [["str", int, int|None]...[]]]
        is_sequence = False
        if len(rule_children) >= 1 and isinstance(rule_children[-1], list):
            is_sequence = True
        return is_sequence

    @staticmethod
    def _is_choice(rule_children: list) -> bool:
        # of the form [["str", int, int|None]...[], int, int|None]]
        is_choice = False
        if len(rule_children) >= 3 and (isinstance(rule_children[0], list) and isinstance(rule_children[-2], int)):
            is_choice = True
        return is_choice

    @staticmethod
    def _get_rule_children_names(children: list) -> list:
        children_names = []
        if len(children) > 0:
            modality = Rule._get_children_modality(children)
            if modality == "choice":
                children_names += Rule._get_rule_children_names(children[:-2])
            elif modality == "sequence":
                for child in children:
                    children_names += Rule._get_rule_children_names(child)
            else:
                children_names.append(children[0])
        return children_names

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes

    @property
    def children(self):
        return self._children

    @property
    def content_rules(self):
        return self._content["content_rules"]

    @property
    def content_enum(self):
        if self.has_enum_content():
            return self._content["content_enum"]
        else:
            return []


# Named constants for EML metadata rules
RULE_ACCESS = "accessRule"
RULE_ACCURACY = "accuracyRule"
RULE_ADDITIONALMETADATA = "additionalMetadataRule"
RULE_ADDRESS = "addressRule"
RULE_ALLOW = "allowRule"
RULE_ALTERNATEIDENTIFIER = "alternateIdentifierRule"
RULE_ALTITUDEUNITS = "altitudeUnitsRule"
RULE_ANNOTATION = "annotationRule"
RULE_ANYINT = "anyIntRule"
RULE_ANYNAME = "anyNameRule"
RULE_ANYSTRING = "anyStringRule"
RULE_ANYURI = "anyURIRule"
RULE_ATTRIBUTE = "attributeRule"
RULE_ATTRIBUTELIST = "attributeListRule"
RULE_AUTHENTICATION = "authenticationRule"
RULE_AWARD = "awardRule"
RULE_BINARYRASTER_FORMAT = "binaryRasterFormatRule"
RULE_BOUNDINGALTITUDES = "boundingAltitudesRule"
RULE_BOUNDINGCOORDINATE_EW = "boundingCoordinateRule_EW"
RULE_BOUNDINGCOORDINATE_NS = "boundingCoordinateRule_NS"
RULE_BOUNDINGCOORDINATES = "boundingCoordinatesRule"
RULE_BOUNDS = "boundsRule"
RULE_CODEDEFINITION = "codeDefinitionRule"
RULE_COMPLEX = "complexRule"
RULE_COVERAGE = "coverageRule"
RULE_DATAFORMAT = "dataFormatRule"
RULE_DATASET = "datasetRule"
RULE_DATASOURCE = "datasetRule"
RULE_DATATABLE = "dataTableRule"
RULE_DATETIME = "dateTimeRule"
RULE_DATETIMEDOMAIN = "dateTimeDomainRule"
RULE_DENY = "denyRule"
RULE_DESCRIPTOR = "descriptorRule"
RULE_DISTRIBUTION = "distributionRule"
RULE_EML = "emlRule"
RULE_ENTITYCODELIST = "entityCodeListRule"
RULE_ENUMERATEDDOMAIN = "enumeratedDomainRule"
RULE_EXTERNALCODESET = "externalCodeSetRule"
RULE_EXTERNALLYDEFINIEDFORMAT = "externallyDefinedFormatRule"
RULE_FUNDING = "fundingRule"
RULE_GEOGRAPHICCOVERAGE = "geographicCoverageRule"
RULE_INDIVIDUALNAME = "individualNameRule"
RULE_INTERVALRATIO = "intervalRatioRule"
RULE_KEYWORD = "keywordRule"
RULE_KEYWORDSET = "keywordSetRule"
RULE_KEYWORDTHESAURUS = "keywordThesaurusRule"
RULE_LICENSED = "licensedRule"
RULE_MAINTENANCE = "maintenanceRule"
RULE_MEASUREMENTSCALE = "measurementScaleRule"
RULE_METADATA = "metadataRule"
RULE_METHODS = "methodsRule"
RULE_METHODSTEP = "methodStepRule"
RULE_MINMAX = "minMaxRule"
RULE_MISSINGVALUECODE = "missingValueCodeRule"
RULE_MULTIBAND = "multiBandRule"
RULE_NOMINAL = "nominalOrdinalRule"
RULE_NONNEGATIVEFLOAT = "nonNegativeFloatRule"
RULE_NONNUMERICDOMAIN = "nonNumericDomainRule"
RULE_NUMERICDOMAIN = "numericDomainRule"
RULE_OFFLINE = "offlineRule"
RULE_ONLINE = "onlineRule"
RULE_ORDINAL = "nominalOrdinalRule"
RULE_OTHERENTITY = "otherEntityRule"
RULE_PERMISSION = "permissionRule"
RULE_PHONE = "phoneRule"
RULE_PHYSICAL = "physicalRule"
RULE_PRINCIPAL = "principalRule"
RULE_PROJECT = "projectRule"
RULE_PROPERTYURI = "propertyUriRule"
RULE_QUALITYCONTROL = "qualityControlRule"
RULE_QUANTITATIVEATTRIBUTEACCURACYASSESSMENT = (
    "quantitativeAttributeAccuracyAssessmentRule"
)
RULE_RANGEOFDATES = "rangeOfDatesRule"
RULE_RATIO = "ratioRule"
RULE_REFERENCES = "referencesRule"
RULE_RELATEDPROJECT = "relatedProjectRule"
RULE_RESPONSIBLEPARTY = "responsiblePartyRule"
RULE_RESPONSIBLEPARTY_WITH_ROLE = "responsiblePartyWithRoleRule"
RULE_ROLE = "roleRule"
RULE_ROWCOLUMN = "rowColumnRule"
RULE_SAMPLING = "samplingRule"
RULE_SECTION = "sectionRule"
RULE_SINGLEDATETIME = "singleDateTimeRule"
RULE_SIMPLEDELIMITED = "simpleDelimitedRule"
RULE_SIZE = "sizeRule"
RULE_STORAGETYPE = "storageTypeRule"
RULE_STUDYAREADESCRIPTION = "studyAreaDescriptionRule"
RULE_STUDYEXTENT = "studyExtentRule"
RULE_TAXONID = "taxonIdRule"
RULE_TAXONOMICCLASSIFICATION = "taxonomicClassificationRule"
RULE_TAXONOMICCOVERAGE = "taxonomicCoverageRule"
RULE_TEMPORALCOVERAGE = "temporalCoverageRule"
RULE_TEXT = "textRule"
RULE_TEXTDELIMITED = "textDelimitedRule"
RULE_TEXTDOMAIN = "textDomainRule"
RULE_TEXTFIXED = "textFixedRule"
RULE_TEXTFORMAT = "textFormatRule"
RULE_TIME = "timeRule"
RULE_UNIT = "unitRule"
RULE_URL = "urlRule"
RULE_USERID = "userIdRule"
RULE_VALUE = "valueRule"
RULE_VALUEURI = "valueUriRule"
RULE_YEARDATE = "yearDateRule"


# Maps node names to their corresponding metadata rule names
node_mappings = {
    names.ABSTRACT: RULE_TEXT,
    names.ACCESS: RULE_ACCESS,
    names.ACCURACY: RULE_ACCURACY,
    names.ACKNOWLEDGEMENTS: RULE_TEXT,
    names.ADDITIONALINFO: RULE_TEXT,
    names.ADDITIONALMETADATA: RULE_ADDITIONALMETADATA,
    names.ADDRESS: RULE_ADDRESS,
    names.ADMINISTRATIVEAREA: RULE_ANYNAME,
    names.ALLOW: RULE_ALLOW,
    names.ALTERNATEIDENTIFIER: RULE_ALTERNATEIDENTIFIER,
    names.ALTITUDEMAXIMUM: RULE_ANYSTRING,
    names.ALTITUDEMINIMUM: RULE_ANYSTRING,
    names.ALTITUDEUNITS: RULE_ALTITUDEUNITS,
    names.ANNOTATION: RULE_ANNOTATION,
    names.ASSOCIATEDPARTY: RULE_RESPONSIBLEPARTY_WITH_ROLE,
    names.ATTRIBUTE: RULE_ATTRIBUTE,
    names.ATTRIBUTEACCURACYEXPLANATION: RULE_ANYSTRING,
    names.ATTRIBUTEACCURACYREPORT: RULE_ANYSTRING,
    names.ATTRIBUTEACCURACYVALUE: RULE_ANYSTRING,
    names.ATTRIBUTEDEFINITION: RULE_ANYSTRING,
    names.ATTRIBUTELABEL: RULE_ANYSTRING,
    names.ATTRIBUTELIST: RULE_ATTRIBUTELIST,
    names.ATTRIBUTENAME: RULE_ANYSTRING,
    names.ATTRIBUTEORIENTATION: RULE_ANYSTRING,
    names.AUTHENTICATION: RULE_AUTHENTICATION,
    names.AWARD: RULE_AWARD,
    names.AWARDNUMBER: RULE_ANYNAME,
    names.AWARDURL: RULE_ANYNAME,
    names.BANDGAPBYTES: RULE_ANYSTRING,
    names.BANDROWBYTES: RULE_ANYSTRING,
    names.BEGINDATE: RULE_SINGLEDATETIME,
    names.BINARYRASTERFORMAT: RULE_BINARYRASTER_FORMAT,
    names.BOUNDINGALTITUDES: RULE_BOUNDINGALTITUDES,
    names.BOUNDINGCOORDINATES: RULE_BOUNDINGCOORDINATES,
    names.BOUNDS: RULE_BOUNDS,
    names.BYTEORDER: RULE_ANYSTRING,
    names.CALENDARDATE: RULE_YEARDATE,
    names.CASESENSITIVE: RULE_ANYSTRING,
    names.CHARACTERENCODING: RULE_ANYSTRING,
    names.CITATION: RULE_ANYSTRING,
    names.CITY: RULE_ANYNAME,
    names.CODE: RULE_ANYSTRING,
    names.CODEDEFINITION: RULE_CODEDEFINITION,
    names.CODEEXPLANATION: RULE_ANYSTRING,
    names.CODESETNAME: RULE_ANYSTRING,
    names.CODESETURL: RULE_ANYURI,
    names.COMMONNAME: RULE_ANYSTRING,
    names.COLLAPSEDELIMITERS: RULE_ANYSTRING,
    names.COMPLEX: RULE_COMPLEX,
    names.COMPRESSIONMETHOD: RULE_ANYSTRING,
    names.CONNECTION: RULE_ANYSTRING,
    names.CONTACT: RULE_RESPONSIBLEPARTY,
    names.COUNTRY: RULE_ANYNAME,
    names.COVERAGE: RULE_COVERAGE,
    names.CREATOR: RULE_RESPONSIBLEPARTY,
    names.CUSTOMUNIT: RULE_ANYSTRING,
    names.DATAFORMAT: RULE_DATAFORMAT,
    names.DATASET: RULE_DATASET,
    names.DATASOURCE: RULE_DATASOURCE,
    names.DATATABLE: RULE_DATATABLE,
    names.DATETIME: RULE_DATETIME,
    names.DATETIMEDOMAIN: RULE_DATETIMEDOMAIN,
    names.DATETIMEPRECISION: RULE_ANYSTRING,
    names.DEFINITION: RULE_ANYSTRING,
    names.DEFINITIONATTRIBUTEREFERENCE: RULE_ANYSTRING,
    names.DELIVERYPOINT: RULE_ANYNAME,
    names.DENY: RULE_DENY,
    names.DESCRIBES: RULE_ANYSTRING,
    names.DESCRIPTOR: RULE_DESCRIPTOR,
    names.DESCRIPTORVALUE: RULE_ANYSTRING,
    names.DESCRIPTION: RULE_TEXT,
    names.DISTRIBUTION: RULE_DISTRIBUTION,
    names.EASTBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_EW,
    names.ELECTRONICMAILADDRESS: RULE_ANYNAME,
    names.EML: RULE_EML,
    names.ENCODINGMETHOD: RULE_ANYSTRING,
    names.ENDDATE: RULE_SINGLEDATETIME,
    names.ENTITYCODELIST: RULE_ENTITYCODELIST,
    names.ENTITYDESCRIPTION: RULE_ANYSTRING,
    names.ENTITYNAME: RULE_ANYSTRING,
    names.ENTITYREFERENCE: RULE_ANYSTRING,
    names.ENTITYTYPE: RULE_ANYSTRING,
    names.ENUMERATEDDOMAIN: RULE_ENUMERATEDDOMAIN,
    names.EXTERNALCODESET: RULE_EXTERNALCODESET,
    names.EXTERNALLYDEFINEDFORMAT: RULE_EXTERNALLYDEFINIEDFORMAT,
    names.FIELDDELIMITER: RULE_ANYSTRING,
    names.FIELDSTARTCOLUMN: RULE_ANYSTRING,
    names.FIELDWIDTH: RULE_ANYSTRING,
    names.FORMATNAME: RULE_ANYSTRING,
    names.FORMATSTRING: RULE_ANYSTRING,
    names.FORMATVERSION: RULE_ANYSTRING,
    names.FUNDERIDENTIFIER: RULE_ANYNAME,
    names.FUNDERNAME: RULE_ANYNAME,
    names.FUNDING: RULE_TEXT,
    names.GENERALTAXONOMICCOVERAGE: RULE_ANYSTRING,
    names.GIVENNAME: RULE_ANYNAME,
    names.GEOGRAPHICCOVERAGE: RULE_GEOGRAPHICCOVERAGE,
    names.GEOGRAPHICDESCRIPTION: RULE_ANYSTRING,
    names.GETTINGSTARTED: RULE_TEXT,
    names.IDENTIFIER: RULE_ANYSTRING,
    names.INDIVIDUALNAME: RULE_INDIVIDUALNAME,
    names.INLINE: RULE_ANYSTRING,
    names.INSTRUMENTATION: RULE_ANYSTRING,
    names.INTELLECTUALRIGHTS: RULE_TEXT,
    names.INTERVAL: RULE_INTERVALRATIO,
    names.INTRODUCTION: RULE_TEXT,
    names.KEYWORD: RULE_KEYWORD,
    names.KEYWORDSET: RULE_KEYWORDSET,
    names.KEYWORDTHESAURUS: RULE_KEYWORDTHESAURUS,
    names.LANGUAGE: RULE_ANYNAME,
    names.LAYOUT: RULE_ANYSTRING,
    names.LICENSED: RULE_LICENSED,
    names.LICENSENAME: RULE_ANYSTRING,
    names.LINENUMBER: RULE_ANYINT,
    names.LITERALCHARACTER: RULE_ANYSTRING,
    names.MAINTENANCE: RULE_MAINTENANCE,
    names.MAINTENANCEUPDATEFREQUENCY: RULE_ANYSTRING,
    names.MARKDOWN: RULE_ANYSTRING,
    names.MAXIMUM: RULE_MINMAX,
    names.MAXRECORDLENGTH: RULE_ANYINT,
    names.MEASUREMENTSCALE: RULE_MEASUREMENTSCALE,
    names.MEDIUMNAME: RULE_ANYSTRING,
    names.MEDIUMDENSITY: RULE_ANYSTRING,
    names.MEDIUMDENSITYUNITS: RULE_ANYSTRING,
    names.MEDIUMVOLUME: RULE_ANYSTRING,
    names.MEDIUMFORMAT: RULE_ANYSTRING,
    names.MEDIUMNOTE: RULE_ANYSTRING,
    names.METADATA: RULE_METADATA,
    names.METADATAPROVIDER: RULE_RESPONSIBLEPARTY,
    names.METHODS: RULE_METHODS,
    names.METHODSTEP: RULE_METHODSTEP,
    names.MINIMUM: RULE_MINMAX,
    names.MISSINGVALUECODE: RULE_MISSINGVALUECODE,
    names.MULTIBAND: RULE_MULTIBAND,
    names.NBANDS: RULE_ANYINT,
    names.NBITS: RULE_ANYINT,
    names.NOMINAL: RULE_NOMINAL,
    names.NONNEGATIVEFLOAT: RULE_NONNEGATIVEFLOAT,
    names.NONNUMERICDOMAIN: RULE_NONNUMERICDOMAIN,
    names.NORTHBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_NS,
    names.NUMBEROFRECORDS: RULE_ANYSTRING,
    names.NUMBERTYPE: RULE_ANYSTRING,
    names.NUMERICDOMAIN: RULE_NUMERICDOMAIN,
    names.NUMFOOTERLINES: RULE_ANYINT,
    names.NUMHEADERLINES: RULE_ANYINT,
    names.NUMPHYSICALLINESPERRECORD: RULE_ANYINT,
    names.OBJECTNAME: RULE_ANYSTRING,
    names.OFFLINE: RULE_OFFLINE,
    names.ONLINE: RULE_ONLINE,
    names.ONLINEDESCRIPTION: RULE_ANYSTRING,
    names.ONLINEURL: RULE_ANYURI,
    names.ORDERATTRIBUTEREFERENCE: RULE_ANYSTRING,
    names.ORDINAL: RULE_ORDINAL,
    names.ORGANIZATIONNAME: RULE_ANYNAME,
    names.OTHERENTITY: RULE_OTHERENTITY,
    names.PARA: RULE_ANYSTRING,
    names.PATTERN: RULE_ANYSTRING,
    names.PERMISSION: RULE_PERMISSION,
    names.PERSONNEL: RULE_RESPONSIBLEPARTY_WITH_ROLE,
    names.PHONE: RULE_PHONE,
    names.PHYSICAL: RULE_PHYSICAL,
    names.PHYSICALLINEDELIMITER: RULE_ANYSTRING,
    names.POSITIONNAME: RULE_ANYNAME,
    names.POSTALCODE: RULE_ANYNAME,
    names.PRECISION: RULE_ANYSTRING,
    names.PRINCIPAL: RULE_PRINCIPAL,
    names.PROJECT: RULE_PROJECT,
    names.PROPERTYURI: RULE_PROPERTYURI,
    names.PUBDATE: RULE_YEARDATE,
    names.PUBLISHER: RULE_RESPONSIBLEPARTY,
    names.PUBPLACE: RULE_ANYSTRING,
    names.PURPOSE: RULE_TEXT,
    names.QUALITYCONTROL: RULE_QUALITYCONTROL,
    names.QUANTITATIVEATTRIBUTEACCURACYASSESSMENT: RULE_QUANTITATIVEATTRIBUTEACCURACYASSESSMENT,
    names.QUOTECHARACTER: RULE_ANYSTRING,
    names.RANGEOFDATES: RULE_RANGEOFDATES,
    names.RATIO: RULE_INTERVALRATIO,
    names.RECORDDELIMITER: RULE_ANYSTRING,
    names.REFERENCES: RULE_REFERENCES,
    names.RELATED_PROJECT: RULE_RELATEDPROJECT,
    names.ROLE: RULE_ROLE,
    names.ROWCOLUMNORIENTATION: RULE_ROWCOLUMN,
    names.SALUTATION: RULE_ANYNAME,
    names.SAMPLING: RULE_SAMPLING,
    names.SAMPLINGDESCRIPTION: RULE_TEXT,
    names.SECTION: RULE_SECTION,
    names.SERIES: RULE_ANYSTRING,
    names.SHORTNAME: RULE_ANYSTRING,
    names.SIMPLEDELIMITED: RULE_SIMPLEDELIMITED,
    names.SINGLEDATETIME: RULE_SINGLEDATETIME,
    names.SIZE: RULE_SIZE,
    names.SKIPBYTES: RULE_ANYSTRING,
    names.SOURCE: RULE_ANYSTRING,
    names.SOUTHBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_NS,
    names.STANDARDUNIT: RULE_ANYSTRING,
    names.STORAGETYPE: RULE_STORAGETYPE,
    names.STUDYAREADESCRIPTION: RULE_STUDYAREADESCRIPTION,
    names.STUDYEXTENT: RULE_STUDYEXTENT,
    names.SURNAME: RULE_ANYNAME,
    names.TAXONID: RULE_TAXONID,
    names.TAXONOMICCLASSIFICATION: RULE_TAXONOMICCLASSIFICATION,
    names.TAXONOMICCOVERAGE: RULE_TAXONOMICCOVERAGE,
    names.TAXONRANKNAME: RULE_ANYSTRING,
    names.TAXONRANKVALUE: RULE_ANYSTRING,
    names.TEMPORALCOVERAGE: RULE_TEMPORALCOVERAGE,
    names.TEXTDELIMITED: RULE_TEXTDELIMITED,
    names.TEXTDOMAIN: RULE_TEXTDOMAIN,
    names.TEXTFIXED: RULE_TEXTFIXED,
    names.TEXTFORMAT: RULE_TEXTFORMAT,
    names.TIME: RULE_TIME,
    names.TITLE: RULE_ANYNAME,
    names.TOTALROWBYTES: RULE_ANYSTRING,
    names.UNIT: RULE_UNIT,
    names.URL: RULE_URL,
    names.USERID: RULE_USERID,
    names.VALUE: RULE_VALUE,
    names.VALUEATTRIBUTEREFERENCE: RULE_ANYSTRING,
    names.VALUEURI: RULE_VALUEURI,
    names.WESTBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_EW,
}


def node_names():
    """
    Helper function.
    Returns a list of all known node names.
    """
    return list(node_mappings.keys())


def get_rule_name(node_name: str):
    """
    Helper function.
    For a given node name, return its corresponding rule name
    """
    return node_mappings.get(node_name)


def get_rule(node_name: str):
    """
    Helper function.
    For a given node name, instantiate its corresponding rule object and return it
    """
    rule_name = get_rule_name(node_name)
    return Rule(rule_name)

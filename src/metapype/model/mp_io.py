#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: mp_io

:Synopsis:
    Utilities for reading and writing a metapype model instance

:Author:
    servilla
    costa
    ide

:Created:
    6/15/18
"""
import json

import daiquiri
import xml.etree.ElementTree as ET

from metapype.model.node import Node


logger = daiquiri.getLogger("model_io: " + __name__)

space = "    "


def from_json(json_node: dict, parent: Node = None) -> Node:
    """
    Recursively traverse Python JSON and build a metapype model
    instance.

    Args:
        json_node: JSON converted to Python structure
        parent: parent node reference to child

    Returns:
        Node: Child node of decomposed and parsed JSON

    """
    # Get first inner JSON object from dict and discard outer
    _ = json_node.popitem()
    name = _[0]
    body = _[1]
    node = Node(name, id=body[0]["id"])

    if parent is not None:
        node.parent = parent

    attributes = body[1]["attributes"]
    if attributes is not None:
        for attribute in attributes:
            node.add_attribute(attribute, attributes[attribute])

    content = body[2]["content"]
    if content is not None:
        node.content = content

    children = body[3]["children"]
    for child in children:
        child_node = from_json(child, node)
        node.add_child(child_node)

    return node


def graph(node: Node, level: int) -> str:
    """
    Return a graphic tree structure of the model instance

    Args:
        node: Root node of the model instance
        level: Indention level

    Returns:
        str: String representation of the model instance.
    """
    indent = "  " * level
    name = f"{node.name}[{node.id}]"
    if node.content is not None:
        name += ": {}".format(node.content)
    if len(node.attributes) > 0:
        name += " " + str(node.attributes)
    if level == 0:
        print(name)
    else:
        print(indent + "\u2570\u2500 " + name)
    for child in node.children:
        graph(child, level + 1)


def objectify(node: Node) -> dict:
    """
    Converts a model instance into a single Python object instance in
    preparation for JSON

    Args:
        node:

    Returns:
        dict: serialized object of the model instance

    """
    j = {node.name: []}
    j[node.name].append({"id": node.id})
    j[node.name].append({"attributes": node.attributes})
    j[node.name].append({"content": node.content})
    children = []
    for child in node.children:
        children.append(objectify(child))
    j[node.name].append({"children": children})
    return j


def to_json(node: Node):
    """
    Converts a serialized object of the model instance to a JSON compliant
    string.

    Args:
        node: Root node of the model instance

    Returns:
        str: JSON representation of the model instance

    """
    j = objectify(node)
    return json.dumps(j)


def from_xml_element(xml_elem, metapype_node, metapype_parent):
    """
    Creates a metapype node corresponding to an xml element.

    Args:
        xml_elem:  the xml element.
        metapype_node:  the metapype_node corresponding to that xml element.
                        metapype_node == None, except at the root of the tree.
        metapype_parent:  the parent metapype_node for this node.
    """
    if metapype_node is None:  # Will be None except at the root
        metapype_node = Node(name=xml_elem.tag, parent=metapype_parent)
    # xml_element_lookup_by_node_id[metapype_node.id] = (metapype_node, xml_elem)
    for name, value in xml_elem.attrib.items():
        if "}" not in name:
            metapype_node.add_attribute(name, value)
    if xml_elem.text:
        metapype_node.content = xml_elem.text
    if metapype_parent is not None:
        metapype_parent.add_child(metapype_node)
    for xml_child in xml_elem:
        from_xml_element(xml_child, None, metapype_node)


def from_xml(xml_str: str) -> Node:
    """
    Given an xml document in string form, creates the corresponding metapype model.

    Args:
        xml_str:  the xml document as a string.

    Returns:
        The root metapype node of the metapype model tree.
    """
    # Create the XML tree from text
    xml_tree = ET.ElementTree(
        ET.fromstring(_clean_namespace_expansions(_clean_xml_whitespace(xml_str)))
    )
    # Get its root
    xml_root = xml_tree.getroot()
    # Create the root node for the metapype model
    metapype_root = Node(name=xml_root.tag, parent=None)
    # Recursively build the metapype model
    from_xml_element(xml_root, metapype_root, None)
    # Return the root of the metapype model
    return metapype_root


def _clean_xml_whitespace(xml_str: str) -> str:
    """
    Given an xml document in string form, remove whitespace that is non-significant.

    Parsing xml from pretty-printed text, we will get spaces and newlines
    between elements. If an xml element's text or tail is pure whitespace,
    we assume it's not meaningful. We can't just trim all leading and
    trailing whitespace, though, because whitespace in a mixed content element
    must be assumed to be there intentionally.

    Args:
        xml_str:  the xml document as a string.

    Returns:
        The xml document as a string, with non-significant whitespace removed.
    """
    tree = ET.ElementTree(ET.fromstring(xml_str))
    xml_root = tree.getroot()
    for xml_elem in ET.ElementTree(xml_root).iter():
        if xml_elem.text and xml_elem.text.isspace():
            xml_elem.text = None
        if xml_elem.tail and xml_elem.tail.isspace():
            xml_elem.tail = None
    return ET.tostring(xml_root)


def _clean_namespace_expansions(xml_str: str) -> str:
    """
    ElementTree expands namespaces, so for example
        eml:eml
    becomes
        {eml://ecoinformatics.org/eml-2.1.1}eml
    This function strips such namespace expansions from tags.

    Args:
        xml_str:  the xml document as a string.

    Returns:
        The xml document as a string, with namespace expansions removed.
    """
    tree = ET.ElementTree(ET.fromstring(xml_str))
    xml_root = tree.getroot()
    for el in ET.ElementTree(xml_root).iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
    return ET.tostring(xml_root)


############################################################
# Everything below is work in progress. Ignore for now.

# Assumes xml_element_lookup_by_node_id dict is present.
# I.e., is intended to be called from from_xml() (currently, at least).
# def check_model_completeness() -> bool:
#
#     for _, node_tuple in xml_element_lookup_by_node_id.items():
#         metapype_node, xml_node = node_tuple
#         if metapype_node.name == 'para':
#             print(f'metapype_node.content={metapype_node.content}')
#             print(ET.tostring(xml_node).decode('utf-8'))
#             print(xml_node.text)
#         if len(metapype_node.children) != len(xml_node.getchildren()):
#             print(f'Node {metapype_node.name} is incomplete')
#             return False
#     return True


# def get_xml_as_string(node_id: str) -> str:
#     # try:
#     return ET.tostring(xml_element_lookup_by_node_id[node_id]).decode('utf-8')

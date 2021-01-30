#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: metapype_io

:Synopsis:
    Metapype import and export utilities

:Author:
    servilla

:Created:
    12/30/20
"""
import json

import daiquiri
from lxml import etree

from metapype.model.node import Node


logger = daiquiri.getLogger(__name__)


def _from_dict(node: dict, parent: Node = None) -> Node:
    """
    Build a Metapype model from a dict.

    Args:
        node: dict representation of a Metapype model
        parent: parent node of current node (root node will be None)

    Returns:
        Node: current node of Metapype model

    """
    name, body = node.popitem()
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
        child_node = _from_dict(child, node)
        node.add_child(child_node)

    return node


def _serialize(node: Node) -> dict:
    """
    Serializes a Metapype model instance into a Python dict

    Args:
        node: Metapype node to serialize

    Returns:
        dict: Metapype model instance dictionary

    """
    j = {node.name: []}
    j[node.name].append({"id": node.id})
    j[node.name].append({"attributes": node.attributes})
    j[node.name].append({"content": node.content})
    children = []
    for child in node.children:
        children.append(_serialize(child))
    j[node.name].append({"children": children})
    return j


def from_json(node: str) -> Node:
    """
    Build a Metapype model instance from JSON.

    Args:
        node: JSON Metapype model

    Returns:
        Node: current node of Metapype model

    """
    m = json.loads(node)
    return _from_dict(m)


def to_json(node: Node):
    """
    Converts a Metapype model instance to JSON

    Args:
        node: node of the model instance

    Returns:
        str: JSON of Metapype model instance

    """
    j = _serialize(node)
    return json.dumps(j, indent=2)


def graph(node: Node, level: int = 0) -> str:
    """
    Return a graphic tree structure of the model instance

    Args:
        node: Root node of the model instance
        level: Indention level

    Returns:
        str: String representation of the model instance.
    """
    indent = "  " * level
    n = f"{node.name}[{node.id}]" if node.prefix is None else f"{node.prefix}:{node.name}[{node.id}]"
    if node.content is not None:
        n += f": {node.content}"
    if len(node.attributes) > 0:
        n += f" {str(node.attributes)}"
    if level == 0:
        n += "\n"
    else:
        n = indent + "\u2570\u2500 " + n + "\n"
    for child in node.children:
        n += graph(child, level + 1)
    return n


def from_xml(xml: str, clean: bool = True, ) -> Node:
    _ = xml.encode("utf-8")
    root = etree.fromstring(_)
    return _process_element(root, clean)


def _process_element(e, clean) -> Node:
    tag = e.tag[e.tag.find("}") + 1:]  # Remove any prepended namespace
    node = Node(tag)
    if clean:
        node.content = None if e.text.strip() == '' else e.text.strip()
    else:
        node.content = e.text
    for name, value in e.attrib.items():
        if "{" not in name:
            node.add_attribute(name, value)
    node.nspmap = e.nsmap
    node.prefix = e.prefix
    for _ in e:
        node.add_child(_process_element(_, clean))
    for child in node.children:
        child.parent = node
    return node

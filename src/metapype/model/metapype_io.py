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
import re

import daiquiri
from lxml import etree
from xml.sax.saxutils import escape

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

    nsmap = body[1]["nsmap"]
    if nsmap is not None:
        for nsp in nsmap:
            node.add_namespace(nsp, nsmap[nsp])

    prefix = body[2]["prefix"]
    if prefix is not None:
        node.prefix = prefix

    attributes = body[3]["attributes"]
    if attributes is not None:
        for attribute in attributes:
            node.add_attribute(attribute, attributes[attribute])

    extras = body[4]["extras"]
    if extras is not None:
        for extra in extras:
            node.add_extras(extra, extras[extra])

    content = body[5]["content"]
    if content is not None:
        node.content = content

    tail = body[6]["tail"]
    if tail is not None:
        node.tail = tail

    children = body[7]["children"]
    for child in children:
        child_node = _from_dict(child, node)
        node.add_child(child_node)

    return node


def _format_extras(name: str, nsmap: dict) -> str:
    match = re.match(r"^\{(.*)\}(.*)$", name)
    nsname = name
    if match is not None:
        uri = match.group(1)
        target = match.group(2)
        for k, v in nsmap.items():
            if uri == v:
                nsname = f"{k}:{target}"
    return nsname


def _nsp_unique(child_nsmap: dict, parent_nsmap: dict) -> dict:
    nsmap = dict()
    for child_nsp in child_nsmap:
        if child_nsp in parent_nsmap:
            if child_nsmap[child_nsp] != parent_nsmap[child_nsp]:
                nsmap[child_nsp] = child_nsmap[child_nsp]
        else:
            nsmap[child_nsp] = child_nsmap[child_nsp]
    return nsmap


def _process_element(e, clean) -> Node:
    """
    Process an lxml etree element into a Metapype node. If the clean attribute is true, then
    remove leading and trailing whitespace from the element content.

    Args:
        e: lxml etree element
        clean: boolean to clean leading and trailing whitespace

    Returns: Node

    """
    tag = e.tag[e.tag.find("}") + 1:]  # Remove any prepended namespace

    node = Node(tag)
    node.nsmap = e.nsmap
    node.prefix = e.prefix

    if clean:
        if e.text is not None:
            node.content = None if e.text.strip() == '' else e.text.strip()
    else:
        node.content = e.text

    for name, value in e.attrib.items():
        if "{" not in name:
            node.add_attribute(name, value)
        else:
            nsname = _format_extras(name, node.nsmap)
            node.add_extras(nsname, value)

    for _ in e:
        if _.tag is not etree.Comment:
            node.add_child(_process_element(_, clean))
    for child in node.children:
        child.parent = node
        if child.nsmap == node.nsmap:
            child.nsmap = node.nsmap  # Map to single instance of nsmap
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
    j[node.name].append({"nsmap": node.nsmap})
    j[node.name].append({"prefix": node.prefix})
    j[node.name].append({"attributes": node.attributes})
    j[node.name].append({"extras": node.extras})
    j[node.name].append({"content": node.content})
    j[node.name].append({"tail": node.tail})
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


def to_json(node: Node, indent: int = None) -> str:
    """
    Converts a Metapype model instance to JSON

    Args:
        indent:
        node: node of the model instance

    Returns:
        str: JSON of Metapype model instance

    """
    j = _serialize(node)
    return json.dumps(j, indent=indent)


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
    g = f"{node.name}[{node.id}]" if node.prefix is None else f"{node.prefix}:{node.name}[{node.id}]"
    if node.content is not None:
        g += f": {node.content}"
    if len(node.attributes) > 0:
        g += f" {str(node.attributes)}"
    if level == 0:
        g += "\n"
    else:
        g = indent + "\u2570\u2500 " + g + "\n"
    for child in node.children:
        g += graph(child, level + 1)
    return g


def from_xml(xml: str, clean: bool = True, ) -> Node:
    """
    Convert an XML model into a Metapype model. If clean is true, remove leading and trailing whitespace
    from the element content.

    Args:
        xml: XML string to be converted
        clean: boolean to clean leading and trailing whitespace

    Returns: the root Node of the Metapype model

    """
    root = _process_element(etree.fromstring(xml.encode("utf-8")), clean)
    return root


def to_xml(node: Node, parent: Node = None, level: int = 0) -> str:
    xml = ""
    indent = "  " * level

    tag = f"{node.name}" if node.prefix is None else f"{node.prefix}:{node.name}"

    attributes = ""
    if len(node.attributes) > 0:
        attributes += " ".join([f"{k}=\"{v}\"" for k, v in node.attributes.items()])

    if parent is None:
        attributes += " " + " ".join([f"xmlns:{k}=\"{v}\"" for k, v in node.nsmap.items()])
    elif node.nsmap != parent.nsmap:
        nsmap = _nsp_unique(node.nsmap, parent.nsmap)
        attributes += " " + " ".join([f"xmlns:{k}=\"{v}\"" for k, v in nsmap.items()])

    if len(node.extras) > 0:
        attributes += " " + " ".join([f"{k}=\"{v}\"" for k, v in node.extras.items()])

    if len(attributes) > 0:
        attributes = " " + attributes

    if node.content is not None:
        content = escape(node.content)
        open_tag = f"{indent}<{tag}{attributes}>{content}"
        close_tag = f"</{tag}>\n"
    else:
        open_tag = f"{indent}<{tag}{attributes}>\n"
        close_tag = f"{indent}</{tag}>\n"

    xml += open_tag
    for child in node.children:
        xml += to_xml(child, node, level + 1)
    xml += close_tag
    return xml

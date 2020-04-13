#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: mp_io

:Synopsis:
    Utilities for reading and writing a metapype model instance

:Author:
    servilla

:Created:
    6/15/18
"""
import json

import daiquiri

from metapype.model.node import Node

logger = daiquiri.getLogger('model_io: ' + __name__)

space = '    '


def from_json(json_node: dict, parent: Node = None) -> Node:
    '''
    Recursively traverse Python JSON and build a metapype model
    instance.

    Args:
        json_node: JSON converted to Python structure
        parent: parent node reference to child

    Returns:
        Node: Child node of decomposed and parsed JSON

    '''
    # Get first inner JSON object from dict and discard outer
    _ = json_node.popitem()
    name = _[0]
    body = _[1]
    node = Node(name, id=body[0]['id'])

    if parent is not None:
        node.parent = parent

    attributes = body[1]['attributes']
    if attributes is not None:
        for attribute in attributes:
            node.add_attribute(attribute, attributes[attribute])

    content = body[2]['content']
    if content is not None:
        node.content = content

    children = body[3]['children']
    for child in children:
        child_node = from_json(child, node)
        node.add_child(child_node)

    return node


def graph(node: Node, level: int) -> str:
    '''
    Return a graphic tree structure of the model instance

    Args:
        node: Root node of the model instance
        level: Indention level

    Returns:
        str: String representation of the model instance.
    '''
    indent = '  ' * level
    name = f'{node.name}[{node.id}]'
    if node.content is not None:
        name += ': {}'.format(node.content)
    if len(node.attributes) > 0:
        name += ' ' + str(node.attributes)
    if level == 0:
        print(name)
    else:
        print(indent + '\u2570\u2500 ' + name)
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
    j[node.name].append({'id': node.id})
    j[node.name].append({'attributes': node.attributes})
    j[node.name].append({'content': node.content})
    children = []
    for child in node.children:
        children.append(objectify(child))
    j[node.name].append({'children': children})
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
    return json.dumps(j, indent=2)

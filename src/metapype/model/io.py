#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: io

:Synopsis:
    Utilities for reading and writing a model instance

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
    node = Node(name)

    if parent is not None:
        node.parent = parent

    attributes = body[0]['attributes']
    if attributes is not None:
        for attribute in attributes:
            node.add_attribute(attribute, attributes[attribute])

    content = body[1]['content']
    if content is not None:
        node.content = content

    children = body[2]['children']
    for child in children:
        if child is not None:
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
    name = node.name
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


def to_json(node: Node, level: int = 0, comma: str = '') -> str:
    '''
    Converts a model instance from the root node to a JSON compliant
    string.

    Args:
        node: Root node of the model instance
        level: Indention level
        comma: String representation of a comma if condition dictates

    Returns:
        str: JSON representation of the model instance.

    '''
    json = ''
    name = node.name
    if level == 0:
        indent = ''
    else:
        indent = space * level

    open_tag = '{"' + name + '":[\n'
    json += indent + open_tag

    attributes = '{"attributes":null},'
    if len(node.attributes) > 0:
        # Creates comma delimited list of attributes
        _ = '{' + ','.join(
            ['"' + key + '":"' + node.attributes[key] + '"' for key in
             node.attributes]) + '}'
        attributes = attributes.replace('null', _)
    json += indent + space + attributes + '\n'

    content = '{"content":null},'
    if node.content is not None:
        _ = '"' + node.content + '"'
        content = content.replace('null', _)
    json += indent + space + content + '\n'

    children = '{"children":[null]}'
    if len(node.children) > 0:
        _ = ''
        for child in node.children:
            # Special formatting necessary for first and last child to
            # cleanly represent indention and commas to be JSON
            # compliant
            newline = ''
            if child is node.children[0]:
                newline = '\n'
            if child is node.children[-1]:
                _ += newline + to_json(child, level + 2, comma='')
            else:
                _ += newline + to_json(child, level + 2, comma=',')
        children = children.replace('null]}', _)
        json += indent + space + children
        json += indent + space + ']}\n'
    else:
        json += indent + space + children + '\n'

    if level == 0:
        close_tag = indent + ']}'
    else:
        close_tag = indent + ']}' + comma + '\n'
    json += close_tag

    return json


def main():
    return 0


if __name__ == "__main__":
    main()

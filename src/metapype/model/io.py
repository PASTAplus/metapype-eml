#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: io

:Synopsis:

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


def from_json(json_node: dict, parent: Node=None) -> Node:
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
    indent = '  ' * level
    type = node.rank
    if node.content is not None:
        type += ': {}'.format(node.content)
    if len(node.attributes) > 0:
        type += ' ' + str(node.attributes)
    if level == 0:
        print(type)
    else:
        print(indent + '\u2570\u2500 ' + type)
    for child in node.children:
       graph(child, level + 1)


def to_json(node: Node, level: int=0, comma: str='') -> str:
    json = ''
    type = node.rank
    if level == 0:
        indent = ''
    else:
        indent = space * level

    open_tag = '{"' + type + '":[\n'
    json += indent + open_tag

    attributes = '{"attributes":null},'
    if len(node.attributes) > 0:
        _ = '{' + ','.join(['"' + key + '":"' + node.attributes[key] + '"' for key in node.attributes]) + '}'
        attributes = attributes.replace('null', _)
    json += indent + space + attributes + '\n'

    content = '{"content":null},'
    if node.content is not None:
        _ = '"' + node.content + '"'
        content = content.replace('null',_)
    json += indent + space + content + '\n'

    children = '{"children":[null]}'
    if  len(node.children) > 0:
        _ = ''
        for child in node.children:
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

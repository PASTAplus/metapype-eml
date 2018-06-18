#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: node

:Synopsis:

:Author:
    servilla

:Created:
    5/15/18
"""
import uuid

import daiquiri


logger = daiquiri.getLogger('node.py: ' + __name__)


class Node(object):

    def __init__(self, name: str, parent=None, content: str=None):
        self._node_id = uuid.uuid4().hex
        self._name = name
        self._parent = parent
        self._content = content
        self._attributes = {} # Attribute key/value pairs
        self._children = [] # Children node objects in add order

    @property
    def node_id(self):
        return self._node_id

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    def add_attribute(self, name, value):
        self._attributes[name] = value

    def remove_attribute(self, name):
        del self._attributes[name]

    def attribute_value(self, name):
        return self._attributes[name]

    def list_attributes(self):
        return list(self._attributes.keys())

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    def add_child(self, child):
        self._children.append(child)

    def remove_child(self, child):
        self._children.remove(child)


def main():
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: node

:Synopsis:

:Author:
    servilla

:Created:
    5/15/18
"""
import copy
import uuid

import daiquiri


logger = daiquiri.getLogger('node.py: ' + __name__)


node_store = {}


class Node(object):
    '''
    Model node class representation.

    Attributes:
        name: Required string of metadata element name being modeled
        parent: Optional parent node
        content: Optional string content
    '''

    @staticmethod
    def get_node_instance(id: str):
        '''
        Returns the instance of a node from its identifier
        Args:
            id: Str

        Returns:
            Node
        '''
        return node_store[id]

    def __init__(self, name: str, parent=None, content: str=None):
        self._id = str(uuid.uuid1())
        self._name = name
        self._parent = parent
        self._content = content
        self._attributes = {} # AttTortugaribute key/value pairs
        self._children = [] # Children node objects in add order

        # Add node to store
        node_store[self._id] = self

    def add_attribute(self, name, value):
        self._attributes[name] = value

    def add_child(self, child, index=None ):
        '''
        Adds a child object into the children list at either the end of
        the list or at the index location if specified.
        Args:
            child: Node
            index: Int

        Returns:
            None
        '''
        if index is None:
            self._children.append(child)
        else:
            self._children.insert(index, child)

    def attribute_value(self, name):
        if name in self._attributes:
            return self._attributes[name]
        return None

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes

    def child_index(self, child):
        '''
        Returns the child index value of where it is found in the children
        list

        Args:
            child: Node

        Returns:
            Int index value

        '''
        index = None
        try:
            index = self._children.index(child)
        except ValueError as e:
            logger.error(e)
        return index

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    def copy(self):
        '''
        Returns a deep copy (including all children) of the node.

        Returns:
            Node

        '''
        return copy.deepcopy(self)

    def find_all_children(self, child_name):
        '''
        Returns a list of all children that matches the child_name, or returns
        an empty list if there are no matches.

        Args:
            child_name: Child name to be matched

        Returns:
            List
        '''
        children = []
        for child_node in self._children:
            if child_node.name == child_name:
                children.append(child_node)
        return children

    @property
    def id(self):
        '''
        Returns the unique identifier of the node instance
        Returns:
            Str
        '''
        return self._id

    @id.setter
    def id(self, id):
        del node_store[self._id]
        self._id = id
        node_store[self._id] = self

    def list_attributes(self):
        return list(self._attributes.keys())

    def find_child(self, child_name):
        '''
        Recursively searches for the first child that matches the 
        child_name and returns it, or returns None if there is no 
        match.

        Args:
            child_name: Child name to be matched

        Returns
            Node or None
        '''
        child = None
        for child_node in self._children:
            if child_node.name == child_name:
                child = child_node
            else:       
                child = child_node.find_child(child_name=child_name)
            if child:
                break
        return child

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def remove_attribute(self, name):
        del self._attributes[name]

    def remove_child(self, child):
        '''
        Removes the child object from the children list.
        Args:
            child: Node

        Returns:
            None
        '''
        self._children.remove(child)

    def replace_child(self, old_child, new_child):
        '''
        Replaces the old child with a new child
        Args:
            old_child: Node
            new_child: Node

        Returns:
            None

        '''
        new_child.parent = self
        self._children[self._children.index(old_child)] = new_child


def main():
    return 0


if __name__ == "__main__":
    main()

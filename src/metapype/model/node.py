#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: node

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    5/15/18
"""
import copy
from enum import Enum
import uuid

import daiquiri


logger = daiquiri.getLogger("node.py: " + __name__)


class Shift(Enum):
    LEFT = 0
    RIGHT = 1


class Node(object):
    """
    Model node class representation.

    Attributes:
        name: Required string of metadata element name being modeled
        id: Optional node identifier
        parent: Optional parent node
        content: Optional string content
    """

    def __init__(
        self, name: str, id: str = None, parent=None, content: str = None
    ):
        self._id = str(uuid.uuid1()) if id is None else id
        self._name = name
        self._parent = parent
        self._content = content
        self._attributes = {}
        self._children = []
        Node.set_node_instance(self)

    store = {}

    @classmethod
    def delete_node_instance(cls, id: str, children: bool = True):
        """
        Removes the node instance from the store; if children set to True, then
        remove all children recursively.

        Args:
            id: str node identifier
            children: bool

        Returns:
            None
        """
        if children:
            node = cls.get_node_instance(id)
            for child in node.children:
                cls.delete_node_instance(child.id)
        del Node.store[id]

    @classmethod
    def get_node_instance(cls, id: str):
        """
        Returns the instance of a node from its identifier

        Args:
            id: Str

        Returns:
            Node
        """
        return cls.store.get(id, None)

    @classmethod
    def set_node_instance(cls, node):
        """
        Sets the node instance in the node store

        Args:
            node:

        Returns:
            None
        """
        cls.store[node._id] = node

    def add_attribute(self, name, value):
        self._attributes[name] = value

    def add_child(self, child, index=None):
        """
        Adds a child object into the children list at either the end of
        the list or at the index location if specified.
        Args:
            child: Node
            index: Int

        Returns:
            None
        """
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
        """
        Returns the child index value of where it is found in the children
        list

        Args:
            child: Node

        Returns:
            Int index value

        """
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
        """
        Returns a deep copy (including all children) of the node.

        Returns:
            Node

        """
        return copy.deepcopy(self)

    def find_all_children(self, child_name):
        """
        Returns a list of all children that matches the child_name, or returns
        an empty list if there are no matches.

        Args:
            child_name: Child name to be matched

        Returns:
            List
        """
        return [
            child_node
            for child_node in self._children
            if child_node.name == child_name
        ]

    def find_all_descendants(self, child_name, descendants):
        """
        Generates a list of all descendants that match the child_name, or
        an empty list if there are no matches.

        Args:
            child_name: Child name to be matched
            descendants: List object to be filled with descendant nodes
        """
        for child_node in self._children:
            if child_node.name == child_name:
                descendants.append(child_node)
            child_node.find_all_descendants(child_name, descendants)

    @property
    def id(self):
        """
        Returns the unique identifier of the node instance
        Returns:
            Str
        """
        return self._id

    def list_attributes(self):
        return list(self._attributes.keys())

    def find_descendant(self, descendant_name):
        """
        Recursively searches for the first descendant that matches the
        descendant_name and returns it, or returns None if there is no
        match.

        Args:
            descendant_name: Descendant node name to be matched

        Returns
            Node or None
        """
        descendant = None
        for descendant_node in self._children:
            if descendant_node.name == descendant_name:
                descendant = descendant_node
            else:
                descendant = descendant_node.find_descendant(descendant_name=descendant_name)
            if descendant:
                break
        return descendant

    def find_child(self, child_name):
        """
        Searches for the first child that matches the
        child_name and returns it, or returns None if there is no
        match. Does not search beyond the first generation of descendants.

        Args:
            child_name: Child name to be matched

        Returns
            Node or None
        """
        for child_node in self._children:
            if child_node.name == child_name:
                return child_node
        return None

    def find_single_node_by_path(self, path: list):
        """
        Search down a descendant lineage, using the names in the path provided. Return
        the first node found that satisfies the path.

        To give an example based on EML 2.2, if self is the EML node, then the path
        [names.DATASET, names.CREATOR, names.USERID] will find the userID node of the
        first creator of the dataset, if any. Note that there may be many userID nodes in the
        tree (for creators, metadataProviders, associatedParties, project personnel, etc.,
        so just doing a recursive search for a userID node isn't likely to return the
        desired result.

        Note that this method only returns a single node (or None, if none is found). To
        get all nodes satisfying the path, use find_all_nodes_by_path.

        Args:
            path: List of node names defining the descendant lineage to be found.

        Returns
            Node or None
        """
        if not path or len(path) == 0:
            return None
        current_node = self
        for name in path:
            if not current_node:
                return None
            current_node = current_node.find_child(name)
        return current_node

    def find_all_nodes_by_path(self, path: list):
        """
        Search down a descendant lineage, using the names in the path provided. Return
        a list of nodes that satisfy the path.

        To give an example based on EML 2.2, if self is the EML node, then the path
        [names.DATASET, names.CREATOR, names.USERID] will return a list consisting of
        the userIDs for all of the creators of the dataset, if any.

        Note that this method returns a list of nodes (or None, if none is found). To
        get a single node satisfying the path, use find_single_node_by_path. In cases
        where it is known that at most one node can satisfy the path, getting a single
        node is more convenient than getting a list.

        Args:
            path: List of node names defining the descendant lineages to be found.

        Returns
            List of Nodes, which may be empty
        """
        if not path or len(path) == 0:
            return []
        current_list = [self]
        for name in path:
            if not current_list:
                return []
            next_generation = []
            for node in current_list:
                next_generation.extend(node.find_all_children(name))
            current_list = next_generation
        return current_list

    def get_ancestry(self):
        ancestry = []
        node = self
        while True:
            ancestry.insert(0, node)
            node = node.parent
            if not node:
                break
        return ancestry

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def remove_attribute(self, name):
        del self._attributes[name]

    def remove_child(self, child):
        """
        Removes the child object from the children list

        Args:
            child: Node

        Returns:
            None
        """
        self._children.remove(child)

    def remove_children(self):
        self._children = []

    def replace_child(self, old_child, new_child):
        """
        Replaces the old child with a new child

        Args:
            old_child: Node
            new_child: Node

        Returns:
            None
        """
        if new_child.name != old_child.name:
            msg = f'Child type "{new_child.name}" and "{old_child.name}" mismatch'
            raise ValueError(msg)

        new_child.parent = self
        self._children[self._children.index(old_child)] = new_child
        Node.delete_node_instance(id=old_child.id)

    def shift(self, child, direction: Shift):
        """
        Shifts a child's position either left or right of its current position
        or not at all of already at local edge

        Args:
            child: Node to be swapped
            direction: shift (LEFT, RIGHT)

        Returns:
            int of new index location or same if no change
        """
        index = self._children.index(child)
        name = self._children[index].name
        if direction == Shift.RIGHT:
            for sib_index in range(index + 1, len(self._children)):
                if self._children[sib_index].name == name:
                    self.children[index], self.children[sib_index] = (
                        self.children[sib_index],
                        self.children[index],
                    )
                    index = sib_index
                    break
        elif direction == Shift.LEFT:
            for sib_index in range(index - 1, -1, -1):
                if self._children[sib_index].name == name:
                    self.children[index], self.children[sib_index] = (
                        self.children[sib_index],
                        self.children[index],
                    )
                    index = sib_index
                    break
        else:
            msg = "Expected direction to be either Shift.RIGHT or Shift.LEFT"
            raise ValueError(msg)

        return index


def main():
    return 0


if __name__ == "__main__":
    main()

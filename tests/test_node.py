#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_node

:Synopsis:

:Author:
    servilla
  
:Created:
    6/18/18
"""
import os
import sys
import unittest

import daiquiri

from metapype.eml2_1_1 import names
from metapype.eml2_1_1 import validate
from metapype.model.node import Node
from metapype.model.node import tree_hash


sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_node: ' + __name__)


class TestNode(unittest.TestCase):

    def setUp(self):
        self.node = Node(names.EML)

    def tearDown(self):
        self.node = None

    def test_add_attribute(self):
        self.node.add_attribute('packageId', 'test.1.1')
        self.node.add_attribute('system', 'metapype')
        attributes = self.node.attributes
        for attribute in attributes:
            self.assertTrue(attribute in ['packageId', 'system'])
            value = attributes[attribute]
            self.assertTrue(value in ['test.1.1', 'metapype'])

    def test_add_child(self):
        child_1 = Node(names.ACCESS)
        self.node.add_child(child_1)
        children = self.node.children
        self.assertIs(child_1, children[0])
        child_2 = Node(names.DATASET)
        self.node.add_child(child_2, 0)
        self.assertIs(child_2, children[0])

    def test_copy(self):
        node = Node(names.GIVENNAME)
        node.content = 'Chase'
        validate.node(node)
        node_copy = node.copy()
        validate.node(node_copy)

    def test_create_node(self):
        self.assertIsNotNone(self.node)

    def test_find_child(self):
        access = Node(names.ACCESS)
        self.node.add_child(access)
        child = self.node.find_child(names.ACCESS)
        self.assertIs(access, child)

        allow = Node(names.ALLOW)
        access.add_child(allow)
        grandchild = self.node.find_child(names.ALLOW)
        self.assertIs(grandchild, allow)

        permission = Node(names.PERMISSION)
        allow.add_child(permission)
        great_grandchild = self.node.find_child(names.PERMISSION)
        self.assertIs(great_grandchild, permission)

        child = self.node.find_child('nonesuch')
        self.assertIs(child, None)
        
    def test_remove_child(self):
        access = Node(names.ACCESS)
        self.node.add_child(access)
        child = self.node.children[0]
        self.assertIs(access,child)
        self.node.remove_child(child, 0)
        self.assertListEqual([], self.node.children)

    def test_tree_hash(self):
        access = Node(names.ACCESS)
        access_from_tree = tree_hash[access.id]
        self.assertIs(access, access_from_tree)

if __name__ == '__main__':
    unittest.main()
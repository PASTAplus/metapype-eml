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

import metapype.eml2_1_1.names as names
from metapype.model.node import Node


sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_node: ' + __name__)


class TestNode(unittest.TestCase):

    def setUp(self):
        self.node = Node(names.EML)

    def tearDown(self):
        self.node = None

    def test_create_node(self):
        self.assertIsNotNone(self.node)

    def test_add_attribute(self):
        self.node.add_attribute('packageId', 'test.1.1')
        self.node.add_attribute('system', 'metapype')
        attributes = self.node.attributes
        for attribute in attributes:
            self.assertTrue(attribute in ['packageId', 'system'])
            value = attributes[attribute]
            self.assertTrue(value in ['test.1.1', 'metapype'])

    def test_add_child(self):
        access = Node(names.ACCESS)
        self.node.add_child(access)
        children = self.node.children
        for child in children:
            self.assertIs(access, child)

    def test_remove_child(self):
        access = Node(names.ACCESS)
        self.node.add_child(access)
        child = self.node.children[0]
        self.assertIs(access,child)
        self.node.remove_child(child)
        self.assertListEqual([], self.node.children)

    def test_find_child(self):
        access = Node(names.ACCESS)
        self.node.add_child(access)
        child = self.node.find_child('access')
        self.assertIs(access, child)
        self.node.remove_child(child)
        self.assertListEqual([], self.node.children)
        child = self.node.find_child('nonesuch')
        self.assertIs(child, None)

if __name__ == '__main__':
    unittest.main()
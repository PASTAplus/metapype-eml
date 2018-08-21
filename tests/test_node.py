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
from metapype.model.node import Shift


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
        self.node.remove_child(child)
        self.assertNotIn(access, self.node.children)

    def test_replace_child(self):
        individual_name = Node(names.INDIVIDUALNAME)
        sur_name_1 = Node(names.SURNAME, parent=individual_name)
        sur_name_1.content = 'Gaucho'
        individual_name.add_child(sur_name_1)
        sur_name_2 = Node(names.SURNAME, parent=individual_name)
        sur_name_2.content = 'Carroll'
        self.assertIn(sur_name_1, individual_name.children)
        self.assertNotIn(sur_name_2, individual_name.children)
        individual_name.replace_child(old_child=sur_name_1, new_child=sur_name_2)
        self.assertIn(sur_name_2, individual_name.children)
        self.assertNotIn(sur_name_1, individual_name.children)

    def test_shift(self):
        individual_name_1 = Node(names.INDIVIDUALNAME)
        individual_name_2 = Node(names.INDIVIDUALNAME)
        individual_name_3 = Node(names.INDIVIDUALNAME)
        organization_name = Node(names.ORGANIZATIONNAME)
        position_name = Node(names.POSITIONNAME)

        # Test shift right
        contact = Node(names.CONTACT)
        contact.add_child(child=organization_name)
        contact.add_child(child=individual_name_1)
        contact.add_child(child=individual_name_2)
        contact.add_child(child=individual_name_3)
        contact.add_child(child=position_name)
        shift_index = contact.shift(child=individual_name_2, direction=Shift.RIGHT)
        self.assertEqual(shift_index, 3)
        self.assertIs(contact.children[3], individual_name_2)

        # Test shift left
        contact = Node(names.CONTACT)
        contact.add_child(child=organization_name)
        contact.add_child(child=individual_name_1)
        contact.add_child(child=individual_name_2)
        contact.add_child(child=individual_name_3)
        contact.add_child(child=position_name)
        shift_index = contact.shift(child=individual_name_2, direction=Shift.LEFT)
        self.assertEqual(shift_index, 1)
        self.assertIs(contact.children[1], individual_name_2)

        # Test shift on edge right
        contact = Node(names.CONTACT)
        contact.add_child(child=organization_name)
        contact.add_child(child=individual_name_1)
        contact.add_child(child=individual_name_2)
        contact.add_child(child=individual_name_3)
        contact.add_child(child=position_name)
        index = contact.children.index(individual_name_3)
        shift_index = contact.shift(child=individual_name_3, direction=Shift.RIGHT)
        self.assertEqual(index, shift_index)

        # Test shift on edge left
        contact = Node(names.CONTACT)
        contact.add_child(child=organization_name)
        contact.add_child(child=individual_name_1)
        contact.add_child(child=individual_name_2)
        contact.add_child(child=individual_name_3)
        contact.add_child(child=position_name)
        index = contact.children.index(individual_name_1)
        shift_index = contact.shift(child=individual_name_1, direction=Shift.LEFT)
        self.assertEqual(index, shift_index)

        # Test hard shift on edge right
        contact.add_child(child=organization_name)
        contact.add_child(child=individual_name_1)
        contact.add_child(child=individual_name_2)
        contact.add_child(child=individual_name_3)
        index = contact.children.index(individual_name_3)
        shift_index = contact.shift(child=individual_name_3, direction=Shift.RIGHT)
        self.assertEqual(index, shift_index)

        # Test hard shift on edge left
        contact.add_child(child=organization_name)
        contact.add_child(child=individual_name_1)
        contact.add_child(child=individual_name_2)
        contact.add_child(child=individual_name_3)
        index = contact.children.index(individual_name_1)
        shift_index = contact.shift(child=individual_name_1, direction=Shift.LEFT)
        self.assertEqual(index, shift_index)


    def test_get_node(self):
        access = Node(names.ACCESS)
        node = Node.get_node_instance(access.id)
        self.assertIs(access, node)

    def test_delete_node(self):
        eml = Node(names.EML)
        eml.add_attribute('packageId', 'edi.23.1')
        eml.add_attribute('system', 'metapype')
        access = Node(names.ACCESS, parent=eml)
        access.add_attribute('authSystem', 'pasta')
        access.add_attribute('order', 'allowFirst')
        eml.add_child(access)
        allow = Node(names.ALLOW, parent=access)
        access.add_child(allow)
        principal = Node(names.PRINCIPAL, parent=allow)
        principal.content = 'uid=gaucho,o=EDI,dc=edirepository,dc=org'
        allow.add_child(principal)
        permission = Node(names.PERMISSION, parent=allow)
        permission.content = 'all'
        allow.add_child(permission)
        node = Node.get_node_instance(principal.id)
        self.assertIs(principal, node)
        Node.delete_node_instance(eml.id)
        self.assertNotIn(principal.id, Node.store)

    def test_delete_node_no_children(self):
        eml = Node(names.EML)
        eml.add_attribute('packageId', 'edi.23.1')
        eml.add_attribute('system', 'metapype')
        access = Node(names.ACCESS, parent=eml)
        access.add_attribute('authSystem', 'pasta')
        access.add_attribute('order', 'allowFirst')
        eml.add_child(access)
        allow = Node(names.ALLOW, parent=access)
        access.add_child(allow)
        principal = Node(names.PRINCIPAL, parent=allow)
        principal.content = 'uid=gaucho,o=EDI,dc=edirepository,dc=org'
        allow.add_child(principal)
        permission = Node(names.PERMISSION, parent=allow)
        permission.content = 'all'
        allow.add_child(permission)
        node = Node.get_node_instance(principal.id)
        self.assertIs(principal, node)
        Node.delete_node_instance(eml.id, children=False)
        self.assertIn(principal.id, Node.store)

if __name__ == '__main__':
    unittest.main()
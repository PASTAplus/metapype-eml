#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_eml_2_1_1

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
import metapype.eml2_1_1.validate as validate
from metapype.model.node import Node


sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_eml_2_1_1: ' + __name__)


class TestEml_2_1_1(unittest.TestCase):

    def setUp(self):
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

        dataset = Node(names.DATASET, parent=eml)
        eml.add_child(dataset)

        title = Node(names.TITLE, parent=dataset)
        title.content = 'Green sea turtle counts: Tortuga Island 20017'
        dataset.add_child(title)

        creator = Node(names.CREATOR, parent=dataset)
        dataset.add_child(creator)

        individualName_creator = Node(names.INDIVIDUALNAME, parent=creator)
        creator.add_child(individualName_creator)

        surName_creator = Node(names.SURNAME, parent=individualName_creator)
        surName_creator.content = 'Gaucho'
        individualName_creator.add_child(surName_creator)

        contact = Node(names.CONTACT, parent=dataset)
        dataset.add_child(contact)

        individualName_contact = Node(names.INDIVIDUALNAME, parent=contact)
        contact.add_child(individualName_contact)

        surName_contact = Node(names.SURNAME, parent=individualName_contact)
        surName_contact.content = 'Gaucho'
        individualName_contact.add_child(surName_contact)

        self.node = eml


    def tearDown(self):
        self.node = None


    def test_validate_node(self):
        self.assertIsNone(validate.node(self.node))

    def test_validate_tree(self):
        self.assertIsNone(validate.tree(self.node))


def main():
    return 0


if __name__ == "__main__":
    main()

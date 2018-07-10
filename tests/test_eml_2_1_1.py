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
import metapype.eml2_1_1.rules as rules
import metapype.eml2_1_1.validate as validate
from metapype.model.node import Node


sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_eml_2_1_1: ' + __name__)


class TestEml_2_1_1(unittest.TestCase):

    def setUp(self):
        self.eml = Node(names.EML)
        self.eml.add_attribute('packageId', 'edi.23.1')
        self.eml.add_attribute('system', 'metapype')

        self.access = Node(names.ACCESS, parent=self.eml)
        self.access.add_attribute('authSystem', 'pasta')
        self.access.add_attribute('order', 'allowFirst')
        self.eml.add_child(self.access)

        self.allow = Node(names.ALLOW, parent=self.access)
        self.access.add_child(self.allow)

        self.principal_allow = Node(names.PRINCIPAL, parent=self.allow)
        self.principal_allow.content = 'uid=gaucho,o=EDI,dc=edirepository,dc=org'
        self.allow.add_child(self.principal_allow)

        self.permission_allow = Node(names.PERMISSION, parent=self.allow)
        self.permission_allow.content = 'all'
        self.allow.add_child(self.permission_allow)
        
        self.deny = Node(names.DENY, parent=self.access)
        self.access.add_child(self.deny)

        self.principal_deny = Node(names.PRINCIPAL, parent=self.deny)
        self.principal_deny.content = 'public'
        self.deny.add_child(self.principal_deny)

        self.permission_deny = Node(names.PERMISSION, parent=self.deny)
        self.permission_deny.content = 'write'
        self.deny.add_child(self.permission_deny)

        self.dataset = Node(names.DATASET, parent=self.eml)
        self.eml.add_child(self.dataset)

        self.title = Node(names.TITLE, parent=self.dataset)
        self.title.content = 'Green sea turtle counts: Tortuga Island 20017'
        self.dataset.add_child(self.title)

        self.creator = Node(names.CREATOR, parent=self.dataset)
        self.dataset.add_child(self.creator)

        self.individualName_creator = Node(names.INDIVIDUALNAME, parent=self.creator)
        self.creator.add_child(self.individualName_creator)

        self.surName_creator = Node(names.SURNAME, parent=self.individualName_creator)
        self.surName_creator.content = 'Gaucho'
        self.individualName_creator.add_child(self.surName_creator)

        self.value = Node(names.VALUE, parent=self.surName_creator)
        self.value.add_attribute('xml:lang', 'en')
        self.value.content = 'Gaucho'
        self.surName_creator.add_child(self.value)

        self.contact = Node(names.CONTACT, parent=self.dataset)
        self.dataset.add_child(self.contact)

        self.individualName_contact = Node(names.INDIVIDUALNAME, parent=self.contact)
        self.contact.add_child(self.individualName_contact)

        self.surName_contact = Node(names.SURNAME, parent=self.individualName_contact)
        self.surName_contact.content = 'Gaucho'
        self.individualName_contact.add_child(self.surName_contact)

        self.additional_metadata = Node(names.ADDITIONALMETADATA, parent=self.eml)
        self.eml.add_child(self.additional_metadata)
        self.metadata = Node(names.METADATA, parent=self.additional_metadata)
        self.metadata.content = '<tag>TAG</tag>'
        self.additional_metadata.add_child(self.metadata)

        self.node = self.eml


    def tearDown(self):
        self.node = None

    def test_validate_node(self):
        self.assertIsNone(validate.node(self.node))

    def test_validate_tree(self):
        self.assertIsNone(validate.tree(self.node))

    def test_accessRule(self):
        r = rules.dispatcher[names.ACCESS]
        self.assertIsNone(r.validate_rule(self.access))

    def test_additionalMetadataRule(self):
        r = rules.dispatcher[names.ADDITIONALMETADATA]
        self.assertIsNone(r.validate_rule(self.additional_metadata))

    def test_allowRule(self):
        r = rules.dispatcher[names.ALLOW]
        self.assertIsNone(r.validate_rule(self.allow))

    def test_anyNameRule(self):
        r = rules.dispatcher[names.SURNAME]
        self.assertIsNone(r.validate_rule(self.surName_contact))
        self.assertIsNone(r.validate_rule(self.title))

    def test_datasetRule(self):
        r = rules.dispatcher[names.DATASET]
        self.assertIsNone(r.validate_rule(self.dataset))

    def test_denyRule(self):
        r = rules.dispatcher[names.DENY]
        self.assertIsNone(r.validate_rule(self.deny))

    def test_emlRule(self):
        r = rules.dispatcher[names.EML]
        self.assertIsNone(r.validate_rule(self.eml))

    def test_individualNameRule(self):
        r = rules.dispatcher[names.INDIVIDUALNAME]
        self.assertIsNone(r.validate_rule(self.individualName_contact))
        self.assertIsNone(r.validate_rule(self.individualName_creator))

    def test_metadataRule(self):
        r = rules.dispatcher[names.METADATA]
        self.assertIsNone(r.validate_rule(self.metadata))

    def test_permissionRule(self):
        r = rules.dispatcher[names.PERMISSION]
        self.assertIsNone(r.validate_rule(self.permission_allow))
        self.assertIsNone(r.validate_rule(self.permission_deny))

    def test_principalRule(self):
        r = rules.dispatcher[names.PRINCIPAL]
        self.assertIsNone(r.validate_rule(self.principal_allow))
        self.assertIsNone(r.validate_rule(self.principal_deny))

    def test_responsiblePartyRule(self):
        r = rules.dispatcher[names.CREATOR]
        self.assertIsNone(r.validate_rule(self.creator))
        self.assertIsNone(r.validate_rule(self.contact))

    def test_valuRule(self):
        r = rules.dispatcher[names.VALUE]
        self.assertIsNone(r.validate_rule(self.value))


def main():
    return 0


if __name__ == "__main__":
    main()

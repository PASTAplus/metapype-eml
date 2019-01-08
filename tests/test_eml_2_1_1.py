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

from metapype.eml2_1_1.exceptions import MetapypeRuleError
import metapype.eml2_1_1.names as names
import metapype.eml2_1_1.rule as rule
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

        self.salutation_creator = Node(names.SALUTATION, parent=self.individualName_creator)
        self.salutation_creator.content = 'Mr.'
        self.individualName_creator.add_child(self.salutation_creator)

        self.given_name_creator = Node(names.GIVENNAME, parent=self.individualName_creator)
        self.given_name_creator.content = 'Chase'
        self.individualName_creator.add_child(self.given_name_creator)

        self.surName_creator = Node(names.SURNAME, parent=self.individualName_creator)
        self.surName_creator.content = 'Gaucho'
        self.individualName_creator.add_child(self.surName_creator)

        self.value = Node(names.VALUE, parent=self.surName_creator)
        self.value.add_attribute('lang', 'en')
        self.value.content = 'Gaucho'
        self.surName_creator.add_child(self.value)

        self.address = Node(names.ADDRESS, parent=self.creator)
        self.creator.add_child(self.address)

        self.delivery_point_1 = Node(names.DELIVERYPOINT, parent=self.address)
        self.delivery_point_1.content = '100 Maple St'
        self.address.add_child(self.delivery_point_1)

        self.delivery_point_2 = Node(names.DELIVERYPOINT, parent=self.address)
        self.delivery_point_2.content = 'Apt. 10-B'
        self.address.add_child(self.delivery_point_2)

        self.city = Node(names.CITY, parent=self.address)
        self.city.content = "Gotham City"
        self.address.add_child(self.city)

        self.administrative_area = Node(names.ADMINISTRATIVEAREA, parent=self.address)
        self.administrative_area.content = "New York"
        self.address.add_child(self.administrative_area)

        self.postal_code = Node(names.POSTALCODE, parent=self.address)
        self.postal_code.content = '11111'
        self.address.add_child(self.postal_code)

        self.country = Node(names.COUNTRY, parent=self.address)
        self.country.content = 'USA'
        self.address.add_child(self.country)

        self.phone = Node(names.PHONE, parent=self.creator)
        self.phone.content = '555-555-5555'
        self.phone.add_attribute('phonetype', 'voice')
        self.creator.add_child(self.phone)

        self.electronic_mail_address = Node(names.ELECTRONICMAILADDRESS, parent=self.creator)
        self.electronic_mail_address.content = 'cgaucho@somecollege.edu'
        self.creator.add_child(self.electronic_mail_address)

        self.online_url = Node(names.ONLINEURL, parent=self.creator)
        self.online_url.content = 'https://www.somecollege.edu/people/cgaucho'
        self.creator.add_child(self.online_url)

        self.user_id = Node(names.USERID, parent=self.creator)
        self.user_id.content = 'uid=jgaucho,o=EDI,dc=edirepository,dc=org'
        self.user_id.add_attribute('directory', 'ldap:///ldap.edirepository.org/dc=edirepository,dc=org')
        self.creator.add_child(self.user_id)

        self.pubdate = Node(names.PUBDATE, parent=self.dataset)
        self.pubdate.content = '2018'
        self.dataset.add_child(self.pubdate)

        self.abstract = Node(names.ABSTRACT, parent=self.dataset)
        self.abstract.add_attribute('lang', 'en')
        self.section = Node(names.SECTION, parent=self.abstract)
        self.abstract.add_child(self.section)
        self.section.content = "abstract section"
        self.para = Node(names.PARA, parent=self.abstract)
        self.abstract.add_child(self.para)
        self.para.content = "para section"
        self.dataset.add_child(self.abstract)

        self.keyword_set = Node(names.KEYWORDSET, parent=self.dataset)
        self.dataset.add_child(self.keyword_set)

        self.keyword_1 = Node(names.KEYWORD, parent=self.keyword_set)
        self.keyword_1.content = 'phytoplankton ecology'
        self.keyword_set.add_child(self.keyword_1)

        self.keyword_2 = Node(names.KEYWORD, parent=self.keyword_set)
        self.keyword_2.add_attribute('keywordType', 'place')
        self.keyword_2.content = 'lake'
        self.keyword_set.add_child(self.keyword_2)

        self.keyword_thesaurus = Node(names.KEYWORDTHESAURUS, parent=self.keyword_set)
        self.keyword_thesaurus.content = 'IRIS keyword thesaurus'
        self.keyword_set.add_child(self.keyword_thesaurus)

        self.coverage = Node(names.COVERAGE, parent=self.dataset)
        self.dataset.add_child(self.coverage)

        self.taxonomic_coverage = Node(names.TAXONOMICCOVERAGE, parent=self.coverage)
        self.coverage.add_child(self.taxonomic_coverage)
        self.general_taxonomic_coverage = Node(names.GENERALTAXONOMICCOVERAGE, 
                                               parent=self.taxonomic_coverage)
        self.taxonomic_coverage.add_child(self.general_taxonomic_coverage)
        self.general_taxonomic_coverage.content = "All vascular plants were \
            identified to family or species, mosses and lichens were \
            identified as moss or lichen."
    
        self.taxonomic_classification_genus = Node(names.TAXONOMICCLASSIFICATION, 
                                                   parent=self.taxonomic_coverage)
        self.taxonomic_coverage.add_child(self.taxonomic_classification_genus)

        self.taxon_rank_name_genus = Node(names.TAXONRANKNAME, 
                                          parent=self.taxonomic_classification_genus)
        self.taxonomic_classification_genus.add_child(self.taxon_rank_name_genus)
        self.taxon_rank_name_genus.content = "Genus"

        self.taxon_rank_value_genus = Node(names.TAXONRANKVALUE, parent=self.taxonomic_classification_genus)
        self.taxonomic_classification_genus.add_child(self.taxon_rank_value_genus)
        self.taxon_rank_value_genus.content = "Escherichia"

        self.taxonomic_classification_species = Node(names.TAXONOMICCLASSIFICATION, 
                                                     parent=self.taxonomic_classification_genus)
        self.taxonomic_classification_genus.add_child(self.taxonomic_classification_species)

        self.taxon_rank_name_species = Node(names.TAXONRANKNAME, parent=self.taxonomic_classification_species)
        self.taxonomic_classification_species.add_child(self.taxon_rank_name_species)
        self.taxon_rank_name_species.content = "Species"

        self.taxon_rank_value_species = Node(names.TAXONRANKVALUE, parent=self.taxonomic_classification_species)
        self.taxonomic_classification_species.add_child(self.taxon_rank_value_species)
        self.taxon_rank_value_species.content = "coli"

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

    def test_get_rule(self):
        r = rule.get_rule(names.ACCESS)
        self.assertEquals(r.name, rule.RULE_ACCESS)
        self.assertEquals(type(r.attributes), type(dict()))
        self.assertEquals(type(r.children), type(list()))
        self.assertEquals(type(r.content_rules), type(list()))
        self.assertEquals(type(r.content_enum), type(list()))

    def test_rule_validation(self):
        r = rule.get_rule(names.ACCESS)
        self.assertIsNone(r.validate_rule(self.access))

    def test_empty_content(self):
        self.access.content = 'some content'
        r = rule.get_rule(names.ACCESS)
        self.assertRaises(MetapypeRuleError, r.validate_rule, self.access)

    def test_non_empty_content(self):
        self.principal_allow.content = None
        r = rule.get_rule(names.PRINCIPAL)
        self.assertRaises(MetapypeRuleError, r.validate_rule,self.principal_allow)

    def test_permissions_content(self):
        self.permission_allow.content = 'some permission'
        r = rule.get_rule(names.PERMISSION)
        self.assertRaises(MetapypeRuleError, r.validate_rule, self.permission_allow)

    def test_str_content(self):
        self.permission_allow.content = 1
        r = rule.get_rule(names.PERMISSION)
        self.assertRaises(MetapypeRuleError, r.validate_rule, self.permission_allow)

    def test_is_allowed_child(self):
        r = rule.get_rule(names.EML)
        allowed = r.is_allowed_child(names.ACCESS)
        self.assertTrue(allowed)
        allowed = r.is_allowed_child(names.INDIVIDUALNAME)
        self.assertFalse(allowed)

    def test_child_insert_index(self):
        eml = Node(names.EML)
        access = Node(names.ACCESS, parent=eml)
        eml.add_child(access)
        additional_metadata = Node(names.ADDITIONALMETADATA, parent=eml)
        eml.add_child(additional_metadata)
        r = rule.get_rule(names.EML)
        dataset = Node(names.DATASET, parent=eml)
        index = r.child_insert_index(eml, dataset)
        eml.add_child(dataset, index=index)
        self.assertIsInstance(index, int)

    def test_is_yeardate(self):
        good_vals = ['1980', '2020', '1980-01-01', '2020-12-31']
        bad_vals = ['nineteen-eighty', 2020, '01-01-1980', '2020-31-12']
        for good_val in good_vals:
            self.assertTrue(rule.Rule.is_yeardate(good_val))
        for bad_val in bad_vals:
            self.assertFalse(rule.Rule.is_yeardate(bad_val))

    # Test whether a value is, or can be converted to, a float
    def test_is_float(self):
        good_vals = ['34.555', '-120.0000', '34', -120]
        bad_vals = ['nineteen-eighty', 'foo', '01-01-1980', '-0000-']
        for good_val in good_vals:
            self.assertTrue(rule.Rule.is_float(good_val))
        for bad_val in bad_vals:
            self.assertFalse(rule.Rule.is_float(bad_val))


def main():
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_eml

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    6/18/18
"""
import daiquiri
import pytest
import os

from metapype.config import Config
from metapype.eml.exceptions import MetapypeRuleError
import metapype.eml.names as names
import metapype.eml.rule as rule
import metapype.eml.validate as validate
import metapype.model.metapype_io as metapype_io
from metapype.model.node import Node

logger = daiquiri.getLogger("test_eml: " + __name__)


@pytest.fixture()
def node():
    eml = Node(names.EML)
    eml.add_attribute("packageId", "edi.23.1")
    eml.add_attribute("system", "metapype")

    access = Node(names.ACCESS, parent=eml)
    access.add_attribute("authSystem", "pasta")
    access.add_attribute("order", "allowFirst")
    eml.add_child(access)

    allow = Node(names.ALLOW, parent=access)
    access.add_child(allow)

    principal_allow = Node(names.PRINCIPAL, parent=allow)
    principal_allow.content = "uid=gaucho,o=EDI,dc=edirepository,dc=org"
    allow.add_child(principal_allow)

    permission_allow = Node(names.PERMISSION, parent=allow)
    permission_allow.content = "all"
    allow.add_child(permission_allow)

    deny = Node(names.DENY, parent=access)
    access.add_child(deny)

    principal_deny = Node(names.PRINCIPAL, parent=deny)
    principal_deny.content = "public"
    deny.add_child(principal_deny)

    permission_deny = Node(names.PERMISSION, parent=deny)
    permission_deny.content = "write"
    deny.add_child(permission_deny)

    dataset = Node(names.DATASET, parent=eml)
    eml.add_child(dataset)

    title = Node(names.TITLE, parent=dataset)
    title.content = "Green sea turtle counts: Tortuga Island 20017"
    dataset.add_child(title)

    creator = Node(names.CREATOR, parent=dataset)
    dataset.add_child(creator)

    individualName_creator = Node(names.INDIVIDUALNAME, parent=creator)
    creator.add_child(individualName_creator)

    salutation_creator = Node(names.SALUTATION, parent=individualName_creator)
    salutation_creator.content = "Mr."
    individualName_creator.add_child(salutation_creator)

    given_name_creator = Node(names.GIVENNAME, parent=individualName_creator)
    given_name_creator.content = "Chase"
    individualName_creator.add_child(given_name_creator)

    surName_creator = Node(names.SURNAME, parent=individualName_creator)
    surName_creator.content = "Gaucho"
    individualName_creator.add_child(surName_creator)

    value = Node(names.VALUE, parent=surName_creator)
    value.add_attribute("lang", "en")
    value.content = "Gaucho"
    surName_creator.add_child(value)

    address = Node(names.ADDRESS, parent=creator)
    creator.add_child(address)

    delivery_point_1 = Node(names.DELIVERYPOINT, parent=address)
    delivery_point_1.content = "100 Maple St"
    address.add_child(delivery_point_1)

    delivery_point_2 = Node(names.DELIVERYPOINT, parent=address)
    delivery_point_2.content = "Apt. 10-B"
    address.add_child(delivery_point_2)

    city = Node(names.CITY, parent=address)
    city.content = "Gotham City"
    address.add_child(city)

    administrative_area = Node(names.ADMINISTRATIVEAREA, parent=address)
    administrative_area.content = "New York"
    address.add_child(administrative_area)

    postal_code = Node(names.POSTALCODE, parent=address)
    postal_code.content = "11111"
    address.add_child(postal_code)

    country = Node(names.COUNTRY, parent=address)
    country.content = "USA"
    address.add_child(country)

    phone = Node(names.PHONE, parent=creator)
    phone.content = "555-555-5555"
    phone.add_attribute("phonetype", "voice")
    creator.add_child(phone)

    electronic_mail_address = Node(names.ELECTRONICMAILADDRESS, parent=creator)
    electronic_mail_address.content = "cgaucho@somecollege.edu"
    creator.add_child(electronic_mail_address)

    online_url = Node(names.ONLINEURL, parent=creator)
    online_url.content = "https://www.somecollege.edu/people/cgaucho"
    creator.add_child(online_url)

    user_id = Node(names.USERID, parent=creator)
    user_id.content = "uid=jgaucho,o=EDI,dc=edirepository,dc=org"
    user_id.add_attribute(
        "directory", "ldap:///ldap.edirepository.org/dc=edirepository," "dc=org"
    )
    creator.add_child(user_id)

    pubdate = Node(names.PUBDATE, parent=dataset)
    pubdate.content = "2018"
    dataset.add_child(pubdate)

    abstract = Node(names.ABSTRACT, parent=dataset)
    abstract.add_attribute("lang", "en")
    section = Node(names.SECTION, parent=abstract)
    abstract.add_child(section)
    para = Node(names.PARA, parent=abstract)
    section.add_child(para)
    para.content = "para section"
    dataset.add_child(abstract)

    keyword_set = Node(names.KEYWORDSET, parent=dataset)
    dataset.add_child(keyword_set)

    keyword_1 = Node(names.KEYWORD, parent=keyword_set)
    keyword_1.content = "phytoplankton ecology"
    keyword_set.add_child(keyword_1)

    keyword_2 = Node(names.KEYWORD, parent=keyword_set)
    keyword_2.add_attribute("keywordType", "place")
    keyword_2.content = "lake"
    keyword_set.add_child(keyword_2)

    keyword_thesaurus = Node(names.KEYWORDTHESAURUS, parent=keyword_set)
    keyword_thesaurus.content = "IRIS keyword thesaurus"
    keyword_set.add_child(keyword_thesaurus)

    coverage = Node(names.COVERAGE, parent=dataset)
    dataset.add_child(coverage)

    taxonomic_coverage = Node(names.TAXONOMICCOVERAGE, parent=coverage)
    coverage.add_child(taxonomic_coverage)
    general_taxonomic_coverage = Node(
        names.GENERALTAXONOMICCOVERAGE, parent=taxonomic_coverage
    )
    taxonomic_coverage.add_child(general_taxonomic_coverage)
    general_taxonomic_coverage.content = "All vascular plants were \
        identified to family or species, mosses and lichens were \
        identified as moss or lichen."

    taxonomic_classification_genus = Node(
        names.TAXONOMICCLASSIFICATION, parent=taxonomic_coverage
    )
    taxonomic_coverage.add_child(taxonomic_classification_genus)

    taxon_rank_name_genus = Node(
        names.TAXONRANKNAME, parent=taxonomic_classification_genus
    )
    taxonomic_classification_genus.add_child(taxon_rank_name_genus)
    taxon_rank_name_genus.content = "Genus"

    taxon_rank_value_genus = Node(
        names.TAXONRANKVALUE, parent=taxonomic_classification_genus
    )
    taxonomic_classification_genus.add_child(taxon_rank_value_genus)
    taxon_rank_value_genus.content = "Escherichia"

    taxonomic_classification_species = Node(
        names.TAXONOMICCLASSIFICATION, parent=taxonomic_classification_genus
    )
    taxonomic_classification_genus.add_child(taxonomic_classification_species)

    taxon_rank_name_species = Node(
        names.TAXONRANKNAME, parent=taxonomic_classification_species
    )
    taxonomic_classification_species.add_child(taxon_rank_name_species)
    taxon_rank_name_species.content = "Species"

    taxon_rank_value_species = Node(
        names.TAXONRANKVALUE, parent=taxonomic_classification_species
    )
    taxonomic_classification_species.add_child(taxon_rank_value_species)
    taxon_rank_value_species.content = "coli"

    contact = Node(names.CONTACT, parent=dataset)
    dataset.add_child(contact)

    individualName_contact = Node(names.INDIVIDUALNAME, parent=contact)
    contact.add_child(individualName_contact)

    surName_contact = Node(names.SURNAME, parent=individualName_contact)
    surName_contact.content = "Gaucho"
    individualName_contact.add_child(surName_contact)

    additional_metadata = Node(names.ADDITIONALMETADATA, parent=eml)
    eml.add_child(additional_metadata)
    metadata = Node(names.METADATA, parent=additional_metadata)
    fictitious = Node("fictitious")
    fictitious.content = "<tag>more fictitious content</tag>"
    metadata.add_child(fictitious)
    additional_metadata.add_child(metadata)
    return eml


def test_validate_node(node):
    assert validate.node(node) is None


def test_validate_tree(node):
    assert validate.tree(node) is None


def test_get_rule():
    r = rule.get_rule(names.ACCESS)
    assert r.name == rule.RULE_ACCESS
    assert isinstance(r.attributes, dict)
    assert isinstance(r.children, list)
    assert isinstance(r.content_rules, list)
    assert isinstance(r.content_enum, list)


def test_rule_validation(node):
    r = rule.get_rule(names.ACCESS)
    access = node.find_child("access")
    assert r.validate_rule(access) is None


def test_empty_content(node):
    access = node.find_child(names.ACCESS)
    access.content = "some content"
    r = rule.get_rule(names.ACCESS)
    with pytest.raises(MetapypeRuleError):
        r.validate_rule(access)


def test_non_empty_content(node):
    principal_allow = node.find_descendant(names.PRINCIPAL)
    principal_allow.content = None
    r = rule.get_rule(names.PRINCIPAL)
    with pytest.raises(MetapypeRuleError):
        r.validate_rule(principal_allow)


def test_permissions_content(node):
    permission_allow = node.find_descendant(names.PERMISSION)
    permission_allow.content = "some permission"
    r = rule.get_rule(names.PERMISSION)
    with pytest.raises(MetapypeRuleError):
        r.validate_rule(permission_allow)


def test_str_content(node):
    permission_allow = node.find_descendant(names.PERMISSION)
    permission_allow.content = 1
    r = rule.get_rule(names.PERMISSION)
    with pytest.raises(MetapypeRuleError):
        r.validate_rule(permission_allow)


def test_is_allowed_child():
    r = rule.get_rule(names.EML)
    allowed = r.is_allowed_child(names.ACCESS)
    assert allowed
    allowed = r.is_allowed_child(names.INDIVIDUALNAME)
    assert not allowed


def test_child_insert_index():
    eml = Node(names.EML)
    eml.add_attribute("packageId", "edi.23.1")
    eml.add_attribute("system", "metapype")
    access = Node(names.ACCESS, parent=eml)
    eml.add_child(access)
    additional_metadata = Node(names.ADDITIONALMETADATA, parent=eml)
    eml.add_child(additional_metadata)
    r = rule.get_rule(names.EML)
    dataset = Node(names.DATASET, parent=eml)
    index = r.child_insert_index(eml, dataset)
    eml.add_child(dataset, index=index)
    validate.node(eml)


def test_is_yeardate():
    good_vals = ["1980", "2020", "1980-01-01", "2020-12-31"]
    bad_vals = ["nineteen-eighty", 2020, "01-01-1980", "2020-31-12"]
    for good_val in good_vals:
        assert rule.Rule.is_yeardate(good_val)
    for bad_val in bad_vals:
        assert not rule.Rule.is_yeardate(bad_val)


def test_is_time():
    good_vals = ["12:00", "12:00:00", "12:00:00.000", "12:00:00.000-06:00"]
    bad_vals = ["2:00", "12:00:0", "12:00:00.00", "12:00:00.000-06"]
    for good_val in good_vals:
        assert rule.Rule.is_time(good_val)
    for bad_val in bad_vals:
        assert not rule.Rule.is_time(bad_val)


# Test whether a value is, or can be converted to, a float
def test_is_float():
    good_vals = ["34.555", "-120.0000", "34", -120]
    bad_vals = ["nineteen-eighty", "foo", "01-01-1980", "-0000-"]
    for good_val in good_vals:
        assert rule.Rule.is_float(good_val)
    for bad_val in bad_vals:
        assert not rule.Rule.is_float(bad_val)


def test_validate_prune():
    if "TEST_DATA" in os.environ:
        xml_path = os.environ["TEST_DATA"]
    else:
        xml_path = Config.TEST_DATA

    with open(f"{xml_path}/eml.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    assert isinstance(eml, Node)
    referencePublication = Node("referencePublication")
    usageCitation = Node("usageCitation")
    dataset = eml.find_single_node_by_path([names.DATASET])
    dataset.add_child(referencePublication)
    dataset.add_child(usageCitation)
    errs = list()
    validate.tree(eml, errs)
    assert len(errs) > 0
    validate.prune(eml)
    errs = list()
    validate.tree(eml, errs)
    assert len(errs) == 0


def test_is_uri():
    good_uri = "http://purl.obolibrary.org/obo/IAO_0000136"
    assert rule.Rule.is_uri(good_uri)
    # Bad scheme (requires http or https)
    bad_uri = "htp://purl.obolibrary.org/obo/IAO_0000136"
    assert not rule.Rule.is_uri(bad_uri)
    # Missing path
    bad_uri = "http://purl.obolibrary.org"
    assert not rule.Rule.is_uri(bad_uri)
    # Missing host and path
    bad_uri = "http://"
    assert not rule.Rule.is_uri(bad_uri)


def test_validate_annotation():
    annotation = Node(names.ANNOTATION)
    property_uri = Node(names.PROPERTYURI)
    property_uri.content = "http://purl.obolibrary.org/obo/IAO_0000136"
    property_uri.add_attribute("label", "some property label")
    annotation.add_child(property_uri)
    value_uri = Node(names.VALUEURI)
    value_uri.content = "http://purl.obolibrary.org/obo/IAO_0000136"
    value_uri.add_attribute("label", "some value label")
    annotation.add_child(value_uri)
    validate.tree(annotation)


def test_responsible_party():
    creator = Node(names.CREATOR)
    creator.add_attribute("id", "creator")
    creator.add_namespace("eml", "https://eml.ecoinformatics.org/eml-2.2.0")
    individual_name = Node(names.INDIVIDUALNAME)
    creator.add_child(individual_name)
    given_name = Node(names.GIVENNAME, content="Chase")
    given_name.add_attribute("lang", "Spanish")
    individual_name.add_child(given_name)
    sur_name = Node(names.SURNAME, content="Gaucho")
    sur_name.add_attribute("lang", "Spanish")
    individual_name.add_child(sur_name)
    individual_name = Node(names.INDIVIDUALNAME)
    creator.add_child(individual_name)
    given_name = Node(names.GIVENNAME, content="Cactus")
    individual_name.add_child(given_name)
    sur_name = Node(names.SURNAME, content="Jack")
    individual_name.add_child(sur_name)
    phone = Node(names.PHONE, content="999-999-9999")
    creator.add_child(phone)
    validate.tree(creator)


def test_references():
    creator = Node(names.CREATOR)
    references = Node(names.REFERENCES)
    creator.add_child(references)
    validate.node(creator)


def test_get_children():
    r = rule.Rule("responsiblePartyRule")
    assert len(r._named_children) == 9

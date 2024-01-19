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

import tests
from metapype.eml.exceptions import MetapypeRuleError, ChildNotAllowedError
import metapype.eml.names as names
import metapype.eml.rule as rule
from metapype.eml.rule import Rule
import metapype.eml.validate as validate
import metapype.model.metapype_io as metapype_io
from metapype.model.node import Node
from metapype.eml.validation_errors import ValidationError

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


def test_validate_bad_tree(node):
    dataset: Node = node.find_child(names.DATASET)
    creator: Node = dataset.find_child(names.CREATOR)
    dataset.remove_child(creator)
    errs = list()
    assert validate.tree(node, errs) is None
    assert len(errs) != 0


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
    # Part 1
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
    # Part 2
    r = rule.get_rule(names.ASSOCIATEDPARTY)
    associated_party = Node(names.ASSOCIATEDPARTY)
    organization_name = Node(names.ORGANIZATIONNAME)
    index = r.child_insert_index(associated_party, organization_name)
    associated_party.add_child(organization_name, index)
    address = Node(names.ADDRESS)
    associated_party.add_child(address)
    online_url = Node(names.ONLINEURL)
    associated_party.add_child(online_url)
    position_name = Node(names.POSITIONNAME)
    index = r.child_insert_index(associated_party, position_name)
    associated_party.add_child(position_name, index)
    role = Node(names.ROLE)
    index = r.child_insert_index(associated_party, role)
    associated_party.add_child(role, index)
    validate.node(associated_party)


def test_is_yeardate():
    good_vals = ["1980", "2020", "1980-01-01", "2020-12-31"]
    bad_vals = ["nineteen-eighty", 2020, "01-01-1980", "2020-31-12"]
    for good_val in good_vals:
        assert rule.Rule.is_yeardate(good_val)
    for bad_val in bad_vals:
        assert not rule.Rule.is_yeardate(bad_val)


def test_is_time():
    good_vals = ["12:00", "12:00:00", "12:00:00.000", "12:00:00.000-06:00"]
    bad_vals = ["2:00", "12:00:0"]
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
        xml_path = tests.test_data_path

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


def test_responsible_party_with_role():
    personnel = Node(names.PERSONNEL)
    personnel.add_attribute("id", "personnel")
    personnel.add_namespace("eml", "https://eml.ecoinformatics.org/eml-2.2.0")
    individual_name = Node(names.INDIVIDUALNAME)
    personnel.add_child(individual_name)
    given_name = Node(names.GIVENNAME, content="Chase")
    given_name.add_attribute("lang", "Spanish")
    individual_name.add_child(given_name)
    sur_name = Node(names.SURNAME, content="Gaucho")
    sur_name.add_attribute("lang", "Spanish")
    individual_name.add_child(sur_name)
    individual_name = Node(names.INDIVIDUALNAME)
    personnel.add_child(individual_name)
    given_name = Node(names.GIVENNAME, content="Cactus")
    individual_name.add_child(given_name)
    sur_name = Node(names.SURNAME, content="Jack")
    individual_name.add_child(sur_name)
    phone = Node(names.PHONE, content="999-999-9999")
    personnel.add_child(phone)
    errs = []
    # Without role, should get an error
    with pytest.raises(MetapypeRuleError):
        validate.tree(personnel)
    # Error should name 'role' as the cause
    validate.tree(personnel, errs)
    for err_code, msg, node, *args in errs:
        err_cause, min = args
        assert err_cause == 'role'
    # With role, it should be ok
    role = Node(names.ROLE, content="drummer")
    personnel.add_child(role)
    validate.tree(personnel, errs)


def test_references():
    creator = Node(names.CREATOR)
    references = Node(names.REFERENCES)
    creator.add_child(references)
    validate.node(creator)


def test_get_children():
    r = rule.Rule("responsiblePartyRule")
    assert len(r._rule_children_names) == 9


def test_validate_choice():
    attribute = Node(names.ATTRIBUTE)
    attribute_name = Node(names.ATTRIBUTENAME)
    attribute.add_child(attribute_name)
    attribute_definition = Node(names.ATTRIBUTEDEFINITION)
    attribute.add_child(attribute_definition)
    measurement_scale = Node(names.MEASUREMENTSCALE)
    attribute.add_child(measurement_scale)
    # references = Node(names.REFERENCES)
    # attribute.add_child(references)
    validate.node(attribute)


def test_validate_sequence():
    errs = list()
    entity_code_list = Node(names.ENTITYCODELIST)
    entity_reference = Node(names.ENTITYREFERENCE)
    entity_code_list.add_child(entity_reference)
    value_attribute_reference = Node(names.VALUEATTRIBUTEREFERENCE)
    entity_code_list.add_child(value_attribute_reference)
    definition_attribute_reference = Node(names.DEFINITIONATTRIBUTEREFERENCE)
    entity_code_list.add_child(definition_attribute_reference)
    validate.node(entity_code_list)


def test_validate_sequence_bad_order():
    externally_defined_format = Node(names.EXTERNALLYDEFINEDFORMAT)
    format_name = Node(names.FORMATNAME)
    externally_defined_format.add_child(format_name)
    format_version = Node(names.FORMATVERSION)
    citation = Node(names.CITATION)
    externally_defined_format.add_child(citation)
    externally_defined_format.add_child(format_version)
    try:
        validate.node(externally_defined_format)
    except ChildNotAllowedError as e:
        assert isinstance(e, ChildNotAllowedError)


def test_validate_layered_choice():
    responsible_party = Node(names.CONTACT)
    individual_name = Node(names.INDIVIDUALNAME)
    responsible_party.add_child(individual_name)
    responsible_party.add_child(individual_name)
    position_name = Node(names.POSITIONNAME)
    responsible_party.add_child(position_name)
    phone = Node(names.PHONE)
    responsible_party.add_child(phone)
    validate.node(responsible_party)


def test_is_mixed_content():
    # Testing textRule
    abstract = Node(names.ABSTRACT)
    with pytest.raises(MetapypeRuleError) as ei:
        validate.node(abstract)
    assert "content should not be empty" in str(ei.value)
    abstract = Node(names.ABSTRACT, content="")
    with pytest.raises(MetapypeRuleError) as ei:
        validate.node(abstract)
    assert "content should not be empty" in str(ei.value)
    abstract = Node(names.ABSTRACT, content="blah blah blah")
    validate.node(abstract)
    abstract = Node(names.ABSTRACT, content="blah blah blah")
    para = Node(names.PARA, content="more blah blah blah")
    abstract.add_child(para)
    validate.node(abstract)
    abstract = Node(names.ABSTRACT)
    para = Node(names.PARA, content="more blah blah blah")
    abstract.add_child(para)
    validate.node(abstract)
    title = Node(names.TITLE, content="more blah blah blah")
    abstract.add_child(title)
    with pytest.raises(MetapypeRuleError) as ei:
        validate.node(abstract)
    assert "not allowed in parent" in str(ei.value)

    # Testing anyNameRule
    city = Node(names.CITY)
    with pytest.raises(MetapypeRuleError) as ei:
        validate.node(city)
    assert "content should not be empty" in str(ei.value)
    city = Node(names.CITY, content="")
    with pytest.raises(MetapypeRuleError) as ei:
        validate.node(city)
    assert "content should not be empty" in str(ei.value)
    city = Node(names.CITY, content="Albuquerque")
    validate.node(city)
    city = Node(names.CITY)
    value = Node(names.VALUE, content="Albuquerque")
    city.add_child(value)
    validate.node(city)


def test_nonempty_mixed_content():
    title = Node(names.TITLE, content="")
    with pytest.raises(MetapypeRuleError):
        validate.node(title)


def test_missing_numerical_unit():
    unit = Node(names.UNIT, parent=None)
    r = rule.get_rule(names.UNIT)
    with pytest.raises(MetapypeRuleError):
        r.validate_rule(unit)
    # Check error
    errs = []
    validate.tree(unit, errs)
    assert len(errs) == 1
    err_code, msg, node, *args = errs[0]
    assert err_code == ValidationError.MIN_CHOICE_UNMET
    assert args[0] == 'unit'
    # With a customUnit, it should be ok
    custom_unit = Node(names.CUSTOMUNIT, parent=unit)
    custom_unit.content = 'bushels per parsec'
    unit.add_child(custom_unit)
    validate.tree(unit)


def test_taxonid():
    taxonId = Node(names.TAXONID, parent=None)
    taxonId.content = "42"
    # without the provider, we should get an error
    with pytest.raises(MetapypeRuleError):
        validate.node(taxonId)
    # with the provider, it should be ok
    taxonId.add_attribute("provider", "https://www.itis.gov")
    validate.node(taxonId)


def test_bounding_altitudes():
    bounding_coordinates = Node(names.BOUNDINGCOORDINATES, parent=None)
    bc_west = Node(names.WESTBOUNDINGCOORDINATE, parent=bounding_coordinates)
    bc_east = Node(names.EASTBOUNDINGCOORDINATE, parent=bounding_coordinates)
    bc_north = Node(names.NORTHBOUNDINGCOORDINATE, parent=bounding_coordinates)
    bc_south = Node(names.SOUTHBOUNDINGCOORDINATE, parent=bounding_coordinates)
    bc_west.content = "0.0"
    bc_east.content = "0.0"
    bc_north.content = "0.0"
    bc_south.content = "0.0"
    bounding_coordinates.add_child(bc_west)
    bounding_coordinates.add_child(bc_east)
    bounding_coordinates.add_child(bc_north)
    bounding_coordinates.add_child(bc_south)
    # without boundingAltitudes should be ok
    validate.node(bounding_coordinates)
    # boundingAltitudes should fail if not all required children present
    bounding_altitudes = Node(names.BOUNDINGALTITUDES, parent=bounding_coordinates)
    bounding_coordinates.add_child(bounding_altitudes)
    with pytest.raises(MetapypeRuleError):
        validate.tree(bounding_coordinates)
    altitude_minimum = Node(names.ALTITUDEMINIMUM, parent=bounding_altitudes)
    bounding_altitudes.add_child(altitude_minimum)
    with pytest.raises(MetapypeRuleError):
        validate.tree(bounding_coordinates)
    altitude_minimum.content = "0.0"
    with pytest.raises(MetapypeRuleError):
        validate.tree(bounding_coordinates)
    # boundingAltitudes should fail if not all required children have content
    altitude_maximum = Node(names.ALTITUDEMAXIMUM, parent=bounding_altitudes)
    bounding_altitudes.add_child(altitude_maximum)
    altitude_units = Node(names.ALTITUDEUNITS, parent=bounding_altitudes)
    bounding_altitudes.add_child(altitude_units)
    with pytest.raises(MetapypeRuleError):
        validate.tree(bounding_coordinates)
    # with content filled in, should pass
    altitude_maximum.content = "1000.0"
    altitude_units.content = "meter"
    validate.tree(bounding_coordinates)


def test_is_in_path():
    associated_party = Node(names.ASSOCIATEDPARTY)
    organization_name = Node(names.ORGANIZATIONNAME)
    associated_party.add_child(organization_name)
    address = Node(names.ADDRESS)
    associated_party.add_child(address)
    online_url = Node(names.ONLINEURL)
    associated_party.add_child(online_url)
    phone = Node(names.PHONE)
    r = rule.get_rule(names.ASSOCIATEDPARTY)
    print("\n")
    assert Rule._is_in_path(r.children, phone)


def test_project():
    """
    Note that this test was created because downstream metapype users (i.e., ezEML) did not support the
    studyAreaDescription element in EML. Metapype did support it, but key sections (including the rules.json "project"
    element) were causing issues with ezEML, so the simplest mitigation was to remove it at this time.

    Content was commented out of
    1. names.py
    2. rule.py

    Content was removed from
    1. rules.json (because native JSON does not support comments)
    """
    project = Node(names.PROJECT)
    title = Node(names.TITLE, content="My Title")
    personnel = Node(names.PERSONNEL)
    individual_name = Node(names.INDIVIDUALNAME)
    personnel.add_child(individual_name)
    sur_name = Node(names.SURNAME, content="Gaucho")
    individual_name.add_child(sur_name)
    project.add_child(title)
    project.add_child(personnel)
    role = Node(names.ROLE, content="Janitor")
    personnel.add_child(role)
    # study_area_description = Node(names.STUDYAREADESCRIPTION)
    # project.add_child(study_area_description)
    descriptor = Node(names.DESCRIPTOR)
    descriptor.add_attribute("name", "A")
    descriptor.add_attribute("citableClassificationSystem", "true")
    # study_area_description.add_child(descriptor)
    descriptor_value = Node(names.DESCRIPTORVALUE, content="Z")
    descriptor.add_child(descriptor_value)
    print("\n")
    print(metapype_io.graph(project))
    validate.tree(project)


def test_data_source():
    methods = Node(names.METHODS)
    method_step = Node(names.METHODSTEP)
    description = Node(names.DESCRIPTION)
    description.content = "This is my description"
    method_step.add_child(description)
    data_source = Node(names.DATASOURCE)
    title = Node(names.TITLE)
    title.content = "This is my title"
    data_source.add_child(title)
    creator = Node(names.CREATOR)
    individual_name = Node(names.INDIVIDUALNAME)
    surname = Node(names.SURNAME)
    surname.content = "Me"
    individual_name.add_child(surname)
    creator.add_child(individual_name)
    data_source.add_child(creator)
    distribution = Node(names.DISTRIBUTION)
    online = Node(names.ONLINE)
    url = Node(names.URL)
    url.add_attribute("function", "information")
    url.content = "https://mydata.org"
    online.add_child(url)
    distribution.add_child(online)
    data_source.add_child(distribution)
    contact = Node(names.CONTACT)
    position_name = Node(names.POSITIONNAME)
    position_name.content = "Information Manager"
    contact.add_child(position_name)
    data_source.add_child(contact)
    method_step.add_child(data_source)
    methods.add_child(method_step)
    print("\n")
    print(metapype_io.graph(methods))
    validate.tree(methods)


def test_measurement_scale():
    measurement_scale = Node(names.MEASUREMENTSCALE)
    ratio = Node(names.RATIO)
    measurement_scale.add_child(ratio)
    unit = Node(names.UNIT)
    standard_unit = Node(names.STANDARDUNIT)
    standard_unit.content = "meter"
    unit.add_child(standard_unit)
    ratio.add_child(unit)
    precision = Node(names.PRECISION)
    precision.content = "0.1"
    ratio.add_child(precision)
    numeric_domain = Node(names.NUMERICDOMAIN)
    number_type = Node(names.NUMBERTYPE)
    number_type.content = "float"
    numeric_domain.add_child(number_type)
    ratio.add_child(numeric_domain)
    print("\n")
    print(metapype_io.graph(measurement_scale))
    validate.tree(measurement_scale)

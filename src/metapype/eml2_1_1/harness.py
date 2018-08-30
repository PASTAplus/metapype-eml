#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: harness

:Synopsis:

:Author:
    servilla
    costa

:Created:
    6/5/18
"""
import json

import daiquiri

from metapype.eml2_1_1.exceptions import MetapypeRuleError
from metapype.eml2_1_1 import export
from metapype.eml2_1_1 import evaluate
from metapype.eml2_1_1 import names
from metapype.eml2_1_1 import rule
from metapype.eml2_1_1 import validate
from metapype.model import io
from metapype.model.node import Node


logger = daiquiri.getLogger('harness: ' + __name__)


def main():

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

    pubdate = Node(names.PUBDATE, parent=dataset)
    pubdate.content = '2018'
    dataset.add_child(pubdate)

    coverage = Node(names.COVERAGE, parent=dataset)
    dataset.add_child(coverage)
    geographic_coverage = Node(names.GEOGRAPHICCOVERAGE, parent=coverage)
    coverage.add_child(geographic_coverage)
    geographic_description = Node(names.GEOGRAPHICDESCRIPTION, 
                                  parent=geographic_coverage)
    geographic_description.content = "Somewhere in the Rocky Mountains"
    geographic_coverage.add_child(geographic_description)
    bounding_coordinates = Node(names.BOUNDINGCOORDINATES, 
                                parent=geographic_coverage)
    geographic_coverage.add_child(bounding_coordinates)
    wbc = Node(names.WESTBOUNDINGCOORDINATE, parent=bounding_coordinates)
    wbc.content = -107.55538624999997
    bounding_coordinates.add_child(wbc)
    ebc = Node(names.EASTBOUNDINGCOORDINATE, parent=bounding_coordinates)
    ebc.content = -106.45675343749997
    bounding_coordinates.add_child(ebc)
    nbc = Node(names.NORTHBOUNDINGCOORDINATE, parent=bounding_coordinates)
    nbc.content = 39.48496522541802
    bounding_coordinates.add_child(nbc)
    sbc = Node(names.SOUTHBOUNDINGCOORDINATE, parent=bounding_coordinates)
    sbc.content = 38.9530013453599
    bounding_coordinates.add_child(sbc)

    taxonomic_coverage = Node(names.TAXONOMICCOVERAGE, parent=coverage)
    coverage.add_child(taxonomic_coverage)
    general_taxonomic_coverage = Node(names.GENERALTAXONOMICCOVERAGE, 
                                      parent=taxonomic_coverage)
    taxonomic_coverage.add_child(general_taxonomic_coverage)
    general_taxonomic_coverage.content = "All vascular plants were \
identified to family or species, mosses and lichens were \
identified as moss or lichen."
    
    taxonomic_classification_genus = Node(names.TAXONOMICCLASSIFICATION, 
                                          parent=taxonomic_coverage)
    taxonomic_coverage.add_child(taxonomic_classification_genus)

    taxon_rank_name_genus = Node(names.TAXONRANKNAME, 
                                 parent=taxonomic_classification_genus)
    taxonomic_classification_genus.add_child(taxon_rank_name_genus)
    taxon_rank_name_genus.content = "Genus"

    taxon_rank_value_genus = Node(names.TAXONRANKVALUE, 
                                  parent=taxonomic_classification_genus)
    taxonomic_classification_genus.add_child(taxon_rank_value_genus)
    taxon_rank_value_genus.content = "Escherichia"

    taxonomic_classification_species = Node(names.TAXONOMICCLASSIFICATION, 
                                       parent=taxonomic_classification_genus)
    taxonomic_classification_genus.add_child(taxonomic_classification_species)

    taxon_rank_name_species = Node(names.TAXONRANKNAME, 
                              parent=taxonomic_classification_species)
    taxonomic_classification_species.add_child(taxon_rank_name_species)
    taxon_rank_name_species.content = "Species"

    taxon_rank_value_species = Node(names.TAXONRANKVALUE,
                               parent=taxonomic_classification_species)
    taxonomic_classification_species.add_child(taxon_rank_value_species)
    taxon_rank_value_species.content = "coli"

    contact = Node(names.CONTACT, parent=dataset)
    dataset.add_child(contact)

    individualName_contact = Node(names.INDIVIDUALNAME, parent=contact)
    contact.add_child(individualName_contact)

    givenName_contact = Node(names.GIVENNAME, parent=individualName_contact)
    givenName_contact.content = 'Chase'
    individualName_contact.add_child(givenName_contact)

    surName_contact = Node(names.SURNAME, parent=individualName_contact)
    surName_contact.content = 'Gaucho'
    individualName_contact.add_child(surName_contact)

    node = Node.get_node_instance(access.id)

    access_rule = rule.get_rule(names.ACCESS)
    
    try:
        access_rule.validate_rule(access)
    except MetapypeRuleError as e:
        logger.error(e)
    print(access_rule.attributes)
    print(access_rule.children)
    print(access_rule.content_rules)

    try:
        validate.node(access)
    except MetapypeRuleError as e:
        logger.error(e)

    try:
        validate.tree(eml)
    except  MetapypeRuleError as e:
        logger.error(e)

    print(evaluate.node(title))

    io.graph(eml, 0)

    attr = access_rule.attributes
    print(attr)
    children = access_rule.children
    print(children)
    #
    print(access.list_attributes())

    json_str = io.to_json(eml)
    print(json_str)
    with open('test_eml.json', 'w') as f:
        f.write(json_str)
    #
    m = json.loads(json_str)
    node = io.from_json(m)
    #
    #
    try:
        validate.tree(node)
    except  MetapypeRuleError as e:
        logger.error(e)
    #
    xml = export.to_xml(eml)
    print(xml)
    with open('test_eml.xml', 'w') as f:
        f.write(xml)


    evaluation = {}
    evaluate.tree(eml, evaluation)
    for e in evaluation:
        print('{0}: {1}'.format(e, evaluation[e]))

    return 0


if __name__ == "__main__":
    main()

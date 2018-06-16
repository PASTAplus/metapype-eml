#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: harness

:Synopsis:

:Author:
    servilla

:Created:
    6/5/18
"""
import json

import daiquiri

from metapype.eml2_1_1.exceptions import MetapypeRuleError
import metapype.eml2_1_1.export
import metapype.eml2_1_1.validate as validate
from metapype.model.node import Node
from metapype.model import io
from metapype.model import views


logger = daiquiri.getLogger('harness: ' + __name__)


def main():
    # Create root EML node, with attributes
    eml = Node('eml')
    eml.add_attribute('packageId', 'edi.1001.1')
    eml.add_attribute('system', 'http://metapypelite.edirepository.org')

    # Create access control node with approrpiate permissionsc
    access = Node('access', parent=eml)
    access.add_attribute('authSystem', 'https://pasta.edirepository.org/authentication')
    access.add_attribute('order', 'allowFirst')
    allow = Node('allow', parent=access)
    principal = Node('principal', parent=allow, content='uid=chase,o=EDI,dc=edirepository,dc=org')
    allow.add_child(principal)
    permission = Node('permission', parent=allow, content='changePermission')
    allow.add_child(permission)
    access.add_child(allow)
    allow = Node('allow', parent=access)
    principal = Node('principal', parent=allow, content='public')
    allow.add_child(principal)
    permission = Node('permission', parent=allow, content='read')
    allow.add_child(permission)
    access.add_child(allow)
    deny = Node('deny', parent=access)
    access.add_child(deny)
    principal = Node('principal', parent=deny, content='public')
    deny.add_child(principal)
    permission = Node('permission', parent=deny, content='write')
    deny.add_child(permission)
    eml.add_child(access)


    # Create dataset node
    dataset = Node('dataset')
    eml.add_child(dataset)
    title = Node('title', parent=dataset, content='This is my title')
    dataset.add_child(title)
    creator = Node('creator', parent=dataset)
    dataset.add_child(creator)
    individual_name = Node('individualName', parent=creator)
    creator.add_child(individual_name)
    given_name = Node('givenName', parent=individual_name, content='Mark')
    individual_name.add_child(given_name)
    surname = Node('surName', parent=individual_name)
    surname.content = 'Servilla'
    value = Node('value', parent = surname)
    value.content = 'Servilla'
    value.add_attribute('xml:lang', 'en')
    surname.add_child(value)
    individual_name.add_child(surname)
    contact = Node('contact', parent=dataset)
    dataset.add_child(contact)
    contact.add_child(individual_name)
    contact = Node('contact', parent=dataset)
    individual_name = Node('individualName', parent=contact)
    surname = Node('surName', parent=individual_name, content='James')
    dataset.add_child(contact)
    contact.add_child(individual_name)
    individual_name.add_child(surname)


    # Create additional metadata node
    additional_metadata = Node('additionalMetadata', parent=eml)
    eml.add_child(additional_metadata)
    metadata = Node('metadata', parent=additional_metadata, content='<test>TEST</test>')
    additional_metadata.add_child(metadata)

    try:
        validate.tree(eml)
    except  MetapypeRuleError as e:
        logger.error(e)

    json_str = io.to_json(eml)
    print(json_str)
    with open('test_eml.json', 'w') as f:
        f.write(json_str)

    m = json.loads(json_str)
    node = io.from_json(m)

    io.graph(node, 0)

    try:
        validate.tree(node)
    except  MetapypeRuleError as e:
        logger.error(e)

    xml = metapype.eml2_1_1.export.to_xml(node)
    print(xml)
    with open('test_eml.xml', 'w') as f:
        f.write(xml)


    return 0


if __name__ == "__main__":
    main()

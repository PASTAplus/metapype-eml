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
from metapype.eml2_1_1 import export
from metapype.eml2_1_1 import evaluate
from metapype.eml2_1_1 import names
from metapype.eml2_1_1 import validate
from metapype.model.node import Node
from metapype.model import io


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

    try:
        validate.tree(eml)
    except  MetapypeRuleError as e:
        logger.error(e)

    evaluation = {}
    evaluate.tree(eml, evaluation)
    for e in evaluation:
        print('{0}: {1}'.format(e, evaluation[e]))

    print(evaluation)

    # json_str = io.to_json(eml)
    # print(json_str)
    # with open('test_eml.json', 'w') as f:
    #     f.write(json_str)
    #
    # m = json.loads(json_str)
    # node = io.from_json(m)
    #
    io.graph(eml, 0)
    #
    # try:
    #     validate.tree(node)
    # except  MetapypeRuleError as e:
    #     logger.error(e)
    #
    # xml = export.to_xml(node)
    # print(xml)
    # with open('test_eml.xml', 'w') as f:
    #     f.write(xml)


    return 0


if __name__ == "__main__":
    main()

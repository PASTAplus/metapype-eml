#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_references

:Synopsis:

:Author:
    servilla

:Created:
    2/24/21
"""
import os

import daiquiri

import tests
import metapype.eml.names as names
import metapype.eml.references as references
import metapype.eml.validate as validate
import metapype.model.metapype_io as metapype_io
from metapype.model.node import Node


logger = daiquiri.getLogger(__name__)


def test_expand():
    if "TEST_DATA" in os.environ:
        xml_path = os.environ["TEST_DATA"]
    else:
        xml_path = tests.test_data_path

    with open(f"{xml_path}/eml.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    validate.tree(eml)
    references.expand(eml)
    validate.tree(eml)
    creator = eml.find_descendant(names.CREATOR)
    creator.name = "node"
    creator.attributes = dict()
    metadata_provider = eml.find_descendant(names.METADATAPROVIDER)
    metadata_provider.name = "node"
    assert Node.is_equal(creator, metadata_provider)
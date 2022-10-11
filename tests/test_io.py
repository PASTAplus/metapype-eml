#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_io

:Synopsis:

:Author:
    servilla
    costa
    ide
  
:Created:
    1/14/19
"""
import os

import daiquiri

import tests
from metapype.eml import validate
from metapype.model import metapype_io
from metapype.model.node import Node


logger = daiquiri.getLogger("test_io: " + __name__)


def test_from_json():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path

    with open(f"{test_data}/eml.json", "r") as f:
        eml_json = "".join([_ for _ in f.readlines()])
    eml = metapype_io.from_json(eml_json)
    validate.tree(eml)


def test_from_xml():
    if "TEST_DATA" in os.environ:
        xml_path = os.environ["TEST_DATA"]
    else:
        xml_path = tests.test_data_path

    with open(f"{xml_path}/eml.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml, literals=("literalLayout", "markdown"))
    assert isinstance(eml, Node)
    validate.tree(eml)


def test_to_json():
    if "TEST_DATA" in os.environ:
        xml_path = os.environ["TEST_DATA"]
    else:
        xml_path = tests.test_data_path

    with open(f"{xml_path}/eml.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml, literals=("literalLayout", "markdown"))
    assert isinstance(eml, Node)
    validate.prune(eml)
    validate.tree(eml)
    j = metapype_io.to_json(eml, 2)
    assert isinstance(j, str)


def test_to_xml():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path

    with open(f"{test_data}/eml.json", "r") as f:
        eml_json = "".join([_ for _ in f.readlines()])
    eml = metapype_io.from_json(eml_json)
    validate.tree(eml)
    xml = metapype_io.to_xml(eml)
    assert isinstance(xml, str)


def test_graph():
    if "TEST_DATA" in os.environ:
        xml_path = os.environ["TEST_DATA"]
    else:
        xml_path = tests.test_data_path

    with open(f"{xml_path}/eml.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    assert isinstance(eml, Node)
    validate.prune(eml)
    validate.tree(eml)
    g = metapype_io.graph(eml)
    assert isinstance(g, str)


def test_text_type():
    xml = """
        <abstract lang="en" xmlns:eml="https://eml.ecoinformatics.org/eml-2.2.0">
            <section xmlns:eml="https://eml.ecoinformatics.org/eml-2.1.1">
                <para>This is <emphasis>abstract</emphasis> <subscript>Para 1</subscript> But 1 &lt; 2, capiche?</para>
            </section>
        </abstract>
    """
    eml = metapype_io.from_xml(xml, True, ("literalLayout", "markdown"))
    validate.tree(eml)
    new_xml = metapype_io.to_xml(eml)
    print("\n", new_xml)

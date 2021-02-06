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

from metapype.config import Config
from metapype.eml import names
from metapype.eml import validate
from metapype.model import metapype_io
from metapype.model.node import Node


logger = daiquiri.getLogger("test_io: " + __name__)


def test_from_json():
    if "EML_JSON" in os.environ:
        json_path = os.environ["EML_JSON"]
    else:
        json_path = Config.EML_JSON

    with open(json_path, "r") as f:
        eml_json = "".join([_ for _ in f.readlines()])
    eml = metapype_io.from_json(eml_json)
    validate.tree(eml)


def test_from_xml():
    if "EML_XML" in os.environ:
        xml_path = os.environ["EML_XML"]
    else:
        xml_path = Config.EML_XML

    with open(xml_path, "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    assert isinstance(eml, Node)
    validate.tree(eml)


def test_to_json():
    if "EML_XML" in os.environ:
        xml_path = os.environ["EML_XML"]
    else:
        xml_path = Config.EML_XML

    with open(xml_path, "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    assert isinstance(eml, Node)
    validate.prune(eml)
    validate.tree(eml)
    j = metapype_io.to_json(eml)
    assert isinstance(j, str)


def test_to_xml():
    if "EML_JSON" in os.environ:
        json_path = os.environ["EML_JSON"]
    else:
        json_path = Config.EML_JSON

    with open(json_path, "r") as f:
        eml_json = "".join([_ for _ in f.readlines()])
    eml = metapype_io.from_json(eml_json)
    validate.tree(eml)
    xml = metapype_io.to_xml(eml)
    assert isinstance(xml, str)


def test_graph():
    if "EML_XML" in os.environ:
        xml_path = os.environ["EML_XML"]
    else:
        xml_path = Config.EML_XML

    with open(xml_path, "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    assert isinstance(eml, Node)
    validate.prune(eml)
    validate.tree(eml)
    g = metapype_io.graph(eml)
    assert isinstance(g, str)

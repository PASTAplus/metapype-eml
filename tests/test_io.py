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


def test_to_json():
    eml = Node(names.EML)
    eml.add_attribute("packageId", "edi.23.1")
    eml.add_attribute("system", "metapype")
    access = Node(names.ACCESS, parent=eml)
    access.add_attribute("authSystem", "pasta")
    access.add_attribute("order", "allowFirst")
    eml.add_child(access)
    allow = Node(names.ALLOW, parent=access)
    access.add_child(allow)
    principal = Node(names.PRINCIPAL, parent=allow)
    principal.content = "uid=gaucho,o=EDI,dc=edirepository,dc=org"
    allow.add_child(principal)
    permission = Node(names.PERMISSION, parent=allow)
    permission.content = "all"
    allow.add_child(permission)
    j = metapype_io.to_json(eml)
    assert isinstance(j, str)

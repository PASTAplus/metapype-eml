#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_prune

:Synopsis:

:Author:
    servilla

:Created:
    10/26/21
"""
import os

import daiquiri

import metapype.model.metapype_io as metapype_io
import metapype.eml.validate as validate
import tests


logger = daiquiri.getLogger(__name__)


def test_prune():
    if "TEST_DATA" in os.environ:
        test_data = os.environ["TEST_DATA"]
    else:
        test_data = tests.test_data_path

    with open(f"{test_data}/eml.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    pruned = validate.prune(eml, strict=True)
    for node in pruned:
        print(f"pruned: {node[0].name} - {node[1]}")
    errs = []
    validate.tree(eml, errs)
    for err in errs:
        print(err)


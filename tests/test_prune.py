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
import daiquiri
import pytest

import metapype.model.metapype_io as metapype_io
import metapype.eml.validate as validate


def test_prune():
    print()
    eml_xml = "./data/eml"
    with open(f"{eml_xml}.xml", "r") as f:
        xml = "".join(f.readlines())
    eml = metapype_io.from_xml(xml)
    pruned = validate.prune(eml, strict=True)
    for node in pruned:
        print(f"pruned: {node[0].name} - {node[1]}")
    errs = []
    validate.tree(eml, errs)
    for err in errs:
        print(err)
    # with open(f"{eml_xml}.new.xml", "w") as f:
    #     f.write(metapype_io.to_xml(eml))


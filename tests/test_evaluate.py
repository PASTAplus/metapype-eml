#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_evaluate

:Synopsis:

:Author:
    servilla

:Created:
    2/17/24
"""
import daiquiri


from metapype.eml import evaluate
from metapype.eml import names
from metapype.model.node import Node


logger = daiquiri.getLogger(__name__)


def test_title_rule():
    dataset = Node(names.DATASET)
    title = Node(names.TITLE, parent=dataset)
    title.content = "Test Title too short"
    assert len(evaluate._title_rule(title)) != 0
    title.content = "This test title is long enough so that it should not fail the tile rule"
    assert len(evaluate._title_rule(title)) == 0
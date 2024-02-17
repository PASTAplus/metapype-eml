#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_normalize

:Synopsis:

:Author:
    servilla

:Created:
    2/17/24
"""
import daiquiri

from metapype.model.normalize import normalize

logger = daiquiri.getLogger(__name__)


def test_normalize_xml():
    test_xml = "<?xml version=\"1.0\"?><test a=\" test  me \"><child>   This is a   test   </child></test>"

    expected = ('<?xml version="1.0"?>\n'
                '<test a="test me">\n'
                '  <child>This is a test</child>\n'
                '</test>\n')

    normalized = normalize(test_xml, is_xml=True)
    assert normalized == expected


def test_normalize_text():
    test_text = "   This is a   test   "

    expected = "This is a test"

    normalized = normalize(test_text, is_xml=False)
    assert normalized == expected

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_io

:Synopsis:

:Author:
    servilla
  
:Created:
    1/14/19
"""
import os
import sys
import unittest

import daiquiri

from metapype.eml2_1_1 import names
from metapype.model import io
from metapype.model.node import Node


sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_io: ' + __name__)


class TestIO(unittest.TestCase):

    def setUp(self):
        self.node = Node(names.EML)

    def tearDown(self):
        self.node = None

    def test_to_json(self):
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
        j = io.to_json(eml)
        self.assertIsInstance(j, str)


if __name__ == '__main__':
    unittest.main()
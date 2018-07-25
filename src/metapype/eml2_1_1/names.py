#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: names

:Synopsis:

:Author:
    servilla

:Created:
    6/18/18
"""
import daiquiri


logger = daiquiri.getLogger('names: ' + __name__)

# Named constants for EML 2.1.1 metadata element names
ABSTRACT = 'abstract'
ACCESS = 'access'
ADDITIONALMETADATA = 'additionalMetadata'
ALLOW = 'allow'
CONTACT = 'contact'
CREATOR = 'creator'
DATASET = 'dataset'
DENY = 'deny'
EML = 'eml'
GIVENNAME = 'givenName'
INDIVIDUALNAME = 'individualName'
KEYWORD = 'keyword'
KEYWORDSET = 'keywordSet'
KEYWORDTHESAURUS = 'keywordThesaurus'
METADATA = 'metadata'
ORGANIZATIONNAME = 'organizationName'
PERMISSION = 'permission'
POSITIONNAME = 'positionName'
PRINCIPAL = 'principal'
SALUTATION = 'salutation'
SURNAME = 'surName'
TITLE = 'title'
VALUE = 'value'

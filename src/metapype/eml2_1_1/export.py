#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: export

:Synopsis:

:Author:
    servilla

:Created:
    6/12/18
"""
import daiquiri

from metapype.model.node import Node

logger = daiquiri.getLogger('export: ' + __name__)

space = '    '

def to_xml(node: Node, level: int=0) -> str:
    xml=''
    boiler = 'xmlns:eml="eml://ecoinformatics.org/eml-2.1.1" ' + \
             'xmlns:stmml="http://www.xml-cml.org/schema/stmml-1.1" ' + \
             'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' + \
             'xsi:schemaLocation="eml://ecoinformatics.org/eml-2.1.1 ' + \
             'http://nis.lternet.edu/schemas/EML/eml-2.1.1/eml.xsd"'
    name = node.name
    attributes = ''
    for attribute in node.attributes:
        attributes += ' {0}="{1}"'.format(attribute, node.attributes[attribute])
    if level == 0:
        indent = ''
        if name == 'eml':
            name = node.name + ':' + node.name
            attributes += ' ' + boiler
    else:
        indent = space * level
    open_tag = '<'+ name + attributes + '>'
    xml += indent + open_tag + '\n'
    if node.content is not None:
        xml += indent + space + node.content + '\n'
    for child in node.children:
       xml += to_xml(child, level + 1)
    close_tag = '</' + name + '>'

    if level == 0:
        xml += indent + close_tag
    else:
        xml += indent + close_tag + '\n'

    return xml


def main():
    return 0


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: export

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    6/12/18
"""
import daiquiri

from metapype.model.node import Node


logger = daiquiri.getLogger('export: ' + __name__)
space = '    '


def to_xml(node: Node, level: int=0) -> str:
    xml=''
    closed = False
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
    close_tag = '</' + name + '>'
    xml += indent + open_tag
    if node.content is not None:
        xml += str(node.content) + close_tag + '\n'
        closed = True
    elif len(node.children) > 0:
        xml += '\n'
    for child in node.children:
        xml += to_xml(child, level + 1)
    if not closed:
        if len(node.children) > 0:
            xml += indent
        xml += close_tag + '\n'

    return xml


def main():
    return 0


if __name__ == "__main__":
    main()

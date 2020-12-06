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
from xml.sax.saxutils import escape, unescape


logger = daiquiri.getLogger("export: " + __name__)
space = "    "


def to_xml(node: Node, level: int = 0) -> str:
    xml = ""
    closed = False
    boiler = (
        'xmlns:eml="https://eml.ecoinformatics.org/eml-2.2.0" '
        'xmlns:stmml="http://www.xml-cml.org/schema/stmml-1.2" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="https://eml.ecoinformatics.org/eml-2.2.0 '
        'https://nis.lternet.edu/schemas/EML/eml-2.2.0/xsd/eml.xsd"'
    )
    name = node.name
    attributes = ""
    for attribute in node.attributes:
        attributes += ' {0}="{1}"'.format(
            attribute, node.attributes[attribute]
        )
    if level == 0:
        indent = ""
        if name == "eml":
            name = node.name + ":" + node.name
            attributes += " " + boiler
    else:
        indent = space * level
    open_tag = "<" + name + attributes + ">"
    close_tag = "</" + name + ">"
    xml += indent + open_tag
    if node.content is not None:
        if isinstance(node.content, str):
            # if it hasn't been escaped already, escape it
            if all (x not in node.content for x in ('&amp;', '&lt;', '&gt;')):
                node.content = escape(node.content)
                # Hopefully, this is a temporary hack. Need to figure out a better way...
                # The problem is that <para> tags are treated idiosyncratically because their rules aren't fully
                #  supported. They appear within node content, unlike other tags.
                node.content = node.content.replace('&lt;para&gt;', '<para>').replace('&lt;/para&gt;', '</para>')
        xml += str(node.content) + close_tag + "\n"
        closed = True
    elif len(node.children) > 0:
        xml += "\n"
    for child in node.children:
        xml += to_xml(child, level + 1)
    if not closed:
        if len(node.children) > 0:
            xml += indent
        xml += close_tag + "\n"

    return xml


def main():
    return 0


if __name__ == "__main__":
    main()

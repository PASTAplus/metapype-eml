#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    normalize

:Synopsis:
    Normalize an EML XML document instance or text content, including replacement of non-breaking space characters
    with space characters.

:Author:
    servilla

:Created:
    2/17/24
"""

import daiquiri
from lxml import etree

logger = daiquiri.getLogger(__name__)

normalize_whitespace = \
    """<xsl:stylesheet version="1.0"
                       xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       >
           <xsl:output omit-xml-declaration="no" indent="yes"/>

           <!-- Template to copy nodes and apply templates to attributes and child nodes -->
           <xsl:template match="@*|node()">
               <xsl:copy>
                   <!-- Apply templates to attributes first to normalize space, then to child nodes -->
                   <xsl:apply-templates select="@*"/>
                   <xsl:apply-templates select="node()"/>
               </xsl:copy>
           </xsl:template>

           <!-- Template for normalizing space in text nodes, with specific exclusions -->
           <xsl:template match="text()[not(ancestor::markup or ancestor::literalLayout or ancestor::objectName or ancestor::attributeName or ancestor::para)]">
               <xsl:value-of select="normalize-space(.)"/>
           </xsl:template>

           <!-- Template to normalize space in attribute values -->
           <xsl:template match="@*">
               <!-- Create a new attribute with the same name but normalized value -->
               <xsl:attribute name="{name()}">
                   <xsl:value-of select="normalize-space(.)"/>
               </xsl:attribute>
           </xsl:template>
       </xsl:stylesheet>"""


def normalize(content: str, is_xml: bool = False) -> str:
    """
    Normalize whitespace within a string, including replacement of non-breaking space characters
    :param content: String content to be normalized
    :param is_xml: Boolean to indicate if content is XML
    :return: Normalized content as a unicode string
    """
    if is_xml:
        xslt = etree.XSLT(etree.XML(normalize_whitespace))
        normalized = str(xslt(etree.XML(content.replace('\xa0', ' ').encode("utf-8"))))
    else:
        words = content.replace('\xa0', ' ').split(" ")
        normalized = " ".join([word.strip() for word in words if word.strip() != ""])
    return normalized

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: harness

:Synopsis:

:Author:
    servilla
    costa

:Created:
    6/5/18
"""
import json

import daiquiri

from metapype.eml2_1_1.exceptions import MetapypeRuleError
from metapype.eml2_1_1 import export
from metapype.eml2_1_1 import evaluate
from metapype.eml2_1_1 import names
from metapype.eml2_1_1 import rule
from metapype.eml2_1_1 import validate
from metapype.model import io
from metapype.model.node import Node


logger = daiquiri.getLogger('harness: ' + __name__)


def main():

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

    dataset = Node(names.DATASET, parent=eml)
    eml.add_child(dataset)

    title = Node(names.TITLE, parent=dataset)
    title.content = 'Green sea turtle counts: Tortuga Island 20017'
    dataset.add_child(title)

    creator = Node(names.CREATOR, parent=dataset)
    dataset.add_child(creator)

    individualName_creator = Node(names.INDIVIDUALNAME, parent=creator)
    creator.add_child(individualName_creator)

    surName_creator = Node(names.SURNAME, parent=individualName_creator)
    surName_creator.content = 'Gaucho'
    individualName_creator.add_child(surName_creator)

    pubdate = Node(names.PUBDATE, parent=dataset)
    pubdate.content = '2018'
    dataset.add_child(pubdate)

    coverage = Node(names.COVERAGE, parent=dataset)
    dataset.add_child(coverage)
    geographic_coverage = Node(names.GEOGRAPHICCOVERAGE, parent=coverage)
    coverage.add_child(geographic_coverage)
    geographic_description = Node(names.GEOGRAPHICDESCRIPTION, 
                                  parent=geographic_coverage)
    geographic_description.content = "Somewhere in the Rocky Mountains"
    geographic_coverage.add_child(geographic_description)
    bounding_coordinates = Node(names.BOUNDINGCOORDINATES, 
                                parent=geographic_coverage)
    geographic_coverage.add_child(bounding_coordinates)
    wbc = Node(names.WESTBOUNDINGCOORDINATE, parent=bounding_coordinates)
    wbc.content = -107.55538624999997
    bounding_coordinates.add_child(wbc)
    ebc = Node(names.EASTBOUNDINGCOORDINATE, parent=bounding_coordinates)
    ebc.content = -106.45675343749997
    bounding_coordinates.add_child(ebc)
    nbc = Node(names.NORTHBOUNDINGCOORDINATE, parent=bounding_coordinates)
    nbc.content = 39.48496522541802
    bounding_coordinates.add_child(nbc)
    sbc = Node(names.SOUTHBOUNDINGCOORDINATE, parent=bounding_coordinates)
    sbc.content = 38.9530013453599
    bounding_coordinates.add_child(sbc)


    temporal_coverage = Node(names.TEMPORALCOVERAGE, parent=coverage)
    coverage.add_child(temporal_coverage)

    single_date_time = Node(names.SINGLEDATETIME, parent=temporal_coverage)
    temporal_coverage.add_child(single_date_time)
    single_date_time.content = '2018'

    range_of_dates = Node(names.RANGEOFDATES, parent=temporal_coverage)
    temporal_coverage.add_child(range_of_dates)
    
    begin_date = Node(names.BEGINDATE, parent=range_of_dates)
    range_of_dates.add_child(begin_date)

    calendar_date_begin = Node(names.CALENDARDATE, parent=begin_date)
    begin_date.add_child(calendar_date_begin)
    calendar_date_begin.content = '2000'

    end_date = Node(names.ENDDATE, parent=range_of_dates)
    range_of_dates.add_child(end_date)

    calendar_date_end = Node(names.CALENDARDATE, parent=end_date)
    end_date.add_child(calendar_date_end)
    calendar_date_end.content = '2018'

    temporal_coverage_rule = rule.get_rule(names.TEMPORALCOVERAGE)
    try:
        temporal_coverage_rule.validate_rule(temporal_coverage)
    except MetapypeRuleError as e:
        logger.error(e)

    taxonomic_coverage = Node(names.TAXONOMICCOVERAGE, parent=coverage)
    coverage.add_child(taxonomic_coverage)
    general_taxonomic_coverage = Node(names.GENERALTAXONOMICCOVERAGE, 
                                      parent=taxonomic_coverage)
    taxonomic_coverage.add_child(general_taxonomic_coverage)
    general_taxonomic_coverage.content = "All vascular plants were \
identified to family or species, mosses and lichens were \
identified as moss or lichen."
    
    taxonomic_classification_genus = Node(names.TAXONOMICCLASSIFICATION, 
                                          parent=taxonomic_coverage)
    taxonomic_coverage.add_child(taxonomic_classification_genus)

    taxon_rank_name_genus = Node(names.TAXONRANKNAME, 
                                 parent=taxonomic_classification_genus)
    taxonomic_classification_genus.add_child(taxon_rank_name_genus)
    taxon_rank_name_genus.content = "Genus"

    taxon_rank_value_genus = Node(names.TAXONRANKVALUE, 
                                  parent=taxonomic_classification_genus)
    taxonomic_classification_genus.add_child(taxon_rank_value_genus)
    taxon_rank_value_genus.content = "Escherichia"

    taxonomic_classification_species = Node(names.TAXONOMICCLASSIFICATION, 
                                       parent=taxonomic_classification_genus)
    taxonomic_classification_genus.add_child(taxonomic_classification_species)

    taxon_rank_name_species = Node(names.TAXONRANKNAME, 
                              parent=taxonomic_classification_species)
    taxonomic_classification_species.add_child(taxon_rank_name_species)
    taxon_rank_name_species.content = "Species"

    taxon_rank_value_species = Node(names.TAXONRANKVALUE,
                               parent=taxonomic_classification_species)
    taxonomic_classification_species.add_child(taxon_rank_value_species)
    taxon_rank_value_species.content = "coli"

    contact = Node(names.CONTACT, parent=dataset)
    dataset.add_child(contact)

    individualName_contact = Node(names.INDIVIDUALNAME, parent=contact)
    contact.add_child(individualName_contact)

    givenName_contact = Node(names.GIVENNAME, parent=individualName_contact)
    givenName_contact.content = 'Chase'
    individualName_contact.add_child(givenName_contact)

    surName_contact = Node(names.SURNAME, parent=individualName_contact)
    surName_contact.content = 'Gaucho'
    individualName_contact.add_child(surName_contact)

    datatable = Node(names.DATATABLE, parent=dataset)
    dataset.add_child(datatable)

    alternate_identifier = Node(names.ALTERNATEIDENTIFIER, parent=datatable)
    datatable.add_child(alternate_identifier)
    alternate_identifier.add_attribute('system', 'EDI')
    alternate_identifier.content = 'https://portal.edirepository.org/nis/dataviewer?packageid=edi.23.1&entityid=ce5438fb9318b1f04d06b8a0276754d6'

    entity_name = Node(names.ENTITYNAME, parent=datatable)
    datatable.add_child(entity_name)
    entity_name.content = '14CO2 data'

    entity_description = Node(names.ENTITYDESCRIPTION, parent=datatable)
    datatable.add_child(entity_description)
    entity_description.content = 'Radiocarbon content of soil-respired air'
 
    physical = Node(names.PHYSICAL, parent=datatable)
    datatable.add_child(physical)
    physical.add_attribute('system', 'EDI')

    object_name = Node(names.OBJECTNAME, parent=physical)
    physical.add_child(object_name)
    object_name.content = 'tvan_14co2.jk.data.csv'

    size = Node(names.SIZE, parent=physical)
    physical.add_child(size)
    size.add_attribute('unit', 'MB')
    size.content = '20'

    authentication = Node(names.AUTHENTICATION, parent=physical)
    physical.add_child(authentication)
    authentication.add_attribute('method', 'password')
    authentication.content = 'LDAP'

    compression_method = Node(names.COMPRESSIONMETHOD, parent=physical)
    physical.add_child(compression_method)
    compression_method.content = 'zip'

    encoding_method = Node(names.ENCODINGMETHOD, parent=physical)
    physical.add_child(encoding_method)
    encoding_method.content = 'base64'

    character_encoding = Node(names.CHARACTERENCODING, parent=physical)
    physical.add_child(character_encoding)
    character_encoding.content = 'UTF-8'

    data_format = Node(names.DATAFORMAT, parent=physical)
    physical.add_child(data_format)

    text_format = Node(names.TEXTFORMAT, parent=data_format)
    data_format.add_child(text_format)

    num_header_lines = Node(names.NUMHEADERLINES, parent=text_format)
    text_format.add_child(num_header_lines)
    num_header_lines.content = '3'
    
    num_footer_lines = Node(names.NUMFOOTERLINES, parent=text_format)
    text_format.add_child(num_footer_lines)
    num_footer_lines.content = '0'

    record_delimiter = Node(names.RECORDDELIMITER, parent=text_format)
    text_format.add_child(record_delimiter)
    record_delimiter.content = '\\r\\n'

    physical_line_delimiter = Node(names.PHYSICALLINEDELIMITER)
    text_format.add_child(physical_line_delimiter)
    physical_line_delimiter.content = '\\r\\n'

    num_physical_lines_per_record = Node(names.NUMPHYSICALLINESPERRECORD)
    text_format.add_child(num_physical_lines_per_record)
    num_physical_lines_per_record.content = '1'

    max_record_length = Node(names.MAXRECORDLENGTH)
    text_format.add_child(max_record_length)
    max_record_length.content = '597'

    attribute_orientation = Node(names.ATTRIBUTEORIENTATION)
    text_format.add_child(attribute_orientation)
    attribute_orientation.content = 'column'

    simple_delimited = Node(names.SIMPLEDELIMITED, parent=text_format)
    text_format.add_child(simple_delimited)

    field_delimiter = Node(names.FIELDDELIMITER, parent=simple_delimited)
    simple_delimited.add_child(field_delimiter)
    field_delimiter.content = '\\t'

    collapse_delimiters = Node(names.COLLAPSEDELIMITERS, parent=simple_delimited)
    simple_delimited.add_child(collapse_delimiters)
    collapse_delimiters.content = 'no'

    quote_character = Node(names.QUOTECHARACTER, parent=simple_delimited)
    simple_delimited.add_child(quote_character)
    quote_character.content = "'"

    literal_character = Node(names.LITERALCHARACTER, parent=simple_delimited)
    simple_delimited.add_child(literal_character)
    literal_character.content = '/'   # Usually a backslash, but that causes an error

    complex = Node(names.COMPLEX, parent=text_format)
    text_format.add_child(complex)

    text_fixed = Node(names.TEXTFIXED, parent=complex)
    complex.add_child(text_fixed)

    field_width = Node(names.FIELDWIDTH, parent=text_fixed)
    text_fixed.add_child(field_width)
    field_width.content = '12'

    line_number = Node(names.LINENUMBER, parent=text_fixed)
    text_fixed.add_child(line_number)
    line_number.content = '3'

    field_start_column = Node(names.FIELDSTARTCOLUMN, parent=text_fixed)
    text_fixed.add_child(field_start_column)
    field_start_column.content = '58'

    text_delimited = Node(names.TEXTDELIMITED, parent=complex)
    complex.add_child(text_delimited)

    field_delimiter_2 = Node(names.FIELDDELIMITER, parent=text_delimited)
    text_delimited.add_child(field_delimiter_2)
    field_delimiter_2.content = ','
    
    collapse_delimiters_2 = Node(names.COLLAPSEDELIMITERS, parent=text_delimited)
    text_delimited.add_child(collapse_delimiters_2)
    collapse_delimiters_2.content = 'no'

    line_number_2 = Node(names.LINENUMBER, parent=text_delimited)
    text_delimited.add_child(line_number_2)
    line_number_2.content = '2'

    quote_character_2 = Node(names.QUOTECHARACTER, parent=text_delimited)
    text_delimited.add_child(quote_character_2)
    quote_character_2.content = "'"

    literal_character_2 = Node(names.LITERALCHARACTER, parent=text_delimited)
    text_delimited.add_child(literal_character_2)
    literal_character_2.content = '/'   # Usually a backslash, but that causes an error

    externally_defined_format = Node(names.EXTERNALLYDEFINEDFORMAT, parent=data_format)
    data_format.add_child(externally_defined_format)

    format_name = Node(names.FORMATNAME, parent=externally_defined_format)
    externally_defined_format.add_child(format_name)
    format_name.content = 'Microsoft Excel'

    format_version = Node(names.FORMATVERSION, parent=externally_defined_format)
    externally_defined_format.add_child(format_version)
    format_version.content = '2000 (9.0.2720)'

    binary_raster_format = Node(names.BINARYRASTERFORMAT, parent=data_format)
    data_format.add_child(binary_raster_format)

    row_column_orientation = Node(names.ROWCOLUMNORIENTATION, parent=binary_raster_format)
    binary_raster_format.add_child(row_column_orientation)
    row_column_orientation.content = 'column'

    multi_band = Node(names.MULTIBAND, parent=binary_raster_format)
    binary_raster_format.add_child(multi_band)

    nbands = Node(names.NBANDS, parent=multi_band)
    multi_band.add_child(nbands)
    nbands.content = '2'

    layout = Node(names.LAYOUT, parent=multi_band)
    multi_band.add_child(layout)
    layout.content = 'bil'

    nbits = Node(names.NBITS, parent=binary_raster_format)
    binary_raster_format.add_child(nbits)
    nbits.content = '16'

    byteorder = Node(names.BYTEORDER, parent=binary_raster_format)
    binary_raster_format.add_child(byteorder)
    byteorder.content = 'little-endian'

    skipbytes = Node(names.SKIPBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(skipbytes)
    skipbytes.content = '0'

    bandrowbytes = Node(names.BANDROWBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(bandrowbytes)
    bandrowbytes.content = '3'

    totalrowbytes = Node(names.TOTALROWBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(totalrowbytes)
    totalrowbytes.content = '8'

    bandgapbytes = Node(names.BANDGAPBYTES, parent= binary_raster_format)
    binary_raster_format.add_child(bandgapbytes)
    bandgapbytes.content = '1'

    distribution = Node(names.DISTRIBUTION, parent=physical)
    physical.add_child(distribution)

    online = Node(names.ONLINE, parent=distribution)
    distribution.add_child(online)

    online_description = Node(names.ONLINEDESCRIPTION, parent=online)
    online.add_child(online_description)
    online_description.content = 'network server'

    url = Node(names.URL, parent=online)
    online.add_child(url)
    url.add_attribute('function', 'download')
    url.content = 'https://data.abc.edu/somedataset/data'

    connection = Node(names.CONNECTION, parent=online)
    online.add_child(connection)
    connection.content = 'This is not a real connection element because it is only a string.'

    datatable_rule = rule.get_rule(names.DATATABLE)
    try:
        datatable_rule.validate_rule(datatable)
    except MetapypeRuleError as e:
        logger.error(e)

    text_format_rule = rule.get_rule(names.TEXTFORMAT)
    try:
        text_format_rule.validate_rule(text_format)
    except MetapypeRuleError as e:
        logger.error(e)

    online_rule = rule.get_rule(names.ONLINE)
    try:
        online_rule.validate_rule(online)
    except MetapypeRuleError as e:
        logger.error(e)

    node = Node.get_node_instance(access.id)

    access_rule = rule.get_rule(names.ACCESS)
    
    try:
        access_rule.validate_rule(access)
    except MetapypeRuleError as e:
        logger.error(e)
    print(access_rule.attributes)
    print(access_rule.children)
    print(access_rule.content_rules)

    try:
        validate.node(access)
    except MetapypeRuleError as e:
        logger.error(e)

    try:
        validate.tree(eml)
    except  MetapypeRuleError as e:
        logger.error(e)

    print(evaluate.node(title))

    io.graph(eml, 0)

    attr = access_rule.attributes
    print(attr)
    children = access_rule.children
    print(children)

    print(access.list_attributes())

    json_str = io.to_json(eml)
    print(json_str)
    with open('test_eml.json', 'w') as f:
        f.write(json_str)

    m = json.loads(json_str)
    node = io.from_json(m)

    try:
        validate.tree(node)
    except  MetapypeRuleError as e:
        logger.error(e)
    #
    xml = export.to_xml(eml)
    print(xml)
    with open('test_eml.xml', 'w') as f:
        f.write(xml)


    evaluation = {}
    evaluate.tree(eml, evaluation)
    for e in evaluation:
        print('{0}: {1}'.format(e, evaluation[e]))

    return 0


if __name__ == "__main__":
    main()

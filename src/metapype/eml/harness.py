#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: harness

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    6/5/18
"""
import json
import logging
import os

import daiquiri

from metapype.eml.exceptions import MetapypeRuleError
from metapype.eml import export
from metapype.eml import evaluate
from metapype.eml import names
from metapype.eml import rule
from metapype.eml import validate
from metapype.model import mp_io
from metapype.model import metapype_io
from metapype.model.node import Node

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/harness.log"
daiquiri.setup(
    level=logging.INFO, outputs=(daiquiri.output.File(logfile), "stdout",)
)
logger = daiquiri.getLogger(__name__)


def main():

    eml = Node(names.EML)
    eml.add_attribute("packageId", "edi.23.1")
    eml.add_attribute("system", "metapype")

    access = Node(names.ACCESS, parent=eml)
    access.add_attribute("authSystem", "pasta")
    access.add_attribute("order", "allowFirst")
    eml.add_child(access)

    allow = Node(names.ALLOW, parent=access)
    access.add_child(allow)

    principal = Node(names.PRINCIPAL, parent=allow)
    principal.content = "uid=gaucho,o=EDI,dc=edirepository,dc=org"
    allow.add_child(principal)

    permission = Node(names.PERMISSION, parent=allow)
    permission.content = "all"
    allow.add_child(permission)

    dataset = Node(names.DATASET, parent=eml)
    eml.add_child(dataset)

    title = Node(names.TITLE, parent=dataset)
    title.content = "Green sea turtle counts: Tortuga Island 20017"
    dataset.add_child(title)

    creator = Node(names.CREATOR, parent=dataset)
    dataset.add_child(creator)

    individualName_creator = Node(names.INDIVIDUALNAME, parent=creator)
    creator.add_child(individualName_creator)

    surName_creator = Node(names.SURNAME, parent=individualName_creator)
    surName_creator.content = "Gaucho"
    individualName_creator.add_child(surName_creator)

    pubdate = Node(names.PUBDATE, parent=dataset)
    pubdate.content = "2018"
    dataset.add_child(pubdate)

    abstract = Node(names.ABSTRACT, parent=dataset)
    dataset.add_child(abstract)

    section_1 = Node(names.SECTION, parent=abstract)
    abstract.add_child(section_1)

    section_2 = Node(names.SECTION, parent=abstract)
    abstract.add_child(section_2)

    para_1 = Node(names.PARA, parent=section_1)
    section_1.add_child(para_1)
    para_1.content = "This is abstract Para 1"

    para_2 = Node(names.PARA, parent=section_2)
    section_2.add_child(para_2)
    para_2.content = "This is abstract Para 2"

    intellectualRights = Node(names.INTELLECTUALRIGHTS, parent=dataset)
    dataset.add_child(intellectualRights)

    section_3 = Node(names.SECTION, parent=intellectualRights)
    intellectualRights.add_child(section_3)

    section_4 = Node(names.SECTION, parent=intellectualRights)
    intellectualRights.add_child(section_4)

    para_3 = Node(names.PARA, parent=section_3)
    section_3.add_child(para_3)
    para_3.content = "This is intellectualRights Para 3"

    para_4 = Node(names.PARA, parent=section_4)
    section_4.add_child(para_4)
    para_4.content = "This is intellectualRights Para 4"

    coverage = Node(names.COVERAGE, parent=dataset)
    dataset.add_child(coverage)
    geographic_coverage = Node(names.GEOGRAPHICCOVERAGE, parent=coverage)
    coverage.add_child(geographic_coverage)
    geographic_description = Node(
        names.GEOGRAPHICDESCRIPTION, parent=geographic_coverage
    )
    geographic_description.content = "Somewhere in the Rocky Mountains"
    geographic_coverage.add_child(geographic_description)
    bounding_coordinates = Node(
        names.BOUNDINGCOORDINATES, parent=geographic_coverage
    )
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

    # single_date_time = Node(names.SINGLEDATETIME, parent=temporal_coverage)
    # temporal_coverage.add_child(single_date_time)
    # single_date_time.content = "2018"

    range_of_dates = Node(names.RANGEOFDATES, parent=temporal_coverage)
    temporal_coverage.add_child(range_of_dates)

    begin_date = Node(names.BEGINDATE, parent=range_of_dates)
    range_of_dates.add_child(begin_date)

    calendar_date_begin = Node(names.CALENDARDATE, parent=begin_date)
    begin_date.add_child(calendar_date_begin)
    calendar_date_begin.content = "2000"

    end_date = Node(names.ENDDATE, parent=range_of_dates)
    range_of_dates.add_child(end_date)

    calendar_date_end = Node(names.CALENDARDATE, parent=end_date)
    end_date.add_child(calendar_date_end)
    calendar_date_end.content = "2018"

    temporal_coverage_rule = rule.get_rule(names.TEMPORALCOVERAGE)
    try:
        temporal_coverage_rule.validate_rule(temporal_coverage)
    except MetapypeRuleError as e:
        # We should see an error like:
        #   Maximum occurrence of "['singleDateTime', 'rangeOfDates']"
        #   exceeded for "temporalCoverage"
        logger.error(e)

    taxonomic_coverage = Node(names.TAXONOMICCOVERAGE, parent=coverage)
    coverage.add_child(taxonomic_coverage)
    general_taxonomic_coverage = Node(
        names.GENERALTAXONOMICCOVERAGE, parent=taxonomic_coverage
    )
    taxonomic_coverage.add_child(general_taxonomic_coverage)
    general_taxonomic_coverage.content = "All vascular plants were \
identified to family or species, mosses and lichens were \
identified as moss or lichen."

    taxonomic_classification_genus = Node(
        names.TAXONOMICCLASSIFICATION, parent=taxonomic_coverage
    )
    taxonomic_coverage.add_child(taxonomic_classification_genus)

    taxon_rank_name_genus = Node(
        names.TAXONRANKNAME, parent=taxonomic_classification_genus
    )
    taxonomic_classification_genus.add_child(taxon_rank_name_genus)
    taxon_rank_name_genus.content = "Genus"

    taxon_rank_value_genus = Node(
        names.TAXONRANKVALUE, parent=taxonomic_classification_genus
    )
    taxonomic_classification_genus.add_child(taxon_rank_value_genus)
    taxon_rank_value_genus.content = "Escherichia"

    taxonomic_classification_species = Node(
        names.TAXONOMICCLASSIFICATION, parent=taxonomic_classification_genus
    )
    taxonomic_classification_genus.add_child(taxonomic_classification_species)

    taxon_rank_name_species = Node(
        names.TAXONRANKNAME, parent=taxonomic_classification_species
    )
    taxonomic_classification_species.add_child(taxon_rank_name_species)
    taxon_rank_name_species.content = "Species"

    taxon_rank_value_species = Node(
        names.TAXONRANKVALUE, parent=taxonomic_classification_species
    )
    taxonomic_classification_species.add_child(taxon_rank_value_species)
    taxon_rank_value_species.content = "coli"

    contact = Node(names.CONTACT, parent=dataset)
    dataset.add_child(contact)

    individualName_contact = Node(names.INDIVIDUALNAME, parent=contact)
    contact.add_child(individualName_contact)

    givenName_contact = Node(names.GIVENNAME, parent=individualName_contact)
    givenName_contact.content = "Chase"
    individualName_contact.add_child(givenName_contact)

    surName_contact = Node(names.SURNAME, parent=individualName_contact)
    surName_contact.content = "Gaucho"
    individualName_contact.add_child(surName_contact)

    publisher = Node(names.PUBLISHER, parent=dataset)
    dataset.add_child(publisher)

    individualName_publisher = Node(names.INDIVIDUALNAME, parent=publisher)
    publisher.add_child(individualName_publisher)

    givenName_publisher = Node(
        names.GIVENNAME, parent=individualName_publisher
    )
    givenName_publisher.content = "Utah"
    individualName_publisher.add_child(givenName_publisher)

    surName_publisher = Node(names.SURNAME, parent=individualName_publisher)
    surName_publisher.content = "Carroll"
    individualName_publisher.add_child(surName_publisher)

    pubplace = Node(names.PUBPLACE, parent=dataset)
    dataset.add_child(pubplace)
    pubplace.content = "University of New Mexico Dept. of Biology"

    methods = Node(names.METHODS, parent=dataset)
    dataset.add_child(methods)

    method_step = Node(names.METHODSTEP, parent=methods)
    methods.add_child(method_step)

    description = Node(names.DESCRIPTION, parent=method_step)
    method_step.add_child(description)

    section_1 = Node(names.SECTION, parent=description)
    description.add_child(section_1)

    section_2 = Node(names.SECTION, parent=description)
    description.add_child(section_2)

    para_1 = Node(names.PARA, parent=section_1)
    section_1.add_child(para_1)
    para_1.content = "This is description Para 1"

    para_2 = Node(names.PARA, parent=section_2)
    section_2.add_child(para_2)
    para_2.content = "This is description Para 2"

    instrumentation_1 = Node(names.INSTRUMENTATION, parent=method_step)
    method_step.add_child(instrumentation_1)
    instrumentation_1.content = "Instrument #1"

    instrumentation_2 = Node(names.INSTRUMENTATION, parent=method_step)
    method_step.add_child(instrumentation_2)
    instrumentation_2.content = "Instrument #2"

    sampling = Node(names.SAMPLING, parent=methods)
    methods.add_child(sampling)

    study_extent = Node(names.STUDYEXTENT, parent=sampling)
    sampling.add_child(study_extent)

    study_extent_coverage = Node(names.COVERAGE, parent=study_extent)
    study_extent.add_child(study_extent_coverage)

    study_extent_geographic_coverage = Node(
        names.GEOGRAPHICCOVERAGE, parent=study_extent_coverage
    )
    study_extent_coverage.add_child(study_extent_geographic_coverage)

    study_extent_geographic_description = Node(
        names.GEOGRAPHICDESCRIPTION, parent=study_extent_geographic_coverage
    )
    study_extent_geographic_description.content = (
        "Somewhere in the Rocky Mountains"
    )
    study_extent_geographic_coverage.add_child(
        study_extent_geographic_description
    )

    study_extent_bounding_coordinates = Node(
        names.BOUNDINGCOORDINATES, parent=study_extent_geographic_coverage
    )
    study_extent_geographic_coverage.add_child(
        study_extent_bounding_coordinates
    )

    study_extent_wbc = Node(
        names.WESTBOUNDINGCOORDINATE, parent=study_extent_bounding_coordinates
    )
    study_extent_wbc.content = -107.55538624999997
    study_extent_bounding_coordinates.add_child(study_extent_wbc)
    study_extent_ebc = Node(
        names.EASTBOUNDINGCOORDINATE, parent=study_extent_bounding_coordinates
    )
    study_extent_ebc.content = -106.45675343749997
    study_extent_bounding_coordinates.add_child(study_extent_ebc)
    study_extent_nbc = Node(
        names.NORTHBOUNDINGCOORDINATE, parent=study_extent_bounding_coordinates
    )
    study_extent_nbc.content = 39.48496522541802
    study_extent_bounding_coordinates.add_child(study_extent_nbc)
    study_extent_sbc = Node(
        names.SOUTHBOUNDINGCOORDINATE, parent=study_extent_bounding_coordinates
    )
    study_extent_sbc.content = 38.9530013453599
    study_extent_bounding_coordinates.add_child(study_extent_sbc)

    study_extent_temporal_coverage = Node(
        names.TEMPORALCOVERAGE, parent=study_extent_coverage
    )
    study_extent_coverage.add_child(study_extent_temporal_coverage)

    study_extent_single_date_time = Node(
        names.SINGLEDATETIME, parent=study_extent_temporal_coverage
    )
    study_extent_temporal_coverage.add_child(study_extent_single_date_time)

    study_extent_calendar_date = Node(names.CALENDARDATE)
    study_extent_calendar_date.content = "2018"
    study_extent_single_date_time.add_child(study_extent_calendar_date)
    study_extent_time = Node(names.TIME)
    study_extent_time.content = "14:34:32.001-06:00"
    study_extent_single_date_time.add_child(study_extent_time)

    study_extent_range_of_dates = Node(
        names.RANGEOFDATES, parent=study_extent_temporal_coverage
    )
    # study_extent_temporal_coverage.add_child(study_extent_range_of_dates)

    study_extent_begin_date = Node(
        names.BEGINDATE, parent=study_extent_range_of_dates
    )
    study_extent_range_of_dates.add_child(study_extent_begin_date)

    study_extent_calendar_date_begin = Node(
        names.CALENDARDATE, parent=study_extent_begin_date
    )
    study_extent_begin_date.add_child(study_extent_calendar_date_begin)
    study_extent_calendar_date_begin.content = "2000"

    study_extent_end_date = Node(
        names.ENDDATE, parent=study_extent_range_of_dates
    )
    study_extent_range_of_dates.add_child(study_extent_end_date)

    study_extent_calendar_date_end = Node(
        names.CALENDARDATE, parent=study_extent_end_date
    )
    study_extent_end_date.add_child(study_extent_calendar_date_end)
    study_extent_calendar_date_end.content = "2018"

    study_extent_temporal_coverage_rule = rule.get_rule(names.TEMPORALCOVERAGE)
    try:
        study_extent_temporal_coverage_rule.validate_rule(temporal_coverage)
    except MetapypeRuleError as e:
        # We should see an error like:
        #   Maximum occurrence of "['singleDateTime', 'rangeOfDates']"
        #   exceeded for "temporalCoverage"
        logger.error(e)

    study_extent_taxonomic_coverage = Node(
        names.TAXONOMICCOVERAGE, parent=study_extent_coverage
    )
    study_extent_coverage.add_child(study_extent_taxonomic_coverage)
    study_extent_general_taxonomic_coverage = Node(
        names.GENERALTAXONOMICCOVERAGE, parent=study_extent_taxonomic_coverage
    )
    study_extent_taxonomic_coverage.add_child(
        study_extent_general_taxonomic_coverage
    )
    study_extent_general_taxonomic_coverage.content = "All vascular plants were \
identified to family or species, mosses and lichens were \
identified as moss or lichen."

    study_extent_taxonomic_classification_genus = Node(
        names.TAXONOMICCLASSIFICATION, parent=study_extent_taxonomic_coverage
    )
    study_extent_taxonomic_coverage.add_child(
        study_extent_taxonomic_classification_genus
    )

    study_extent_taxon_rank_name_genus = Node(
        names.TAXONRANKNAME, parent=study_extent_taxonomic_classification_genus
    )
    study_extent_taxonomic_classification_genus.add_child(
        study_extent_taxon_rank_name_genus
    )
    study_extent_taxon_rank_name_genus.content = "Genus"

    study_extent_taxon_rank_value_genus = Node(
        names.TAXONRANKVALUE,
        parent=study_extent_taxonomic_classification_genus,
    )
    study_extent_taxonomic_classification_genus.add_child(
        study_extent_taxon_rank_value_genus
    )
    study_extent_taxon_rank_value_genus.content = "Escherichia"

    study_extent_taxonomic_classification_species = Node(
        names.TAXONOMICCLASSIFICATION,
        parent=study_extent_taxonomic_classification_genus,
    )
    study_extent_taxonomic_classification_genus.add_child(
        study_extent_taxonomic_classification_species
    )

    study_extent_taxon_rank_name_species = Node(
        names.TAXONRANKNAME,
        parent=study_extent_taxonomic_classification_species,
    )
    study_extent_taxonomic_classification_species.add_child(
        study_extent_taxon_rank_name_species
    )
    study_extent_taxon_rank_name_species.content = "Species"

    study_extent_taxon_rank_value_species = Node(
        names.TAXONRANKVALUE,
        parent=study_extent_taxonomic_classification_species,
    )
    study_extent_taxonomic_classification_species.add_child(
        study_extent_taxon_rank_value_species
    )
    study_extent_taxon_rank_value_species.content = "coli"

    study_extent_description = Node(names.DESCRIPTION, parent=study_extent)
    study_extent.add_child(study_extent_description)

    study_extent_section_1 = Node(
        names.SECTION, parent=study_extent_description
    )
    study_extent_description.add_child(study_extent_section_1)

    study_extent_section_2 = Node(
        names.SECTION, parent=study_extent_description
    )
    study_extent_description.add_child(study_extent_section_2)

    study_extent_para_1 = Node(names.PARA, parent=study_extent_section_1)
    study_extent_section_1.add_child(study_extent_para_1)
    study_extent_para_1.content = "This is study_extent_description Para 1"

    study_extent_para_2 = Node(names.PARA, parent=study_extent_section_2)
    study_extent_section_2.add_child(study_extent_para_2)
    study_extent_para_2.content = "This is study_extent_description Para 2"

    sampling_description = Node(names.SAMPLINGDESCRIPTION, parent=sampling)
    sampling.add_child(sampling_description)

    sampling_description_section_1 = Node(
        names.SECTION, parent=sampling_description
    )
    sampling_description.add_child(sampling_description_section_1)

    sampling_description_section_2 = Node(
        names.SECTION, parent=sampling_description
    )
    sampling_description.add_child(sampling_description_section_2)

    sampling_description_para_1 = Node(names.PARA, parent=sampling_description_section_1)
    sampling_description_section_1.add_child(sampling_description_para_1)
    sampling_description_para_1.content = "This is sampling_description Para 1"

    sampling_description_para_2 = Node(names.PARA, parent=sampling_description_section_2)
    sampling_description_section_2.add_child(sampling_description_para_2)
    sampling_description_para_2.content = "This is sampling_description Para 2"

    quality_control = Node(names.QUALITYCONTROL, parent=methods)
    methods.add_child(quality_control)

    quality_control_description = Node(
        names.DESCRIPTION, parent=quality_control
    )
    quality_control.add_child(quality_control_description)

    quality_control_description_section_1 = Node(
        names.SECTION, parent=quality_control_description
    )
    quality_control_description.add_child(
        quality_control_description_section_1
    )

    quality_control_description_section_2 = Node(
        names.SECTION, parent=quality_control_description
    )
    quality_control_description.add_child(
        quality_control_description_section_2
    )

    quality_control_description_para_1 = Node(
        names.PARA, parent=quality_control_description_section_1
    )
    quality_control_description_section_1.add_child(quality_control_description_para_1)
    quality_control_description_para_1.content = (
        "This is quality_control_description Para 1"
    )

    quality_control_description_para_2 = Node(
        names.PARA, parent=quality_control_description_section_2
    )
    quality_control_description_section_2.add_child(quality_control_description_para_2)
    quality_control_description_para_2.content = (
        "This is quality_control_description Para 2"
    )

    quality_control_instrumentation_1 = Node(
        names.INSTRUMENTATION, parent=quality_control
    )
    quality_control.add_child(quality_control_instrumentation_1)
    quality_control_instrumentation_1.content = (
        "Quality Control Instrumentation string 1"
    )

    quality_control_instrumentation_2 = Node(
        names.INSTRUMENTATION, parent=quality_control
    )
    quality_control.add_child(quality_control_instrumentation_2)
    quality_control_instrumentation_2.content = (
        "Quality Control Instrumentation string 2"
    )

    project = Node(names.PROJECT, parent=dataset)
    dataset.add_child(project)

    project_title = Node(names.TITLE, parent=project)
    project.add_child(project_title)
    project_title.content = "The Title of the Project"

    personnel = Node(names.PERSONNEL, parent=project)
    project.add_child(personnel)

    individualName_personnel = Node(names.INDIVIDUALNAME, parent=personnel)
    personnel.add_child(individualName_personnel)

    givenName_personnel = Node(
        names.GIVENNAME, parent=individualName_personnel
    )
    givenName_personnel.content = "Baxter"
    individualName_personnel.add_child(givenName_personnel)

    surName_personnel = Node(names.SURNAME, parent=individualName_personnel)
    surName_personnel.content = "Duffington"
    individualName_personnel.add_child(surName_personnel)

    project_role = Node(names.ROLE, parent=personnel)
    personnel.add_child(project_role)
    project_role.content = "principalInvestigator"

    datatable = Node(names.DATATABLE, parent=dataset)
    dataset.add_child(datatable)

    alternate_identifier = Node(names.ALTERNATEIDENTIFIER, parent=datatable)
    datatable.add_child(alternate_identifier)
    alternate_identifier.add_attribute("system", "EDI")
    alternate_identifier.content = "https://portal.edirepository.org/nis/dataviewer?packageid=edi.23.1&entityid=ce5438fb9318b1f04d06b8a0276754d6"

    entity_name = Node(names.ENTITYNAME, parent=datatable)
    datatable.add_child(entity_name)
    entity_name.content = "14CO2 data"

    entity_description = Node(names.ENTITYDESCRIPTION, parent=datatable)
    datatable.add_child(entity_description)
    entity_description.content = "Radiocarbon content of soil-respired air"

    physical = Node(names.PHYSICAL, parent=datatable)
    datatable.add_child(physical)
    physical.add_attribute("system", "EDI")

    object_name = Node(names.OBJECTNAME, parent=physical)
    physical.add_child(object_name)
    object_name.content = "tvan_14co2.jk.data.csv"

    size = Node(names.SIZE, parent=physical)
    physical.add_child(size)
    size.add_attribute("unit", "MB")
    size.content = "20"

    authentication = Node(names.AUTHENTICATION, parent=physical)
    physical.add_child(authentication)
    authentication.add_attribute("method", "MD5")
    authentication.content = "7c9e8eb43ab7b52fa9b1db7de756d6a2"

    compression_method = Node(names.COMPRESSIONMETHOD, parent=physical)
    physical.add_child(compression_method)
    compression_method.content = "zip"

    encoding_method = Node(names.ENCODINGMETHOD, parent=physical)
    physical.add_child(encoding_method)
    encoding_method.content = "base64"

    character_encoding = Node(names.CHARACTERENCODING, parent=physical)
    physical.add_child(character_encoding)
    character_encoding.content = "UTF-8"

    data_format = Node(names.DATAFORMAT, parent=physical)
    physical.add_child(data_format)

    text_format = Node(names.TEXTFORMAT, parent=data_format)
    data_format.add_child(text_format)

    num_header_lines = Node(names.NUMHEADERLINES, parent=text_format)
    text_format.add_child(num_header_lines)
    num_header_lines.content = "3"

    num_footer_lines = Node(names.NUMFOOTERLINES, parent=text_format)
    text_format.add_child(num_footer_lines)
    num_footer_lines.content = "0"

    record_delimiter = Node(names.RECORDDELIMITER, parent=text_format)
    text_format.add_child(record_delimiter)
    record_delimiter.content = "\\r\\n"

    physical_line_delimiter = Node(
        names.PHYSICALLINEDELIMITER, parent=text_format
    )
    text_format.add_child(physical_line_delimiter)
    physical_line_delimiter.content = "\\r\\n"

    num_physical_lines_per_record = Node(
        names.NUMPHYSICALLINESPERRECORD, parent=text_format
    )
    text_format.add_child(num_physical_lines_per_record)
    num_physical_lines_per_record.content = "1"

    max_record_length = Node(names.MAXRECORDLENGTH, parent=text_format)
    text_format.add_child(max_record_length)
    max_record_length.content = "597"

    attribute_orientation = Node(
        names.ATTRIBUTEORIENTATION, parent=text_format
    )
    text_format.add_child(attribute_orientation)
    attribute_orientation.content = "column"

    simple_delimited = Node(names.SIMPLEDELIMITED, parent=text_format)
    text_format.add_child(simple_delimited)

    field_delimiter = Node(names.FIELDDELIMITER, parent=simple_delimited)
    simple_delimited.add_child(field_delimiter)
    field_delimiter.content = "\\t"

    collapse_delimiters = Node(
        names.COLLAPSEDELIMITERS, parent=simple_delimited
    )
    simple_delimited.add_child(collapse_delimiters)
    collapse_delimiters.content = "no"

    quote_character = Node(names.QUOTECHARACTER, parent=simple_delimited)
    simple_delimited.add_child(quote_character)
    quote_character.content = "'"

    literal_character = Node(names.LITERALCHARACTER, parent=simple_delimited)
    simple_delimited.add_child(literal_character)
    literal_character.content = (
        "/"  # Usually a backslash, but that causes an error
    )

    complex = Node(names.COMPLEX, parent=text_format)
    # text_format.add_child(complex)

    text_fixed = Node(names.TEXTFIXED, parent=complex)
    complex.add_child(text_fixed)

    field_width = Node(names.FIELDWIDTH, parent=text_fixed)
    text_fixed.add_child(field_width)
    field_width.content = "12"

    line_number = Node(names.LINENUMBER, parent=text_fixed)
    text_fixed.add_child(line_number)
    line_number.content = "3"

    field_start_column = Node(names.FIELDSTARTCOLUMN, parent=text_fixed)
    text_fixed.add_child(field_start_column)
    field_start_column.content = "58"

    text_delimited = Node(names.TEXTDELIMITED, parent=complex)
    complex.add_child(text_delimited)

    field_delimiter_2 = Node(names.FIELDDELIMITER, parent=text_delimited)
    text_delimited.add_child(field_delimiter_2)
    field_delimiter_2.content = ","

    collapse_delimiters_2 = Node(
        names.COLLAPSEDELIMITERS, parent=text_delimited
    )
    text_delimited.add_child(collapse_delimiters_2)
    collapse_delimiters_2.content = "no"

    line_number_2 = Node(names.LINENUMBER, parent=text_delimited)
    text_delimited.add_child(line_number_2)
    line_number_2.content = "2"

    quote_character_2 = Node(names.QUOTECHARACTER, parent=text_delimited)
    text_delimited.add_child(quote_character_2)
    quote_character_2.content = "'"

    literal_character_2 = Node(names.LITERALCHARACTER, parent=text_delimited)
    text_delimited.add_child(literal_character_2)
    literal_character_2.content = (
        "/"  # Usually a backslash, but that causes an error
    )

    externally_defined_format = Node(
        names.EXTERNALLYDEFINEDFORMAT, parent=data_format
    )

    format_name = Node(names.FORMATNAME, parent=externally_defined_format)
    externally_defined_format.add_child(format_name)
    format_name.content = "Microsoft Excel"

    format_version = Node(
        names.FORMATVERSION, parent=externally_defined_format
    )
    externally_defined_format.add_child(format_version)
    format_version.content = "2000 (9.0.2720)"

    binary_raster_format = Node(names.BINARYRASTERFORMAT, parent=data_format)

    row_column_orientation = Node(
        names.ROWCOLUMNORIENTATION, parent=binary_raster_format
    )
    binary_raster_format.add_child(row_column_orientation)
    row_column_orientation.content = "column"

    multi_band = Node(names.MULTIBAND, parent=binary_raster_format)
    binary_raster_format.add_child(multi_band)

    nbands = Node(names.NBANDS, parent=multi_band)
    multi_band.add_child(nbands)
    nbands.content = "2"

    layout = Node(names.LAYOUT, parent=multi_band)
    multi_band.add_child(layout)
    layout.content = "bil"

    nbits = Node(names.NBITS, parent=binary_raster_format)
    binary_raster_format.add_child(nbits)
    nbits.content = "16"

    byteorder = Node(names.BYTEORDER, parent=binary_raster_format)
    binary_raster_format.add_child(byteorder)
    byteorder.content = "little-endian"

    skipbytes = Node(names.SKIPBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(skipbytes)
    skipbytes.content = "0"

    bandrowbytes = Node(names.BANDROWBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(bandrowbytes)
    bandrowbytes.content = "3"

    totalrowbytes = Node(names.TOTALROWBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(totalrowbytes)
    totalrowbytes.content = "8"

    bandgapbytes = Node(names.BANDGAPBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(bandgapbytes)
    bandgapbytes.content = "1"

    distribution = Node(names.DISTRIBUTION, parent=physical)
    physical.add_child(distribution)

    online = Node(names.ONLINE, parent=distribution)
    distribution.add_child(online)

    online_description = Node(names.ONLINEDESCRIPTION, parent=online)
    online.add_child(online_description)
    online_description.content = "network server"

    url = Node(names.URL, parent=online)
    online.add_child(url)
    url.add_attribute("function", "download")
    url.content = "https://data.abc.edu/somedataset/data"

    # connection = Node(names.CONNECTION, parent=online)
    # online.add_child(connection)
    # connection.content = (
    #     "This is not a real connection element because it is only a string."
    # )

    offline = Node(names.OFFLINE, parent=distribution)

    medium_name = Node(names.MEDIUMNAME, parent=offline)
    offline.add_child(medium_name)
    medium_name.content = "hardcopy"

    medium_density = Node(names.MEDIUMDENSITY, parent=offline)
    offline.add_child(medium_density)
    medium_density.content = "High Density (HD)"

    medium_density_units = Node(names.MEDIUMDENSITYUNITS, parent=offline)
    offline.add_child(medium_density_units)
    medium_density_units.content = "B/cm"

    medium_volume = Node(names.MEDIUMVOLUME, parent=offline)
    offline.add_child(medium_volume)
    medium_volume.content = "650 MB"

    medium_format = Node(names.MEDIUMFORMAT, parent=offline)
    offline.add_child(medium_format)
    medium_format.content = "NTFS"

    medium_note = Node(names.MEDIUMNOTE, parent=offline)
    offline.add_child(medium_note)
    medium_note.content = (
        "Some additional pertinent information about the media"
    )

    inline = Node(names.INLINE, parent=distribution)
    inline.content = "1,2,3,4,5,6,7,8,9"

    datatable_access = Node(names.ACCESS, parent=distribution)
    datatable_access.add_attribute("authSystem", "pasta")
    datatable_access.add_attribute("order", "allowFirst")
    distribution.add_child(datatable_access)

    datatable_allow = Node(names.ALLOW, parent=datatable_access)
    datatable_access.add_child(datatable_allow)

    datatable_principal = Node(names.PRINCIPAL, parent=datatable_allow)
    datatable_principal.content = "uid=ucarroll,o=EDI,dc=edirepository,dc=org"
    datatable_allow.add_child(datatable_principal)

    datatable_permission = Node(names.PERMISSION, parent=datatable_allow)
    datatable_permission.content = "write"
    datatable_allow.add_child(datatable_permission)

    attribute_list = Node(names.ATTRIBUTELIST, parent=datatable)
    datatable.add_child(attribute_list)

    attribute_1 = Node(names.ATTRIBUTE, parent=attribute_list)
    attribute_list.add_child(attribute_1)
    attribute_name_1 = Node(names.ATTRIBUTENAME, parent=attribute_1)
    attribute_1.add_child(attribute_name_1)
    attribute_name_1.content = "att-1"
    att_label_1 = Node(names.ATTRIBUTELABEL, parent=attribute_1)
    attribute_1.add_child(att_label_1)
    att_label_1.content = "Attribute Label 1"
    att_def_1 = Node(names.ATTRIBUTEDEFINITION)
    att_def_1.content = "Attribute 1 definition"
    attribute_1.add_child(att_def_1)
    ms_1 = Node(names.MEASUREMENTSCALE, parent=attribute_1)
    attribute_1.add_child(ms_1)
    nominal = Node(names.NOMINAL, parent=ms_1)
    ms_1.add_child(nominal)
    non_numeric_domain_1 = Node(names.NONNUMERICDOMAIN, parent=nominal)
    nominal.add_child(non_numeric_domain_1)
    enumerated_domain = Node(
        names.ENUMERATEDDOMAIN, parent=non_numeric_domain_1
    )
    non_numeric_domain_1.add_child(enumerated_domain)
    enumerated_domain.add_attribute("enforced", "yes")
    code_definition = Node(names.CODEDEFINITION, parent=enumerated_domain)
    enumerated_domain.add_child(code_definition)
    code_definition.add_attribute("order", "3")
    code = Node(names.CODE, parent=code_definition)
    code_definition.add_child(code)
    code.content = "HIGH"
    definition = Node(names.DEFINITION, parent=code_definition)
    code_definition.add_child(definition)
    definition.content = "high density, above 10 per square meter"
    source = Node(names.SOURCE, parent=code_definition)
    code_definition.add_child(source)
    source.content = "ISO country codes"
    external_code_set = Node(names.EXTERNALCODESET, parent=enumerated_domain)
    # enumerated_domain.add_child(external_code_set)
    codeset_name = Node(names.CODESETNAME, parent=external_code_set)
    external_code_set.add_child(codeset_name)
    codeset_name.content = "FIPS State Abbreviation Codes"
    citation = Node(names.CITATION, parent=external_code_set)
    external_code_set.add_child(citation)
    citation.content = "This is not an actual citation element"
    codeset_url = Node(names.CODESETURL, parent=external_code_set)
    external_code_set.add_child(codeset_url)
    codeset_url.content = (
        "https://codesets.abc.edu/fips_state_abbreviation_codes"
    )
    entity_code_list = Node(names.ENTITYCODELIST, parent=enumerated_domain)
    # enumerated_domain.add_child(entity_code_list)
    entity_reference = Node(names.ENTITYREFERENCE, parent=entity_code_list)
    entity_code_list.add_child(entity_reference)
    entity_reference.content = "entity_id_1"
    value_attribute_reference = Node(
        names.VALUEATTRIBUTEREFERENCE, parent=entity_code_list
    )
    entity_code_list.add_child(value_attribute_reference)
    value_attribute_reference.content = "attribute_id_1"
    definition_attribute_reference = Node(
        names.DEFINITIONATTRIBUTEREFERENCE, parent=entity_code_list
    )
    entity_code_list.add_child(definition_attribute_reference)
    definition_attribute_reference.content = "attribute_id_1"
    order_attribute_reference = Node(
        names.ORDERATTRIBUTEREFERENCE, parent=entity_code_list
    )
    entity_code_list.add_child(order_attribute_reference)
    order_attribute_reference.content = "attribute_id_1"

    attribute_2 = Node(names.ATTRIBUTE, parent=attribute_list)
    attribute_list.add_child(attribute_2)
    attribute_name_2 = Node(names.ATTRIBUTENAME, parent=attribute_2)
    attribute_2.add_child(attribute_name_2)
    attribute_name_2.content = "att-2"
    att_label_2 = Node(names.ATTRIBUTELABEL, parent=attribute_2)
    attribute_2.add_child(att_label_2)
    att_label_2.content = "Attribute Label 2"
    att_def_2 = Node(names.ATTRIBUTEDEFINITION)
    att_def_2.content = "Attribute 2 definition"
    attribute_2.add_child(att_def_2)
    ms_2 = Node(names.MEASUREMENTSCALE, parent=attribute_2)
    attribute_2.add_child(ms_2)
    ordinal = Node(names.ORDINAL, parent=ms_2)
    ms_2.add_child(ordinal)
    non_numeric_domain_2 = Node(names.NONNUMERICDOMAIN, parent=ordinal)
    ordinal.add_child(non_numeric_domain_2)
    text_domain = Node(names.TEXTDOMAIN, parent=non_numeric_domain_2)
    non_numeric_domain_2.add_child(text_domain)
    definition_2 = Node(names.DEFINITION, parent=text_domain)
    text_domain.add_child(definition_2)
    definition_2.content = "US telephone numbers in the format (999) 888-7777"
    pattern = Node(names.PATTERN, parent=text_domain)
    text_domain.add_child(pattern)
    pattern.content = "[0-9a-zA-Z] matches simple alphanumeric strings"
    source_2 = Node(names.SOURCE, parent=text_domain)
    text_domain.add_child(source_2)
    source_2.content = "ISO country codes"

    attribute_3 = Node(names.ATTRIBUTE, parent=attribute_list)
    attribute_list.add_child(attribute_3)
    attribute_name_3 = Node(names.ATTRIBUTENAME, parent=attribute_3)
    attribute_3.add_child(attribute_name_3)
    attribute_name_3.content = "att-3"
    att_label_3 = Node(names.ATTRIBUTELABEL, parent=attribute_3)
    attribute_3.add_child(att_label_3)
    att_label_3.content = "Attribute Label 3"
    att_def_3 = Node(names.ATTRIBUTEDEFINITION)
    att_def_3.content = "Attribute 3 definition"
    attribute_3.add_child(att_def_3)
    storage_type = Node(names.STORAGETYPE, parent=attribute_3)
    attribute_3.add_child(storage_type)
    storage_type.add_attribute(
        "typeSystem", "http://www.w3.org/2001/XMLSchema-datatypes"
    )
    storage_type.content = "integer"
    ms_3 = Node(names.MEASUREMENTSCALE, parent=attribute_3)
    attribute_3.add_child(ms_3)
    interval = Node(names.INTERVAL, parent=ms_3)
    ms_3.add_child(interval)
    unit = Node(names.UNIT, parent=interval)
    interval.add_child(unit)
    standard_unit = Node(names.STANDARDUNIT, parent=unit)
    unit.add_child(standard_unit)
    standard_unit.content = "meter"
    custom_unit = Node(names.CUSTOMUNIT, parent=unit)
    # unit.add_child(custom_unit)
    custom_unit.content = "metersPerOneThirdGram"
    precision = Node(names.PRECISION, parent=interval)
    interval.add_child(precision)
    precision.content = "0.1"
    numeric_domain = Node(names.NUMERICDOMAIN, parent=interval)
    interval.add_child(numeric_domain)
    number_type = Node(names.NUMBERTYPE, parent=numeric_domain)
    numeric_domain.add_child(number_type)
    number_type.content = "integer"
    bounds = Node(names.BOUNDS, parent=numeric_domain)
    numeric_domain.add_child(bounds)
    minimum = Node(names.MINIMUM, parent=bounds)
    bounds.add_child(minimum)
    minimum.add_attribute("exclusive", "false")
    minimum.content = "0"
    maximum = Node(names.MAXIMUM, parent=bounds)
    bounds.add_child(maximum)
    maximum.add_attribute("exclusive", "false")
    maximum.content = "10"

    attribute_4 = Node(names.ATTRIBUTE, parent=attribute_list)
    attribute_list.add_child(attribute_4)
    attribute_name_4 = Node(names.ATTRIBUTENAME, parent=attribute_4)
    attribute_4.add_child(attribute_name_4)
    attribute_name_4.content = "att-4"
    att_label_4 = Node(names.ATTRIBUTELABEL, parent=attribute_4)
    attribute_4.add_child(att_label_4)
    att_label_4.content = "Attribute Label 4"
    att_def_4 = Node(names.ATTRIBUTEDEFINITION)
    att_def_4.content = "Attribute 4 definition"
    attribute_4.add_child(att_def_4)
    ms_4 = Node(names.MEASUREMENTSCALE, parent=attribute_4)
    attribute_4.add_child(ms_4)
    ratio = Node(names.RATIO, parent=ms_4)
    ms_4.add_child(ratio)
    unit_ratio = Node(names.UNIT, parent=ratio)
    ratio.add_child(unit_ratio)
    standard_unit_ratio = Node(names.STANDARDUNIT, parent=unit_ratio)
    # unit_ratio.add_child(standard_unit_ratio)
    standard_unit_ratio.content = "grams"
    custom_unit_ratio = Node(names.CUSTOMUNIT, parent=unit_ratio)
    unit_ratio.add_child(custom_unit_ratio)
    custom_unit_ratio.content = "gramsPerOneThirdMeter"
    precision_ratio = Node(names.PRECISION, parent=ratio)
    ratio.add_child(precision_ratio)
    precision_ratio.content = "0.01"
    numeric_domain_ratio = Node(names.NUMERICDOMAIN, parent=ratio)
    ratio.add_child(numeric_domain_ratio)
    number_type_ratio = Node(names.NUMBERTYPE, parent=numeric_domain_ratio)
    numeric_domain_ratio.add_child(number_type_ratio)
    number_type_ratio.content = "real"
    bounds_ratio = Node(names.BOUNDS, parent=numeric_domain_ratio)
    numeric_domain_ratio.add_child(bounds_ratio)
    minimum_ratio = Node(names.MINIMUM, parent=bounds_ratio)
    bounds_ratio.add_child(minimum_ratio)
    minimum_ratio.add_attribute("exclusive", "false")
    minimum_ratio.content = "0.0"
    maximum_ratio = Node(names.MAXIMUM, parent=bounds_ratio)
    bounds_ratio.add_child(maximum_ratio)
    maximum_ratio.add_attribute("exclusive", "false")
    maximum_ratio.content = "10.0"

    attribute_5 = Node(names.ATTRIBUTE, parent=attribute_list)
    attribute_list.add_child(attribute_5)
    attribute_name_5 = Node(names.ATTRIBUTENAME, parent=attribute_5)
    attribute_5.add_child(attribute_name_5)
    attribute_name_5.content = "att-5"
    att_label_5 = Node(names.ATTRIBUTELABEL, parent=attribute_5)
    attribute_5.add_child(att_label_5)
    att_label_5.content = "Attribute Label 5"
    att_def_5 = Node(names.ATTRIBUTEDEFINITION)
    att_def_5.content = "Attribute 5 definition"
    attribute_5.add_child(att_def_5)
    ms_5 = Node(names.MEASUREMENTSCALE, parent=attribute_5)
    attribute_5.add_child(ms_5)
    datetime = Node(names.DATETIME, parent=ms_5)
    ms_5.add_child(datetime)
    format_string = Node(names.FORMATSTRING, parent=datetime)
    datetime.add_child(format_string)
    format_string.content = "YYYY-MM-DD"
    datetime_precision = Node(names.DATETIMEPRECISION, parent=datetime)
    datetime.add_child(datetime_precision)
    datetime_precision.content = "1"
    datetime_domain = Node(names.DATETIMEDOMAIN, parent=datetime)
    datetime.add_child(datetime_domain)
    datetime_domain.add_attribute("id", "dtd-1")
    bounds_datetime = Node(names.BOUNDS, parent=datetime_domain)
    datetime_domain.add_child(bounds_datetime)
    minimum_datetime = Node(names.MINIMUM, parent=bounds_datetime)
    bounds_datetime.add_child(minimum_datetime)
    minimum_datetime.add_attribute("exclusive", "false")
    minimum_datetime.content = "2003-10-15"
    maximum_datetime = Node(names.MAXIMUM, parent=bounds_datetime)
    bounds_datetime.add_child(maximum_datetime)
    maximum_datetime.add_attribute("exclusive", "false")
    maximum_datetime.content = "2019-06-30"

    missing_value_code = Node(names.MISSINGVALUECODE, parent=attribute_1)
    attribute_1.add_child(missing_value_code)
    code_mvc = Node(names.CODE, parent=missing_value_code)
    missing_value_code.add_child(code_mvc)
    code_mvc.content = "SDT"
    code_explanation = Node(names.CODEEXPLANATION, parent=missing_value_code)
    missing_value_code.add_child(code_explanation)
    code_explanation.content = "Sensor Downtime"
    accuracy = Node(names.ACCURACY, parent=attribute_1)
    attribute_1.add_child(accuracy)
    attribute_accuracy_report = Node(
        names.ATTRIBUTEACCURACYREPORT, parent=accuracy
    )
    accuracy.add_child(attribute_accuracy_report)
    attribute_accuracy_report.content = "An explanation of the accuracy of the observation recorded in this attribute"
    qaaa = Node(names.QUANTITATIVEATTRIBUTEACCURACYASSESSMENT, parent=accuracy)
    accuracy.add_child(qaaa)
    attribute_accuracy_value = Node(names.ATTRIBUTEACCURACYVALUE, parent=qaaa)
    qaaa.add_child(attribute_accuracy_value)
    attribute_accuracy_value.content = (
        "An estimate of the accuracy of the identification"
    )
    attribute_accuracy_explanation = Node(
        names.ATTRIBUTEACCURACYEXPLANATION, parent=qaaa
    )
    qaaa.add_child(attribute_accuracy_explanation)
    attribute_accuracy_explanation.content = 'The identification of the test that yielded the "Attribute Accuracy Value"'

    case_sensitive = Node(names.CASESENSITIVE, parent=datatable)
    datatable.add_child(case_sensitive)
    case_sensitive.content = "yes"

    number_of_records = Node(names.NUMBEROFRECORDS, parent=datatable)
    datatable.add_child(number_of_records)
    number_of_records.content = "454"

    other_entity = Node(names.OTHERENTITY, parent=dataset)
    dataset.add_child(other_entity)

    alternate_identifier = Node(names.ALTERNATEIDENTIFIER, parent=other_entity)
    other_entity.add_child(alternate_identifier)
    alternate_identifier.add_attribute("system", "EDI")
    alternate_identifier.content = "https://portal.edirepository.org/nis/dataviewer?packageid=edi.23.1&entityid=ce5438fb9318b1f04d06b8a0276754d6"

    entity_name = Node(names.ENTITYNAME, parent=other_entity)
    other_entity.add_child(entity_name)
    entity_name.content = "Some Other Entity Data"

    entity_description = Node(names.ENTITYDESCRIPTION, parent=other_entity)
    other_entity.add_child(entity_description)
    entity_description.content = "Radiocarbon content of soil-respired air"

    physical = Node(names.PHYSICAL, parent=other_entity)
    other_entity.add_child(physical)
    physical.add_attribute("system", "EDI")

    object_name = Node(names.OBJECTNAME, parent=physical)
    physical.add_child(object_name)
    object_name.content = "tvan_14co2.jk.data.csv"

    size = Node(names.SIZE, parent=physical)
    physical.add_child(size)
    size.add_attribute("unit", "MB")
    size.content = "20"

    authentication = Node(names.AUTHENTICATION, parent=physical)
    physical.add_child(authentication)
    authentication.add_attribute("method", "password")
    authentication.content = "LDAP"

    compression_method = Node(names.COMPRESSIONMETHOD, parent=physical)
    physical.add_child(compression_method)
    compression_method.content = "zip"

    encoding_method = Node(names.ENCODINGMETHOD, parent=physical)
    physical.add_child(encoding_method)
    encoding_method.content = "base64"

    character_encoding = Node(names.CHARACTERENCODING, parent=physical)
    physical.add_child(character_encoding)
    character_encoding.content = "UTF-8"

    data_format = Node(names.DATAFORMAT, parent=physical)
    physical.add_child(data_format)

    text_format = Node(names.TEXTFORMAT, parent=data_format)
    data_format.add_child(text_format)

    num_header_lines = Node(names.NUMHEADERLINES, parent=text_format)
    text_format.add_child(num_header_lines)
    num_header_lines.content = "3"

    num_footer_lines = Node(names.NUMFOOTERLINES, parent=text_format)
    text_format.add_child(num_footer_lines)
    num_footer_lines.content = "0"

    record_delimiter = Node(names.RECORDDELIMITER, parent=text_format)
    text_format.add_child(record_delimiter)
    record_delimiter.content = "\\r\\n"

    physical_line_delimiter = Node(
        names.PHYSICALLINEDELIMITER, parent=text_format
    )
    text_format.add_child(physical_line_delimiter)
    physical_line_delimiter.content = "\\r\\n"

    num_physical_lines_per_record = Node(
        names.NUMPHYSICALLINESPERRECORD, parent=text_format
    )
    text_format.add_child(num_physical_lines_per_record)
    num_physical_lines_per_record.content = "1"

    max_record_length = Node(names.MAXRECORDLENGTH, parent=text_format)
    text_format.add_child(max_record_length)
    max_record_length.content = "597"

    attribute_orientation = Node(
        names.ATTRIBUTEORIENTATION, parent=text_format
    )
    text_format.add_child(attribute_orientation)
    attribute_orientation.content = "column"

    simple_delimited = Node(names.SIMPLEDELIMITED, parent=text_format)
    # text_format.add_child(simple_delimited)

    field_delimiter = Node(names.FIELDDELIMITER, parent=simple_delimited)
    simple_delimited.add_child(field_delimiter)
    field_delimiter.content = "\\t"

    collapse_delimiters = Node(
        names.COLLAPSEDELIMITERS, parent=simple_delimited
    )
    simple_delimited.add_child(collapse_delimiters)
    collapse_delimiters.content = "no"

    quote_character = Node(names.QUOTECHARACTER, parent=simple_delimited)
    simple_delimited.add_child(quote_character)
    quote_character.content = "'"

    literal_character = Node(names.LITERALCHARACTER, parent=simple_delimited)
    simple_delimited.add_child(literal_character)
    literal_character.content = (
        "/"  # Usually a backslash, but that causes an error
    )

    complex = Node(names.COMPLEX, parent=text_format)
    text_format.add_child(complex)

    text_fixed = Node(names.TEXTFIXED, parent=complex)
    complex.add_child(text_fixed)

    field_width = Node(names.FIELDWIDTH, parent=text_fixed)
    text_fixed.add_child(field_width)
    field_width.content = "12"

    line_number = Node(names.LINENUMBER, parent=text_fixed)
    text_fixed.add_child(line_number)
    line_number.content = "3"

    field_start_column = Node(names.FIELDSTARTCOLUMN, parent=text_fixed)
    text_fixed.add_child(field_start_column)
    field_start_column.content = "58"

    text_delimited = Node(names.TEXTDELIMITED, parent=complex)
    complex.add_child(text_delimited)

    field_delimiter_2 = Node(names.FIELDDELIMITER, parent=text_delimited)
    text_delimited.add_child(field_delimiter_2)
    field_delimiter_2.content = ","

    collapse_delimiters_2 = Node(
        names.COLLAPSEDELIMITERS, parent=text_delimited
    )
    text_delimited.add_child(collapse_delimiters_2)
    collapse_delimiters_2.content = "no"

    line_number_2 = Node(names.LINENUMBER, parent=text_delimited)
    text_delimited.add_child(line_number_2)
    line_number_2.content = "2"

    quote_character_2 = Node(names.QUOTECHARACTER, parent=text_delimited)
    text_delimited.add_child(quote_character_2)
    quote_character_2.content = "'"

    literal_character_2 = Node(names.LITERALCHARACTER, parent=text_delimited)
    text_delimited.add_child(literal_character_2)
    literal_character_2.content = (
        "/"  # Usually a backslash, but that causes an error
    )

    externally_defined_format = Node(
        names.EXTERNALLYDEFINEDFORMAT, parent=data_format
    )
    # data_format.add_child(externally_defined_format)

    format_name = Node(names.FORMATNAME, parent=externally_defined_format)
    externally_defined_format.add_child(format_name)
    format_name.content = "Microsoft Excel"

    format_version = Node(
        names.FORMATVERSION, parent=externally_defined_format
    )
    externally_defined_format.add_child(format_version)
    format_version.content = "2000 (9.0.2720)"

    binary_raster_format = Node(names.BINARYRASTERFORMAT, parent=data_format)
    # data_format.add_child(binary_raster_format)

    row_column_orientation = Node(
        names.ROWCOLUMNORIENTATION, parent=binary_raster_format
    )
    binary_raster_format.add_child(row_column_orientation)
    row_column_orientation.content = "column"

    multi_band = Node(names.MULTIBAND, parent=binary_raster_format)
    binary_raster_format.add_child(multi_band)

    nbands = Node(names.NBANDS, parent=multi_band)
    multi_band.add_child(nbands)
    nbands.content = "2"

    layout = Node(names.LAYOUT, parent=multi_band)
    multi_band.add_child(layout)
    layout.content = "bil"

    nbits = Node(names.NBITS, parent=binary_raster_format)
    binary_raster_format.add_child(nbits)
    nbits.content = "16"

    byteorder = Node(names.BYTEORDER, parent=binary_raster_format)
    binary_raster_format.add_child(byteorder)
    byteorder.content = "little-endian"

    skipbytes = Node(names.SKIPBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(skipbytes)
    skipbytes.content = "0"

    bandrowbytes = Node(names.BANDROWBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(bandrowbytes)
    bandrowbytes.content = "3"

    totalrowbytes = Node(names.TOTALROWBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(totalrowbytes)
    totalrowbytes.content = "8"

    bandgapbytes = Node(names.BANDGAPBYTES, parent=binary_raster_format)
    binary_raster_format.add_child(bandgapbytes)
    bandgapbytes.content = "1"

    distribution = Node(names.DISTRIBUTION, parent=physical)
    physical.add_child(distribution)

    online = Node(names.ONLINE, parent=distribution)
    # distribution.add_child(online)

    online_description = Node(names.ONLINEDESCRIPTION, parent=online)
    online.add_child(online_description)
    online_description.content = "network server"

    url = Node(names.URL, parent=online)
    online.add_child(url)
    url.add_attribute("function", "download")
    url.content = "https://data.abc.edu/somedataset/other_entity_data"

    # connection = Node(names.CONNECTION, parent=online)
    # online.add_child(connection)
    # connection.content = (
    #     "This is not a real connection element because it is only a string."
    # )

    offline = Node(names.OFFLINE, parent=distribution)
    distribution.add_child(offline)

    medium_name = Node(names.MEDIUMNAME, parent=offline)
    offline.add_child(medium_name)
    medium_name.content = "hardcopy"

    medium_density = Node(names.MEDIUMDENSITY, parent=offline)
    offline.add_child(medium_density)
    medium_density.content = "High Density (HD)"

    medium_density_units = Node(names.MEDIUMDENSITYUNITS, parent=offline)
    offline.add_child(medium_density_units)
    medium_density_units.content = "B/cm"

    medium_volume = Node(names.MEDIUMVOLUME, parent=offline)
    offline.add_child(medium_volume)
    medium_volume.content = "650 MB"

    medium_format = Node(names.MEDIUMFORMAT, parent=offline)
    offline.add_child(medium_format)
    medium_format.content = "NTFS"

    medium_note = Node(names.MEDIUMNOTE, parent=offline)
    offline.add_child(medium_note)
    medium_note.content = (
        "Some additional pertinent information about the media"
    )

    inline = Node(names.INLINE, parent=distribution)
    # distribution.add_child(inline)
    inline.content = "1,2,3,4,5,6,7,8,9"

    other_entity_access = Node(names.ACCESS, parent=distribution)
    other_entity_access.add_attribute("authSystem", "pasta")
    other_entity_access.add_attribute("order", "allowFirst")
    distribution.add_child(other_entity_access)

    other_entity_allow = Node(names.ALLOW, parent=other_entity_access)
    other_entity_access.add_child(other_entity_allow)

    other_entity_principal = Node(names.PRINCIPAL, parent=other_entity_allow)
    other_entity_principal.content = (
        "uid=ucarroll,o=EDI,dc=edirepository,dc=org"
    )
    other_entity_allow.add_child(other_entity_principal)

    other_entity_permission = Node(names.PERMISSION, parent=other_entity_allow)
    other_entity_permission.content = "write"
    other_entity_allow.add_child(other_entity_permission)

    entity_type = Node(names.ENTITYTYPE, parent=other_entity)
    other_entity.add_child(entity_type)
    entity_type.content = "Unknown Entity Type"

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
    # print(access_rule.attributes)
    # print(access_rule.children)
    # print(access_rule.content_rules)

    try:
        validate.node(access)
    except MetapypeRuleError as e:
        logger.error(e)

    try:
        errors = []
        validate.tree(eml, errors)
    except MetapypeRuleError as e:
        logger.error(e)

    for error in errors:
        print(error)

    # print(evaluate.node(title))
    #
    # mp_io.graph(eml, 0)
    #
    # attr = access_rule.attributes
    # print(attr)
    # children = access_rule.children
    # print(children)
    #
    # print(access.list_attributes())

    json_str = metapype_io.to_json(eml)
    # print(json_str)
    with open("test_eml.json", "w") as f:
        f.write(json_str)

    node = metapype_io.from_json(json_str)

    try:
        validate.tree(node)
    except MetapypeRuleError as e:
        logger.error(e)
    #
    xml = export.to_xml(eml)
    metapype_io.from_xml(xml)
    # print(xml)
    with open("test_eml.xml", "w") as f:
        f.write(xml)

    # warnings = []
    # evaluate.tree(eml, warnings)
    # for w in warnings:
    #     print(f"{w}")
    #
    # other_entity_rule = rule.get_rule(names.OTHERENTITY)
    # try:
    #     other_entity_rule.validate_rule(other_entity)
    # except MetapypeRuleError as e:
    #     logger.error(e)

    return 0


if __name__ == "__main__":
    main()

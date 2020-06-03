#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: rule

:Synopsis:
    EML node rules processing

:Author:
    servilla
    costa
    ide

:Created:
    7/10/18
"""
import os

import daiquiri
import datetime
import json

from metapype.config import Config
from metapype.eml.exceptions import MetapypeRuleError
from metapype.eml import names
from metapype.model.node import Node


logger = daiquiri.getLogger("validate: " + __name__)


REQUIRED = True
OPTIONAL = False
INFINITY = None

TYPE_NONE = None
TYPE_STR = "str"
TYPE_INT = "int"
TYPE_FLOAT = "float"
TYPE_DATETIME = "datetime"
TYPE_YEARDATE = "yearDate"


def load_rules():
    """
    Load rules from the JSON file into the rules dict
    """
    if "EML_RULES" in os.environ:
        json_path = os.environ["EML_RULES"]
    else:
        json_path = Config.EML_RULES

    with open(json_path) as fh:
        rules_dict = json.load(fh)

    return rules_dict


rules_dict = load_rules()


class Rule(object):
    """
    The Rule class holds rule content for a specific rule as well as the logic for
    processing content validation.
    """

    @staticmethod
    def child_list_node_names(child_list: list):
        if list is None or len(child_list) < 3:
            raise Exception("Child list must contain at least 3 elements")
        node_names = child_list[:-2]
        return node_names

    @staticmethod
    def child_list_min_occurrences(child_list: list):
        if list is None or len(child_list) < 3:
            raise Exception("Child list must contain at least 3 elements")
        min_occurrences = child_list[-2]
        return min_occurrences

    @staticmethod
    def child_list_max_occurrences(child_list: list):
        if list is None or len(child_list) < 3:
            raise Exception("Child list must contain at least 3 elements")
        max_occurrences = child_list[-1]
        return max_occurrences

    @staticmethod
    def is_float(val: str = None):
        """
        Boolean to determine whether node content is
        (or can be converted to) a valid float value.
        """
        is_valid = False
        if val:
            try:
                __ = float(val)
                is_valid = True
            except ValueError:
                pass
        return is_valid

    @staticmethod
    def is_int(val: str = None):
        """
        Boolean to determine whether node content is
        (or can be converted to) a valid int value.
        """
        is_valid = False
        if val:
            try:
                __ = int(val)
                is_valid = True
            except ValueError:
                pass
        return is_valid

    @staticmethod
    def is_yeardate(val: str = None):
        """
        Boolean to determine whether node content is a valid yearDate value.
        """
        is_valid = False
        if val and type(val) is str:
            for yeardate_format in ["%Y", "%Y-%m-%d"]:
                try:
                    datetime.datetime.strptime(val, yeardate_format)
                    is_valid = True
                    break
                except ValueError:
                    pass
        return is_valid

    @staticmethod
    def is_time(val: str = None):
        """
        Boolean to determine whether node content is a valid time value.
        """
        is_valid = False
        if val and type(val) is str:
            for time_format in ["%H:%M:%S", "%H:%M:%S.%f"]:
                try:
                    datetime.datetime.strptime(val, time_format)
                    is_valid = True
                    break
                except ValueError:
                    pass
        return is_valid

    def __init__(self, rule_name=None):
        self._name = rule_name

        # Initialize rule content for this instance from the rules dict
        rule_data = rules_dict[rule_name]
        self._attributes = rule_data[0]
        self._children = rule_data[1]
        self._content = rule_data[2]

    def child_insert_index(self, parent: Node, new_child: Node):
        new_child_name = new_child.name
        new_child_position = self._get_child_position(new_child_name)
        for index in range(len(parent.children) - 1, -1, -1):
            child_name = parent.children[index].name
            child_position = self._get_child_position(child_name)
            if new_child_position >= child_position:
                return index + 1
        return 0

    def is_required_attribute(self, attribute: str):
        if attribute in self._attributes:
            return self._attributes[attribute][0]
        else:
            raise Exception(f"Unknown attribute {attribute}")

    def is_allowed_child(self, child_name: str):
        allowed = False
        for child_list in self._children:
            if child_name in child_list[:-2]:
                allowed = True
        return allowed

    def allowed_attribute_values(self, attribute: str):
        values = []
        if attribute in self._attributes:
            if len(self._attributes[attribute]) > 1:
                values = self._attributes[attribute][1:]
        else:
            raise Exception(f"Unknown attribute {attribute}")
        return values

    def has_enum_content(self):
        return "content_enum" in self._content

    def validate_rule(self, node: Node):
        """
        Validates a node for rule compliance by validating the node's
        content, attributes, and children.

        Args:
            node: Node instance to be validates

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        """
        self._validate_content(node)
        self._validate_attributes(node)
        self._validate_children(node)

    def _get_child_position(self, node_name: str):
        for position in range(0, len(self.children)):
            if node_name in self.children[position][:-2]:
                return position
        msg = f'Child "{node_name}" not allowed'
        raise MetapypeRuleError(msg)

    def _validate_content(self, node: Node):
        """
        Validates node content for rule compliance.
        For each of the content rules configured for this rule,
        validates the node to see if its content complies 
        with the content that this rule expects.

        Args:
            node: Node instance to be validated

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        """
        for content_rule in self._content["content_rules"]:
            if content_rule == "emptyContent":
                self._validate_empty_content(node)
            elif content_rule == "floatContent":
                self._validate_float_content(node)
            elif content_rule == "floatRangeContent_EW":
                self._validate_float_range_ew_content(node)
            elif content_rule == "floatRangeContent_NS":
                self._validate_float_range_ns_content(node)
            elif content_rule == "intContent":
                # TODO: need validate_int_content fucntion
                # self._validate_int_content(node)
                pass
            elif content_rule == "nonEmptyContent":
                self._validate_non_empty_content(node)
            elif content_rule == "strContent":
                self._validate_str_content(node)
            elif content_rule == "timeContent":
                self._validate_time_content(node)
            elif content_rule == "yearDateContent":
                self._validate_yeardate_content(node)

        if self.has_enum_content():
            enum_values = self._content["content_enum"]
            self._validate_enum_content(node, enum_values)

    @staticmethod
    def _validate_empty_content(node: Node):
        if node.content is not None:
            msg = f'Node "{node.name}" content should be empty'
            raise MetapypeRuleError(msg)

    @staticmethod
    def _validate_enum_content(node: Node, enum_values: list):
        if node.content not in enum_values:
            msg = f'Node "{node.name}" content should be one of "{enum_values}", not "{node.content}"'
            raise MetapypeRuleError(msg)

    @staticmethod
    def _validate_float_content(node: Node):
        val = node.content
        if val is not None and not Rule.is_float(val):
            msg = f'Node "{node.name}" content should be type "{TYPE_FLOAT}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)

    def _validate_float_range_content(self, node: Node, minmax):
        self._validate_float_content(node)
        float_val = float(node.content)
        if float_val < minmax[0] or float_val > minmax[1]:
            msg = f'Node "{node.name}" content should be in range {minmax}'
            raise MetapypeRuleError(msg)

    def _validate_float_range_ew_content(self, node: Node):
        self._validate_float_range_content(node, (-180.0, 180.0))

    def _validate_float_range_ns_content(self, node: Node):
        self._validate_float_range_content(node, (-90.0, 90.0))

    @staticmethod
    def _validate_non_empty_content(node: Node):
        if len(node.children) == 0 and node.content is None:
            msg = f'Node "{node.name}" content should not be empty'
            raise MetapypeRuleError(msg)

    @staticmethod
    def _validate_str_content(node: Node):
        if node.content is not None and type(node.content) is not str:
            msg = f'Node "{node.name}" content should be type "{TYPE_STR}", not "{type(node.content)}"'
            raise MetapypeRuleError(msg)

    @staticmethod
    def _validate_time_content(node: Node):
        val = node.content
        if val is not None and not Rule.is_time(val):
            msg = f'Node "{node.name}" format should be time ("HH:MM:SS" or "HH:MM:SS.f")'
            raise MetapypeRuleError(msg)

    @staticmethod
    def _validate_yeardate_content(node: Node):
        val = node.content
        if val is not None and not Rule.is_yeardate(val):
            msg = f'Node "{node.name}" format should be year ("YYYY") or date ("YYYY-MM-DD")'
            raise MetapypeRuleError(msg)

    def _validate_attributes(self, node: Node) -> None:
        """
        Validates node attributes for rule compliance.

        Iterates through the dict of attribute rules and validates whether
        the node instance complies with the rule.

        Args:
            node: Node instance to be validates

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal attribute or missing required attribute
        """
        for attribute in self._attributes:
            required = self._attributes[attribute][0]
            # Test for required attributes
            if required and attribute not in node.attributes:
                msg = f'"{attribute}" is a required attribute of node "{node.name}"'
                raise MetapypeRuleError(msg)
        for attribute in node.attributes:
            # Test for non-allowed attribute
            if attribute not in self._attributes:
                msg = f'"{attribute}" is not a recognized attributes of node "{node.name}"'
                raise MetapypeRuleError(msg)
            else:
                # Test for enumerated list of allowed values
                if (
                    len(self._attributes[attribute]) > 1
                    and node.attributes[attribute]
                    not in self._attributes[attribute][1:]
                ):
                    msg = f'Node "{node.name}" attribute "{attribute}" must be one of the following: "{self._attributes[attribute][1:]}"'
                    raise MetapypeRuleError(msg)

    def _validate_children(self, node: Node) -> None:
        """
        Validates node children for rule compliance.

        Iterates through the list children rules and validates whether
        the node instance complies with the rules.

        Args:
            node: Node instance to be validated

        Returns:
            None

        Raises:
            MetapypeRuleError: Illegal child, bad sequence or choice, missing
            child, or wrong child cardinality
        """
        i = 0
        max_i = len(node.children)
        for child in self._children:
            name = child[:-2]
            min = child[-2]
            max = child[-1]
            cnt = 0
            while i < max_i:
                child_name = node.children[i].name
                if child_name in name:
                    cnt += 1
                    if max is not INFINITY and cnt > max:
                        msg = f'Maximum occurrence of "{name}" exceeded for "{node.name}"'
                        raise MetapypeRuleError(msg)
                    i += 1
                else:
                    break
            if cnt < min:
                msg = (
                    f'Minimum occurrence of "{name}" not met for "{node.name}"'
                )
                raise MetapypeRuleError(msg)
        if i < max_i:
            child_name = node.children[i].name
            msg = f'Child "{child_name}" not allowed  for "{node.name}"'
            raise MetapypeRuleError(msg)

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes

    @property
    def children(self):
        return self._children

    @property
    def content_rules(self):
        return self._content["content_rules"]

    @property
    def content_enum(self):
        if self.has_enum_content():
            return self._content["content_enum"]
        else:
            return []


# Named constants for EML metadata rules
RULE_ACCESS = "accessRule"
RULE_ACCURACY = "accuracyRule"
RULE_ADDITIONALMETADATA = "additionalMetadataRule"
RULE_ADDRESS = "addressRule"
RULE_ALLOW = "allowRule"
RULE_ALTERNATEIDENTIFIER = "alternateIdentifierRule"
RULE_ANNOTATION = "annotationRule"
RULE_ANYINT = "anyIntRule"
RULE_ANYNAME = "anyNameRule"
RULE_ANYSTRING = "anyStringRule"
RULE_ANYURI = "anyURIRule"
RULE_ATTRIBUTE = "attributeRule"
RULE_ATTRIBUTELIST = "attributeListRule"
RULE_AUTHENTICATION = "authenticationRule"
RULE_AWARD = "awardRule"
RULE_BINARYRASTER_FORMAT = "binaryRasterFormatRule"
RULE_BOUNDINGCOORDINATE_EW = "boundingCoordinateRule_EW"
RULE_BOUNDINGCOORDINATE_NS = "boundingCoordinateRule_NS"
RULE_BOUNDINGCOORDINATES = "boundingCoordinatesRule"
RULE_BOUNDS = "boundsRule"
RULE_CODEDEFINITION = "codeDefinitionRule"
RULE_COMPLEX = "complexRule"
RULE_COVERAGE = "coverageRule"
RULE_DATAFORMAT = "dataFormatRule"
RULE_DATASET = "datasetRule"
RULE_DATATABLE = "dataTableRule"
RULE_DATETIME = "dateTimeRule"
RULE_DATETIMEDOMAIN = "dateTimeDomainRule"
RULE_DENY = "denyRule"
RULE_DESCRIPTOR = "descriptorRule"
RULE_DISTRIBUTION = "distributionRule"
RULE_EML = "emlRule"
RULE_ENTITYCODELIST = "entityCodeListRule"
RULE_ENUMERATEDDOMAIN = "enumeratedDomainRule"
RULE_EXTERNALCODESET = "externalCodeSetRule"
RULE_EXTERNALLYDEFINIEDFORMAT = "externallyDefinedFormatRule"
RULE_FUNDING = "fundingRule"
RULE_GEOGRAPHICCOVERAGE = "geographicCoverageRule"
RULE_INDIVIDUALNAME = "individualNameRule"
RULE_INTERVALRATIO = "intervalRatioRule"
RULE_KEYWORD = "keywordRule"
RULE_KEYWORDSET = "keywordSetRule"
RULE_KEYWORDTHESAURUS = "keywordThesaurusRule"
RULE_LICENSED = "licensedRule"
RULE_MAINTENANCE = "maintenanceRule"
RULE_MEASUREMENTSCALE = "measurementScaleRule"
RULE_METADATA = "metadataRule"
RULE_METHODS = "methodsRule"
RULE_METHODSTEP = "methodStepRule"
RULE_MINMAX = "minMaxRule"
RULE_MISSINGVALUECODE = "missingValueCodeRule"
RULE_MULTIBAND = "multiBandRule"
RULE_NOMINAL = "nominalOrdinalRule"
RULE_NONNUMERICDOMAIN = "nonNumericDomainRule"
RULE_NUMERICDOMAIN = "numericDomainRule"
RULE_OFFLINE = "offlineRule"
RULE_ONLINE = "onlineRule"
RULE_ORDINAL = "nominalOrdinalRule"
RULE_OTHERENTITY = "otherEntityRule"
RULE_PERMISSION = "permissionRule"
RULE_PHONE = "phoneRule"
RULE_PHYSICAL = "physicalRule"
RULE_PRINCIPAL = "principalRule"
RULE_PROJECT = "projectRule"
RULE_QUALITYCONTROL = "qualityControlRule"
RULE_QUANTITATIVEATTRIBUTEACCURACYASSESSMENT = (
    "quantitativeAttributeAccuracyAssessmentRule"
)
RULE_RANGEOFDATES = "rangeOfDatesRule"
RULE_RATIO = "ratioRule"
RULE_RESPONSIBLEPARTY = "responsiblePartyRule"
RULE_RESPONSIBLEPARTY_WITH_ROLE = "responsiblePartyWithRoleRule"
RULE_ROWCOLUMN = "rowColumnRule"
RULE_SAMPLING = "samplingRule"
RULE_SINGLEDATETIME = "singleDateTimeRule"
RULE_SIMPLEDELIMITED = "simpleDelimitedRule"
RULE_SIZE = "sizeRule"
RULE_STORAGETYPE = "storageTypeRule"
RULE_STUDYAREADESCRIPTION = "studyAreaDescriptionRule"
RULE_STUDYEXTENT = "studyExtentRule"
RULE_TAXONOMICCLASSIFICATION = "taxonomicClassificationRule"
RULE_TAXONOMICCOVERAGE = "taxonomicCoverageRule"
RULE_TEMPORALCOVERAGE = "temporalCoverageRule"
RULE_TEXT = "textRule"
RULE_TEXTDELIMITED = "textDelimitedRule"
RULE_TEXTDOMAIN = "textDomainRule"
RULE_TEXTFIXED = "textFixedRule"
RULE_TEXTFORMAT = "textFormatRule"
RULE_TIME = "timeRule"
RULE_UNIT = "unitRule"
RULE_URL = "urlRule"
RULE_USERID = "userIdRule"
RULE_VALUE = "valueRule"
RULE_YEARDATE = "yearDateRule"


# Maps node names to their corresponding metadata rule names
node_mappings = {
    names.ABSTRACT: RULE_TEXT,
    names.ACCESS: RULE_ACCESS,
    names.ACCURACY: RULE_ACCURACY,
    names.ACKNOWLEDGEMENTS: RULE_TEXT,
    names.ADDITIONALINFO: RULE_TEXT,
    names.ADDITIONALMETADATA: RULE_ADDITIONALMETADATA,
    names.ADDRESS: RULE_ADDRESS,
    names.ADMINISTRATIVEAREA: RULE_ANYNAME,
    names.ALLOW: RULE_ALLOW,
    names.ALTERNATEIDENTIFIER: RULE_ALTERNATEIDENTIFIER,
    names.ANNOTATION: RULE_ANNOTATION,
    names.ASSOCIATEDPARTY: RULE_RESPONSIBLEPARTY_WITH_ROLE,
    names.ATTRIBUTE: RULE_ATTRIBUTE,
    names.ATTRIBUTEACCURACYEXPLANATION: RULE_ANYSTRING,
    names.ATTRIBUTEACCURACYREPORT: RULE_ANYSTRING,
    names.ATTRIBUTEACCURACYVALUE: RULE_ANYSTRING,
    names.ATTRIBUTEDEFINITION: RULE_ANYSTRING,
    names.ATTRIBUTELABEL: RULE_ANYSTRING,
    names.ATTRIBUTELIST: RULE_ATTRIBUTELIST,
    names.ATTRIBUTENAME: RULE_ANYSTRING,
    names.ATTRIBUTEORIENTATION: RULE_ANYSTRING,
    names.AUTHENTICATION: RULE_AUTHENTICATION,
    names.AWARD: RULE_AWARD,
    names.AWARDNUMBER: RULE_ANYNAME,
    names.AWARDURL: RULE_ANYNAME,
    names.BANDGAPBYTES: RULE_ANYSTRING,
    names.BANDROWBYTES: RULE_ANYSTRING,
    names.BEGINDATE: RULE_SINGLEDATETIME,
    names.BINARYRASTERFORMAT: RULE_BINARYRASTER_FORMAT,
    names.BOUNDINGCOORDINATES: RULE_BOUNDINGCOORDINATES,
    names.BOUNDS: RULE_BOUNDS,
    names.BYTEORDER: RULE_ANYSTRING,
    names.CALENDARDATE: RULE_YEARDATE,
    names.CASESENSITIVE: RULE_ANYSTRING,
    names.CHARACTERENCODING: RULE_ANYSTRING,
    names.CITATION: RULE_ANYSTRING,
    names.CITY: RULE_ANYNAME,
    names.CODE: RULE_ANYSTRING,
    names.CODEDEFINITION: RULE_CODEDEFINITION,
    names.CODEEXPLANATION: RULE_ANYSTRING,
    names.CODESETNAME: RULE_ANYSTRING,
    names.CODESETURL: RULE_ANYURI,
    names.COMMONNAME: RULE_ANYSTRING,
    names.COLLAPSEDELIMITERS: RULE_ANYSTRING,
    names.COMPLEX: RULE_COMPLEX,
    names.COMPRESSIONMETHOD: RULE_ANYSTRING,
    names.CONNECTION: RULE_ANYSTRING,
    names.CONTACT: RULE_RESPONSIBLEPARTY,
    names.COUNTRY: RULE_ANYNAME,
    names.COVERAGE: RULE_COVERAGE,
    names.CREATOR: RULE_RESPONSIBLEPARTY,
    names.CUSTOMUNIT: RULE_ANYSTRING,
    names.DATAFORMAT: RULE_DATAFORMAT,
    names.DATASET: RULE_DATASET,
    names.DATATABLE: RULE_DATATABLE,
    names.DATETIME: RULE_DATETIME,
    names.DATETIMEDOMAIN: RULE_DATETIMEDOMAIN,
    names.DATETIMEPRECISION: RULE_ANYSTRING,
    names.DEFINITION: RULE_ANYSTRING,
    names.DEFINITIONATTRIBUTEREFERENCE: RULE_ANYSTRING,
    names.DELIVERYPOINT: RULE_ANYNAME,
    names.DENY: RULE_DENY,
    names.DESCRIBES: RULE_ANYSTRING,
    names.DESCRIPTOR: RULE_DESCRIPTOR,
    names.DESCRIPTORVALUE: RULE_ANYSTRING,
    names.DESCRIPTION: RULE_TEXT,
    names.DISTRIBUTION: RULE_DISTRIBUTION,
    names.EASTBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_EW,
    names.ELECTRONICMAILADDRESS: RULE_ANYNAME,
    names.EML: RULE_EML,
    names.ENCODINGMETHOD: RULE_ANYSTRING,
    names.ENDDATE: RULE_SINGLEDATETIME,
    names.ENTITYCODELIST: RULE_ENTITYCODELIST,
    names.ENTITYDESCRIPTION: RULE_ANYSTRING,
    names.ENTITYNAME: RULE_ANYSTRING,
    names.ENTITYREFERENCE: RULE_ANYSTRING,
    names.ENTITYTYPE: RULE_ANYSTRING,
    names.ENUMERATEDDOMAIN: RULE_ENUMERATEDDOMAIN,
    names.EXTERNALCODESET: RULE_EXTERNALCODESET,
    names.EXTERNALLYDEFINEDFORMAT: RULE_EXTERNALLYDEFINIEDFORMAT,
    names.FIELDDELIMITER: RULE_ANYSTRING,
    names.FIELDSTARTCOLUMN: RULE_ANYSTRING,
    names.FIELDWIDTH: RULE_ANYSTRING,
    names.FORMATNAME: RULE_ANYSTRING,
    names.FORMATSTRING: RULE_ANYSTRING,
    names.FORMATVERSION: RULE_ANYSTRING,
    names.FUNDERIDENTIFIER: RULE_ANYNAME,
    names.FUNDERNAME: RULE_ANYNAME,
    names.FUNDING: RULE_TEXT,
    names.GENERALTAXONOMICCOVERAGE: RULE_ANYSTRING,
    names.GIVENNAME: RULE_ANYNAME,
    names.GEOGRAPHICCOVERAGE: RULE_GEOGRAPHICCOVERAGE,
    names.GEOGRAPHICDESCRIPTION: RULE_ANYSTRING,
    names.GETTINGSTARTED: RULE_TEXT,
    names.IDENTIFIER: RULE_ANYSTRING,
    names.INDIVIDUALNAME: RULE_INDIVIDUALNAME,
    names.INLINE: RULE_ANYSTRING,
    names.INSTRUMENTATION: RULE_ANYSTRING,
    names.INTELLECTUALRIGHTS: RULE_TEXT,
    names.INTERVAL: RULE_INTERVALRATIO,
    names.INTRODUCTION: RULE_TEXT,
    names.KEYWORD: RULE_KEYWORD,
    names.KEYWORDSET: RULE_KEYWORDSET,
    names.KEYWORDTHESAURUS: RULE_KEYWORDTHESAURUS,
    names.LANGUAGE: RULE_ANYNAME,
    names.LAYOUT: RULE_ANYSTRING,
    names.LICENSED: RULE_LICENSED,
    names.LICENSENAME: RULE_ANYSTRING,
    names.LINENUMBER: RULE_ANYINT,
    names.LITERALCHARACTER: RULE_ANYSTRING,
    names.MAINTENANCE: RULE_MAINTENANCE,
    names.MAINTENANCEUPDATEFREQUENCY: RULE_ANYSTRING,
    names.MARKDOWN: RULE_ANYSTRING,
    names.MAXIMUM: RULE_MINMAX,
    names.MAXRECORDLENGTH: RULE_ANYINT,
    names.MEASUREMENTSCALE: RULE_MEASUREMENTSCALE,
    names.MEDIUMNAME: RULE_ANYSTRING,
    names.MEDIUMDENSITY: RULE_ANYSTRING,
    names.MEDIUMDENSITYUNITS: RULE_ANYSTRING,
    names.MEDIUMVOLUME: RULE_ANYSTRING,
    names.MEDIUMFORMAT: RULE_ANYSTRING,
    names.MEDIUMNOTE: RULE_ANYSTRING,
    names.METADATA: RULE_METADATA,
    names.METADATAPROVIDER: RULE_RESPONSIBLEPARTY,
    names.METHODS: RULE_METHODS,
    names.METHODSTEP: RULE_METHODSTEP,
    names.MINIMUM: RULE_MINMAX,
    names.MISSINGVALUECODE: RULE_MISSINGVALUECODE,
    names.MULTIBAND: RULE_MULTIBAND,
    names.NBANDS: RULE_ANYINT,
    names.NBITS: RULE_ANYINT,
    names.NOMINAL: RULE_NOMINAL,
    names.NONNUMERICDOMAIN: RULE_NONNUMERICDOMAIN,
    names.NORTHBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_NS,
    names.NUMBEROFRECORDS: RULE_ANYSTRING,
    names.NUMBERTYPE: RULE_ANYSTRING,
    names.NUMERICDOMAIN: RULE_NUMERICDOMAIN,
    names.NUMFOOTERLINES: RULE_ANYINT,
    names.NUMHEADERLINES: RULE_ANYINT,
    names.NUMPHYSICALLINESPERRECORD: RULE_ANYINT,
    names.OBJECTNAME: RULE_ANYSTRING,
    names.OFFLINE: RULE_OFFLINE,
    names.ONLINE: RULE_ONLINE,
    names.ONLINEDESCRIPTION: RULE_ANYSTRING,
    names.ONLINEURL: RULE_ANYURI,
    names.ORDERATTRIBUTEREFERENCE: RULE_ANYSTRING,
    names.ORDINAL: RULE_ORDINAL,
    names.ORGANIZATIONNAME: RULE_ANYNAME,
    names.OTHERENTITY: RULE_OTHERENTITY,
    names.PARA: RULE_ANYSTRING,
    names.PATTERN: RULE_ANYSTRING,
    names.PERMISSION: RULE_PERMISSION,
    names.PERSONNEL: RULE_RESPONSIBLEPARTY_WITH_ROLE,
    names.PHONE: RULE_PHONE,
    names.PHYSICAL: RULE_PHYSICAL,
    names.PHYSICALLINEDELIMITER: RULE_ANYSTRING,
    names.POSITIONNAME: RULE_ANYNAME,
    names.POSTALCODE: RULE_ANYNAME,
    names.PRECISION: RULE_ANYSTRING,
    names.PRINCIPAL: RULE_PRINCIPAL,
    names.PROJECT: RULE_PROJECT,
    names.PROPERTYURI: RULE_ANYURI,
    names.PUBDATE: RULE_YEARDATE,
    names.PUBLISHER: RULE_RESPONSIBLEPARTY,
    names.PUBPLACE: RULE_ANYSTRING,
    names.PURPOSE: RULE_TEXT,
    names.QUALITYCONTROL: RULE_QUALITYCONTROL,
    names.QUANTITATIVEATTRIBUTEACCURACYASSESSMENT:
        RULE_QUANTITATIVEATTRIBUTEACCURACYASSESSMENT,
    names.QUOTECHARACTER: RULE_ANYSTRING,
    names.RANGEOFDATES: RULE_RANGEOFDATES,
    names.RATIO: RULE_INTERVALRATIO,
    names.RECORDDELIMITER: RULE_ANYSTRING,
    names.ROLE: RULE_ANYSTRING,
    names.ROWCOLUMNORIENTATION: RULE_ROWCOLUMN,
    names.SALUTATION: RULE_ANYNAME,
    names.SAMPLING: RULE_SAMPLING,
    names.SAMPLINGDESCRIPTION: RULE_TEXT,
    names.SECTION: RULE_ANYSTRING,
    names.SERIES: RULE_ANYSTRING,
    names.SHORTNAME: RULE_ANYSTRING,
    names.SIMPLEDELIMITED: RULE_SIMPLEDELIMITED,
    names.SINGLEDATETIME: RULE_SINGLEDATETIME,
    names.SIZE: RULE_SIZE,
    names.SKIPBYTES: RULE_ANYSTRING,
    names.SOURCE: RULE_ANYSTRING,
    names.SOUTHBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_NS,
    names.STANDARDUNIT: RULE_ANYSTRING,
    names.STORAGETYPE: RULE_STORAGETYPE,
    names.STUDYAREADESCRIPTION: RULE_STUDYAREADESCRIPTION,
    names.STUDYEXTENT: RULE_STUDYEXTENT,
    names.SURNAME: RULE_ANYNAME,
    names.TAXONOMICCLASSIFICATION: RULE_TAXONOMICCLASSIFICATION,
    names.TAXONOMICCOVERAGE: RULE_TAXONOMICCOVERAGE,
    names.TAXONRANKNAME: RULE_ANYSTRING,
    names.TAXONRANKVALUE: RULE_ANYSTRING,
    names.TEMPORALCOVERAGE: RULE_TEMPORALCOVERAGE,
    names.TEXTDELIMITED: RULE_TEXTDELIMITED,
    names.TEXTDOMAIN: RULE_TEXTDOMAIN,
    names.TEXTFIXED: RULE_TEXTFIXED,
    names.TEXTFORMAT: RULE_TEXTFORMAT,
    names.TIME: RULE_TIME,
    names.TITLE: RULE_ANYNAME,
    names.TOTALROWBYTES: RULE_ANYSTRING,
    names.UNIT: RULE_UNIT,
    names.URL: RULE_URL,
    names.USERID: RULE_USERID,
    names.VALUE: RULE_VALUE,
    names.VALUEATTRIBUTEREFERENCE: RULE_ANYSTRING,
    names.VALUEURI: RULE_ANYURI,
    names.WESTBOUNDINGCOORDINATE: RULE_BOUNDINGCOORDINATE_EW,
}


def node_names():
    """
    Helper function.
    Returns a list of all known node names.
    """
    return list(node_mappings.keys())


def get_rule_name(node_name: str):
    """
    Helper function.
    For a given node name, return its corresponding rule name
    """
    return node_mappings.get(node_name)


def get_rule(node_name: str):
    """
    Helper function.
    For a given node name, instantiate its corresponding rule object and return it
    """
    rule_name = get_rule_name(node_name)
    return Rule(rule_name)


def main():
    eml_rule = Rule("emlRule")
    print(eml_rule)


if __name__ == "__main__":
    main()

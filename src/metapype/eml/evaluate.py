#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: evaluate

:Synopsis:

:Author:
    servilla
    costa
    ide

:Created:
    6/21/18
"""
import daiquiri

from metapype.eml import names
from metapype.model.node import Node
from metapype.model.normalize import normalize
from metapype.eml.evaluation_warnings import EvaluationWarning


logger = daiquiri.getLogger("evaluate: " + __name__)


def get_text_content(text_node: Node) -> str:
    # Collect the text under a TextType node.
    # This is intended for use in checking if text is present and that it has enough words, if there is
    #  such a requirement. I.e., it doesn't worry about getting the text in the correct order if, for example, there
    #  are para and markdown nodes interleaved.
    content = text_node.content if text_node.content else ''
    paras = []
    text_node.find_all_descendants(names.PARA, paras)
    for para in paras:
        content += '\n' + para.content
    markdowns = []
    text_node.find_all_descendants(names.MARKDOWN, markdowns)
    for markdown in markdowns:
        content += '\n' + markdown.content
    return content


# ==================== Begin of rules section ====================

def _associated_responsible_party_rule(node: Node) -> list:
    return _responsible_party_rule(node)


def _contact_rule(node: Node) -> list:
    return _responsible_party_rule(node)


def _creator_rule(node: Node) -> list:
    return _responsible_party_rule(node)


def _dataset_rule(node: Node) -> list:
    evaluation = []
    abstract_node = None
    coverage_node = None
    datatable_node = None
    intellectual_rights_node = None
    keywordset_nodes = []
    methods_node = None
    project_node = None
    for child in node.children:
        if child.name == names.ABSTRACT:
            abstract_node = child
        elif child.name == names.COVERAGE:
            coverage_node = child
        elif child.name == names.DATATABLE:
            datatable_node = child
        elif child.name == names.INTELLECTUALRIGHTS:
            intellectual_rights_node = child
        elif child.name == names.KEYWORDSET:
            keywordset_nodes.append(child)
        elif child.name == names.METHODS:
            methods_node = child
        elif child.name == names.PROJECT:
            project_node = child

    if abstract_node:
        content = get_text_content(abstract_node)
        if content:
            words = content.split()
            if len(words) < 20:
                evaluation.append((
                    EvaluationWarning.DATASET_ABSTRACT_TOO_SHORT,
                    f'Consider increasing the length of the dataset''s abstract.',
                    node
                ))
        else:
            evaluation.append((
                EvaluationWarning.DATASET_ABSTRACT_MISSING,
                f'A dataset abstract should be provided.',
                node
            ))
    else:
        evaluation.append((
            EvaluationWarning.DATASET_ABSTRACT_MISSING,
            f'A dataset abstract should be provided.',
            node
        ))
    if not (coverage_node and coverage_node.children):
        evaluation.append((
            EvaluationWarning.DATASET_COVERAGE_MISSING,
            f'At least one coverage element should be present in a dataset. I.e., at least one of Geographic Coverage,'
            f' Temporal Coverage, or Taxonomic Coverage should be specified.',
            node
        ))
    if not datatable_node:
        evaluation.append((
            EvaluationWarning.DATATABLE_MISSING,
            f'A dataset should contain at least one Data Table.',
            node
        ))
    if not (intellectual_rights_node and intellectual_rights_node.content):
        evaluation.append((
            EvaluationWarning.INTELLECTUAL_RIGHTS_MISSING,
            f'An Intellectual Rights policy should be specified.',
            node
        ))
    if not keywordset_nodes:
        evaluation.append((
            EvaluationWarning.KEYWORDS_MISSING,
            f'Keywords should be provided to make the dataset more discoverable.',
            node
        ))
    else:
        num_keywords = 0
        for keywordset_node in keywordset_nodes:
            keyword_nodes = keywordset_node.find_all_children(names.KEYWORD)
            num_keywords += len(keyword_nodes)
        if num_keywords < 5:
            evaluation.append((
                EvaluationWarning.KEYWORDS_INSUFFICIENT,
                f'Consider adding more keywords to make the dataset more discoverable.',
                node
            ))
    if not methods_node:
        evaluation.append((
            EvaluationWarning.DATASET_METHOD_STEPS_MISSING,
            f'A dataset should contain at least one Method Step.',
            node
        ))
    if not project_node:
        evaluation.append((
            EvaluationWarning.DATASET_PROJECT_MISSING,
            f'A dataset should contain a Project.',
            node
        ))

    return evaluation


def _datatable_rule(node: Node) -> list:
    evaluation = []
    description = any(
        child.name == names.ENTITYDESCRIPTION and child.content
        for child in node.children
    )
    if not description:
        evaluation.append((
            EvaluationWarning.DATATABLE_DESCRIPTION_MISSING,
            f'A data table Description is highly recommended.',
            node
        ))

    physical_node = None
    authentication_node = None
    number_of_records_node = None
    size_node = None

    data_format_node = None
    text_format_node = None
    record_delimiter_node = None

    for child in node.children:
        if child.name == names.PHYSICAL:
            physical_node = child
            break
    if physical_node:
        for child in physical_node.children:
            if child.name == names.AUTHENTICATION:
                authentication_node = child
            elif child.name == names.RECORDDELIMITER:
                record_delimiter_node = child
            elif child.name == names.SIZE:
                size_node = child
            elif child.name == names.DATAFORMAT:
                data_format_node = child
    if data_format_node:
        for child in data_format_node.children:
            if child.name == names.TEXTFORMAT:
                text_format_node = child
                break
    if text_format_node:
        for child in text_format_node.children:
            if child.name == names.RECORDDELIMITER:
                record_delimiter_node = child
                break
    for child in node.children:
        if child.name == names.NUMBEROFRECORDS:
            number_of_records_node = child
            break

    if not size_node or not size_node.content:
        evaluation.append((
            EvaluationWarning.DATATABLE_SIZE_MISSING,
            f'A data table should contain a Size element.',
            node
        ))

    if not authentication_node or not authentication_node.content:
        evaluation.append((
            EvaluationWarning.DATATABLE_MD5_CHECKSUM_MISSING,
            f'A data table should contain an Authentication element.',
            node
        ))

    if not number_of_records_node or not number_of_records_node.content:
        evaluation.append((
            EvaluationWarning.DATATABLE_NUMBER_OF_RECORDS_MISSING,
            f'A data table should contain a Number of Records element.',
            node
        ))

    if not record_delimiter_node or not record_delimiter_node.content:
        evaluation.append((
            EvaluationWarning.DATATABLE_RECORD_DELIMITER_MISSING,
            f'A data table should contain a Record Delimiter element.',
            node
        ))

    return evaluation


def _description_rule(node: Node) -> list:
    # Various description nodes are required but since they have TextType, the rules allow them to be empty.
    # Require them to have nonempty content (including para and markdown children).
    evaluation = []
    warning = None
    content = get_text_content(node)
    if not content:
        parent = node.parent.name
        if parent == 'connectionDefinition':
            warning = EvaluationWarning.CONNECTION_DEFINITION_DESCRIPTION_MISSING
        elif parent == 'designDescription':
            warning = EvaluationWarning.DESIGN_DESCRIPTION_DESCRIPTION_MISSING
        elif parent == 'maintenance':
            warning = EvaluationWarning.MAINTENANCE_DESCRIPTION_MISSING
        elif parent == 'methodStep':
            warning = EvaluationWarning.METHOD_STEP_DESCRIPTION_MISSING
        elif parent == 'procedureStep':
            warning = EvaluationWarning.PROCEDURE_STEP_DESCRIPTION_MISSING
        elif parent == 'qualityControl':
            warning = EvaluationWarning.QUALITY_CONTROL_DESCRIPTION_MISSING
        elif parent == 'samplingDescription':
            warning = EvaluationWarning.SAMPLING_DESCRIPTION_DESCRIPTION_MISSING
        elif parent == 'studyExtent':
            warning = EvaluationWarning.STUDY_EXTENT_DESCRIPTION_MISSING
    if warning:
        evaluation.append((
            warning,
            f'A Description is required.',
            node
        ))
    return evaluation


def _publisher_rule(node: Node) -> list:
    return _responsible_party_rule(node)


def _individual_name_rule(node: Node) -> list:
    evaluation = []
    givename = False
    surname = False
    for child in node.children:
        if child.name == names.GIVENNAME and child.content:
            givename = True
        if child.name == names.SURNAME and child.content:
            surname = True
    if givename and surname:
        evaluation = None
    else:
        evaluation.append((
            EvaluationWarning.INDIVIDUAL_NAME_INCOMPLETE,
            f'An individual\'s name should have both a "{names.GIVENNAME}" and a "{names.SURNAME}"',
            node
        ))
    return evaluation


def _responsible_party_rule(node: Node) -> list:
    evaluation = []
    userid = False
    orcid = False
    email = False
    for child in node.children:
        if child.name == names.USERID and child.content:
            userid = True
            if child.attributes.get('directory') in ['http://orcid.org', 'https://orcid.org']:
                orcid = True
        if child.name == names.ELECTRONICMAILADDRESS and child.content:
            email = True
    if not orcid:
        evaluation.append((
            EvaluationWarning.ORCID_ID_MISSING,
            f'An ORCID ID is recommended."',
            node
        ))
    if not userid:
        evaluation.append((
            EvaluationWarning.USER_ID_MISSING,
            f'A User ID should be provided. An ORCID ID is recommended."',
            node
        ))
    if not email:
        evaluation.append((
            EvaluationWarning.EMAIL_MISSING,
            f'An email address should be provided."',
            node
        ))
    return evaluation


def _metadata_provider_rule(node: Node) -> list:
    return _responsible_party_rule(node)


def _other_entity_rule(node: Node) -> list:
    evaluation = []
    description = any(
        child.name == names.ENTITYDESCRIPTION and child.content
        for child in node.children
    )

    if not description:
        evaluation.append((
            EvaluationWarning.OTHER_ENTITY_DESCRIPTION_MISSING,
            f'Entity Description is highly recommended."',
            node
        ))
    return evaluation


def _personnel_rule(node: Node) -> list:
    return _responsible_party_rule(node)


def _title_rule(node: Node) -> list:
    evaluation = []
    title = node.content
    if title is not None:
        if node.parent is not None and node.parent.name == names.DATASET:
            length = len(normalize(title).split(" "))
            if length < 5:
                evaluation.append((
                    EvaluationWarning.TITLE_TOO_SHORT,
                    f'The title "{title}" is too short. A title should have at least 5 words;'
                    f' between 7 and 20 words is recommended.',
                    node
                ))
    return evaluation


# ===================== End of rules section =====================


def node(node: Node):
    """
    Evaluates a given node for rule compliance.

    Args:
        node: Node instance to be evaluated

    Returns:
        None or evaluation dict
    """
    evaluation = None
    if node.name in rules:
        evaluation = rules[node.name](node)
    return evaluation


def tree(root: Node, warnings: list):
    """
    Recursively walks from the root node and evaluates
    each child node for rule compliance.

    Args:
        root: Node instance of root for evaluation
        warnings: List of warnings collected during the evaluation

    Returns:
        None
    """
    evaluation = node(root)
    if evaluation is not None:
        warnings.extend(evaluation)
    for child in root.children:
        tree(child, warnings)


# Rule function pointers
rules = {
    names.ASSOCIATEDPARTY: _associated_responsible_party_rule,
    names.CONTACT: _contact_rule,
    names.CREATOR: _creator_rule,
    names.DATASET: _dataset_rule,
    names.DATATABLE: _datatable_rule,
    names.DESCRIPTION: _description_rule,
    names.INDIVIDUALNAME: _individual_name_rule,
    names.METADATAPROVIDER: _metadata_provider_rule,
    names.OTHERENTITY: _other_entity_rule,
    names.PERSONNEL: _personnel_rule,
    names.PUBLISHER: _publisher_rule,
    names.TITLE: _title_rule,
}

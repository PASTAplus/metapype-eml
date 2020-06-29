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
from metapype.eml.evaluation_warnings import EvaluationWarning


logger = daiquiri.getLogger("evaluate: " + __name__)


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
    keywordset_node = None
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
            keywordset_node = child
        elif child.name == names.METHODS:
            methods_node = child
        elif child.name == names.PROJECT:
            project_node = child

    if abstract_node:
        content = abstract_node.content if abstract_node.content else ''
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
    if not (keywordset_node and keywordset_node.children):
        evaluation.append((
            EvaluationWarning.KEYWORDS_MISSING,
            f'Keywords should be provided to make the dataset more discoverable.',
            node
        ))
    elif len(keywordset_node.children) < 5:
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
    return evaluation


def _description_rule(node: Node) -> list:
    # Various description nodes are required but since they have TextType, the rules allow them to be empty.
    # Require them to have nonempty content.
    evaluation = []
    warning = None
    if not node.content:
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
    for child in node.children:
        if child.name == names.USERID and child.content:
            userid = True
            if child.attributes.get('directory') == 'https://orcid.org':
                orcid = True
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
        length = len(title.split(" "))
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
    names.TITLE: _title_rule,
}

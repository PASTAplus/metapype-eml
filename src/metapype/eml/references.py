#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: references

:Synopsis:

:Author:
    servilla

:Created:
    2/23/21
"""
import daiquiri

import metapype.eml.names as names
from metapype.model.node import Node


logger = daiquiri.getLogger(__name__)


def _register_ids(node: Node) -> dict:
    id_register = dict()
    for a, v in node.attributes.items():
        if a == "id":
            id_register[v] = node
    for child in node.children:
        _ = _register_ids(child)
        for k in _.keys():
            if k in id_register:
                msg = f"Duplicate use of ID: '{k}'"
                raise ValueError(msg)
        id_register = {**id_register, **_}
    return id_register


def expand(node: Node):
    references = list()
    node.find_all_descendants(names.REFERENCES, references)
    ids = _register_ids(node)
    for reference in references:
        if reference.content not in ids:
            msg = f"ID not found for REFERENCE '{reference}'"
            raise ValueError(msg)
        source_node = ids[reference.content]
        destination_node = reference.parent
        destination_node.remove_child(reference)
        Node.delete_node_instance(reference.id)
        for source_child in source_node.children:
            source_child_copy = source_child.copy()
            destination_node.add_child(source_child_copy)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_node

:Synopsis:

:Author:
    servilla
    costa
    ide
  
:Created:
    6/18/18
"""
import daiquiri
import pytest

from metapype.eml import names
from metapype.eml import validate
from metapype.model.node import Node
from metapype.model.node import Shift


logger = daiquiri.getLogger("test_node: " + __name__)


@pytest.fixture()
def node():
    return Node(names.EML)


def test_add_attribute(node):
    node.add_attribute("packageId", "test.1.1")
    node.add_attribute("system", "metapype")
    attributes = node.attributes
    for attribute in attributes:
        assert attribute in ["packageId", "system"]
        value = attributes[attribute]
        assert value in ["test.1.1", "metapype"]


def test_add_child(node):
    child_1 = Node(names.ACCESS)
    node.add_child(child_1)
    children = node.children
    assert child_1 is children[0]
    child_2 = Node(names.DATASET)
    node.add_child(child_2, 0)
    assert child_2 is children[0]


def test_copy():
    creator = Node(names.CREATOR)
    creator.add_attribute("id", "creator")
    creator.add_namespace("eml", "https://eml.ecoinformatics.org/eml-2.2.0")
    individual_name = Node(names.INDIVIDUALNAME)
    creator.add_child(individual_name)
    given_name = Node(names.GIVENNAME, content="Chase")
    given_name.add_attribute("lang", "Spanish")
    individual_name.add_child(given_name)
    sur_name = Node(names.SURNAME, content="Gaucho")
    sur_name.add_attribute("lang", "Spanish")
    individual_name.add_child(sur_name)
    individual_name = Node(names.INDIVIDUALNAME)
    creator.add_child(individual_name)
    given_name = Node(names.GIVENNAME, content="Cactus")
    individual_name.add_child(given_name)
    sur_name = Node(names.SURNAME, content="Jack")
    individual_name.add_child(sur_name)
    validate.tree(creator)
    creator_copy = creator.copy()
    validate.tree(creator_copy)
    assert is_deep_copy(creator, creator_copy)


def test_create_node(node):
    assert node is not None


def test_find_child(node):
    access = Node(names.ACCESS)
    node.add_child(access)
    child = node.find_child(names.ACCESS)
    assert access is child

    allow = Node(names.ALLOW)
    access.add_child(allow)
    grandchild = node.find_child(names.ALLOW)
    assert grandchild is None

    permission = Node(names.PERMISSION)
    allow.add_child(permission)
    great_grandchild = node.find_child(names.PERMISSION)
    assert great_grandchild is None

    child = node.find_child("nonesuch")
    assert child is None


def test_find_descendant(node):
    access = Node(names.ACCESS)
    node.add_child(access)
    child = node.find_descendant(names.ACCESS)
    assert access is child

    allow = Node(names.ALLOW)
    access.add_child(allow)
    grandchild = node.find_descendant(names.ALLOW)
    assert grandchild is allow

    permission = Node(names.PERMISSION)
    allow.add_child(permission)
    great_grandchild = node.find_descendant(names.PERMISSION)
    assert great_grandchild is permission

    child = node.find_descendant("nonesuch")
    assert child is None


def test_find_single_node_by_path(node):
    access = Node(names.ACCESS)
    node.add_child(access)
    child = node.find_single_node_by_path([names.ACCESS])
    assert access is child

    allow = Node(names.ALLOW)
    access.add_child(allow)
    grandchild = node.find_single_node_by_path([names.ACCESS, names.ALLOW])
    assert grandchild is allow

    permission = Node(names.PERMISSION)
    allow.add_child(permission)
    great_grandchild = node.find_single_node_by_path([names.ACCESS, names.ALLOW, names.PERMISSION])
    assert great_grandchild is permission

    child = node.find_single_node_by_path([names.ACCESS, names.ALLOW, "nonesuch"])
    assert child is None

    child = node.find_single_node_by_path([])
    assert child is None

    child = node.find_single_node_by_path(None)
    assert child is None


def test_find_all_nodes_by_path(node):
    access = Node(names.ACCESS)
    node.add_child(access)
    children = node.find_all_nodes_by_path([names.ACCESS])
    assert children == [access]

    allow = Node(names.ALLOW)
    access.add_child(allow)
    grandchildren = node.find_all_nodes_by_path([names.ACCESS, names.ALLOW])
    assert grandchildren == [allow]

    principal_1 = Node(names.PRINCIPAL)
    allow.add_child(principal_1)
    principal_2 = Node(names.PRINCIPAL)
    allow.add_child(principal_2)
    great_grandchildren = node.find_all_nodes_by_path([names.ACCESS, names.ALLOW, names.PRINCIPAL])
    assert great_grandchildren == [principal_1, principal_2]

    child = node.find_all_nodes_by_path([names.ACCESS, names.ALLOW, "nonesuch"])
    assert child == []

    child = node.find_all_nodes_by_path([])
    assert child == []

    child = node.find_all_nodes_by_path(None)
    assert child == []


def test_remove_child(node):
    access = Node(names.ACCESS)
    node.add_child(access)
    child = node.children[0]
    assert access is child
    node.remove_child(child)
    assert access not in node.children


def test_replace_child():
    individual_name = Node(names.INDIVIDUALNAME)
    sur_name_1 = Node(names.SURNAME, parent=individual_name)
    sur_name_1.content = "Gaucho"
    individual_name.add_child(sur_name_1)
    sur_name_2 = Node(names.SURNAME, parent=individual_name)
    sur_name_2.content = "Carroll"
    assert sur_name_1 in individual_name.children
    assert sur_name_2 not in individual_name.children
    individual_name.replace_child(old_child=sur_name_1, new_child=sur_name_2)
    assert sur_name_2 in individual_name.children
    assert sur_name_1 not in individual_name.children

    # Test for old child removal from node store
    assert sur_name_1.id not in Node.store

    # Test for child node type mismatch
    given_name = Node(names.GIVENNAME)
    given_name.content = "Chase"
    with pytest.raises(ValueError):
        individual_name.replace_child(old_child=sur_name_2, new_child=given_name)


def test_shift():
    individual_name_1 = Node(names.INDIVIDUALNAME)
    individual_name_2 = Node(names.INDIVIDUALNAME)
    individual_name_3 = Node(names.INDIVIDUALNAME)
    individual_name_4 = Node(names.INDIVIDUALNAME)
    organization_name = Node(names.ORGANIZATIONNAME)
    position_name = Node(names.POSITIONNAME)

    # Test shift right
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    contact.add_child(child=position_name)
    shift_index = contact.shift(child=individual_name_2, direction=Shift.RIGHT)
    assert shift_index == 3
    assert contact.children[3] is individual_name_2

    # Test shift left
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    contact.add_child(child=position_name)
    shift_index = contact.shift(child=individual_name_2, direction=Shift.LEFT)
    assert shift_index == 1
    assert contact.children[1] is individual_name_2

    # Test shift on edge right
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    contact.add_child(child=position_name)
    index = contact.children.index(individual_name_3)
    shift_index = contact.shift(child=individual_name_3, direction=Shift.RIGHT)
    assert index == shift_index

    # Test shift on edge left
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    contact.add_child(child=position_name)
    index = contact.children.index(individual_name_1)
    shift_index = contact.shift(child=individual_name_1, direction=Shift.LEFT)
    assert index == shift_index

    # Test hard shift on edge right
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    index = contact.children.index(individual_name_3)
    shift_index = contact.shift(child=individual_name_3, direction=Shift.RIGHT)
    assert index == shift_index

    # Test hard shift on edge left
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    index = contact.children.index(individual_name_1)
    shift_index = contact.shift(child=individual_name_1, direction=Shift.LEFT)
    assert index == shift_index

    # Test distant sibling shift right
    contact = Node(names.CONTACT)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    contact.add_child(child=position_name)
    contact.add_child(child=individual_name_4)
    shift_index = contact.shift(child=individual_name_3, direction=Shift.RIGHT)
    index = contact.children.index(individual_name_3)
    assert index == shift_index

    # Test distant sibling shift left
    contact = Node(names.CONTACT)
    contact.add_child(child=individual_name_1)
    contact.add_child(child=organization_name)
    contact.add_child(child=individual_name_2)
    contact.add_child(child=individual_name_3)
    contact.add_child(child=individual_name_4)
    contact.add_child(child=position_name)
    shift_index = contact.shift(child=individual_name_2, direction=Shift.LEFT)
    index = contact.children.index(individual_name_2)
    assert index == shift_index


def test_get_node():
    access = Node(names.ACCESS)
    node = Node.get_node_instance(access.id)
    assert access is node


def test_delete_node():
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
    node = Node.get_node_instance(principal.id)
    assert principal is node
    Node.delete_node_instance(eml.id)
    assert principal.id not in Node.store


def test_delete_node_no_children():
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
    node = Node.get_node_instance(principal.id)
    assert principal is node
    Node.delete_node_instance(eml.id, children=False)
    assert principal.id in Node.store


def is_deep_copy(node1: Node, node2: Node) -> bool:
    if id(node1) == id(node2):
        return False

    if node1.name != node2.name:
        return False

    if node1.content != node2.content:
        return False

    if node1.tail != node2.tail:
        return False

    if len(node1.attributes) != len(node2.attributes):
        return False
    else:
        for key in node1.attributes.keys():
            try:
                if node1.attributes[key] != node2.attributes[key]:
                    return False
            except KeyError:
                return False

    if len(node1.nsmap) != len(node2.nsmap):
        return False
    else:
        for key in node1.nsmap.keys():
            try:
                if node1.nsmap[key] != node2.nsmap[key]:
                    return False
            except KeyError:
                return False

    if node1.prefix != node2.prefix:
        return False

    if len(node1.extras) != len(node2.extras):
        return False
    else:
        for key in node1.extras.keys():
            try:
                if node1.extras[key] != node2.extras[key]:
                    return False
            except KeyError:
                return False

    if len(node1.children) != len(node2.children):
        return False
    else:
        for index in range(len(node1.children)):
            child1 = node1.children[index]
            child2 = node2.children[index]
            return is_deep_copy(child1, child2)

    return True

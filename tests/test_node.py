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
    node = Node(names.GIVENNAME)
    node.content = "Chase"
    validate.node(node)
    node_copy = node.copy()
    validate.node(node_copy)


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
    assert grandchild is allow

    permission = Node(names.PERMISSION)
    allow.add_child(permission)
    great_grandchild = node.find_child(names.PERMISSION)
    assert great_grandchild is permission

    child = node.find_child("nonesuch")
    assert child is None


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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_node_store_scope

:Synopsis:
    Tests context isolation of node store. Tests both:
        Isolation: two concurrent “requests” (threads) don’t see each other’s nodes when each uses its own store scope.
        Cleanup: the store is cleared even if an exception happens inside the scope.

:Author:
    ChatGPT 5.2
    ide

:Created:
    3/3/2026
"""

import threading
import queue
import pytest

from metapype.model.node import Node


def _worker_handshake(name: str,
                      ready_q: "queue.Queue[tuple[str, str]]",
                      other_id_q: "queue.Queue[str]",
                      result_q: "queue.Queue[tuple[str, str, bool, int]]"):
    """
    Worker thread handshake:
      - create a store scope
      - create node
      - announce (name, my_id) on ready_q
      - wait to receive other_id on other_id_q
      - test visibility of other_id in this scope
      - report results and store size
    """
    with Node.store_scope(clear_on_exit=True) as store:
        n = Node(name=name)
        my_id = n.id
        ready_q.put((name, my_id))

        other_id = other_id_q.get()
        can_see_other = Node.get_node_instance(other_id) is not None

        result_q.put((name, my_id, can_see_other, len(store)))


def test_store_isolation_and_no_clobbering():
    ready_q: "queue.Queue[tuple[str, str]]" = queue.Queue()
    other1_q: "queue.Queue[str]" = queue.Queue()
    other2_q: "queue.Queue[str]" = queue.Queue()
    result_q: "queue.Queue[tuple[str, str, bool, int]]" = queue.Queue()

    t1 = threading.Thread(target=_worker_handshake, args=("t1", ready_q, other1_q, result_q), daemon=True)
    t2 = threading.Thread(target=_worker_handshake, args=("t2", ready_q, other2_q, result_q), daemon=True)
    t1.start()
    t2.start()

    # Collect ids from both threads
    (name_a, id_a) = ready_q.get(timeout=2)
    (name_b, id_b) = ready_q.get(timeout=2)

    # Send each thread the other thread's id
    if name_a == "t1":
        other1_q.put(id_b)
        other2_q.put(id_a)
    else:
        other1_q.put(id_a)
        other2_q.put(id_b)

    # Collect results
    r1 = result_q.get(timeout=2)
    r2 = result_q.get(timeout=2)

    t1.join(timeout=2)
    t2.join(timeout=2)

    # Assert neither can see the other's node
    # r = (name, my_id, can_see_other, store_len)
    assert r1[2] is False
    assert r2[2] is False

    # Each store should have exactly 1 node during the scope (the one it created)
    assert r1[3] == 1
    assert r2[3] == 1


def test_store_clears_on_exception():
    """
    If an exception occurs inside store_scope(clear_on_exit=True),
    the store dict should be cleared.
    """
    store = {}
    with pytest.raises(RuntimeError):
        with Node.store_scope(store, clear_on_exit=True):
            Node(name="boom")
            assert len(store) == 1
            raise RuntimeError("kaboom") # Force an exception

    # cleared after scope exits
    assert store == {}


def test_store_restores_previous_context():
    """
    Demonstrates nesting: after inner scope exits, previous store is restored.
    """
    outer = {}
    inner = {}

    with Node.store_scope(outer, clear_on_exit=True):
        n1 = Node("outer")
        assert Node.get_node_instance(n1.id) is n1
        assert len(outer) == 1

        with Node.store_scope(inner, clear_on_exit=True):
            n2 = Node("inner")
            assert Node.get_node_instance(n2.id) is n2
            # outer node not visible in inner store
            assert Node.get_node_instance(n1.id) is None
            assert len(inner) == 1

        # after inner exits, outer context is restored
        assert Node.get_node_instance(n1.id) is n1
        assert Node.get_node_instance(n2.id) is None

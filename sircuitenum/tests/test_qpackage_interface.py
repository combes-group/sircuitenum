import numpy as np
import pytest
import os
import itertools
import networkx as nx
import SQcircuit as sq

from sircuitenum import qpackage_interface as pi
from sircuitenum import utils


# Make some test circuits
TEST_CIRCUITS = [
    [[(0, 1)], [("L",)]],
    [[(0, 1)], [("L", "J")]],
    [[(0, 1)], [("C", "J", "L")]],
    [[(0, 1), (1, 2), (2, 0)], [("L",), ("J",), ("J",)]],
    [[(0, 1), (1, 2), (2, 3), (2, 4), (3, 4), (4, 0)],
     [("C",), ("C", "J"), ("C", "L"), ("C", "J", "L"),
      ("C", "L"), ("C",)]],
    [[(0, 1), (1, 2), (2, 3), (3, 0),
      (0, 4), (1, 4), (2, 4), (3, 4)],
     [("L",), ("C", "L"), ("L",), ("C", "J", "L"),
      ("L",), ("L",), ("C",), ("J",)]],
    [[(0, 1)], [("C",)]]
    ]


def test_single_edge_loop_knitting():

    # Go through test circuits
    edges, circuit = TEST_CIRCUITS[0][0], TEST_CIRCUITS[0][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == circuit
    assert e2 == edges

    edges, circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == [("J",), ("L",), ("L",)]
    assert e2 == [(0, 1), (0, 2), (2, 1)]

    edges, circuit = TEST_CIRCUITS[2][0], TEST_CIRCUITS[2][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == [("C", "J"), ("L",), ("L",)]
    assert e2 == [(0, 1), (0, 2), (2, 1)]

    edges, circuit = TEST_CIRCUITS[3][0], TEST_CIRCUITS[3][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == circuit
    assert e2 == edges

    edges, circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == [("C",), ("C", "J"), ("C", "L"), ("C", "J"),
                  ("L",), ("L",), ("C", "L"), ("C",)]
    assert e2 == [(0, 1), (1, 2), (2, 3), (2, 4), (2, 5),
                  (5, 4), (3, 4), (4, 0)]

    edges, circuit = TEST_CIRCUITS[5][0], TEST_CIRCUITS[5][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == [("L",), ("C", "L"), ("L",),
                  ("C", "J"), ("L",), ("L",),
                  ("L",), ("L",), ("C",), ("J",)]
    assert e2 == [(0, 1), (1, 2), (2, 3), (3, 0),
                  (3, 5), (5, 0), (0, 4),
                  (1, 4), (2, 4), (3, 4)]

    edges, circuit = TEST_CIRCUITS[6][0], TEST_CIRCUITS[6][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert c2 == circuit
    assert e2 == edges


def test_inductive_subgraph():

    # Go through test circuits
    edges, circuit = TEST_CIRCUITS[0][0], TEST_CIRCUITS[0][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == [(0, 1)]

    edges, circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == [(0, 1)]

    edges, circuit = TEST_CIRCUITS[2][0], TEST_CIRCUITS[2][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == [(0, 1)]

    edges, circuit = TEST_CIRCUITS[3][0], TEST_CIRCUITS[3][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == [(0, 1), (1, 2), (2, 0)]

    edges, circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == [(1, 2), (2, 3), (2, 4), (3, 4)]

    edges, circuit = TEST_CIRCUITS[5][0], TEST_CIRCUITS[5][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (3, 4)]

    edges, circuit = TEST_CIRCUITS[6][0], TEST_CIRCUITS[6][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J", "L"])
    assert e2 == []


def test_find_loops():

    # Go through test circuits
    edges, circuit = TEST_CIRCUITS[0][0], TEST_CIRCUITS[0][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    assert loops == []

    edges, circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    assert loops == [(0, 1)]

    edges, circuit = TEST_CIRCUITS[2][0], TEST_CIRCUITS[2][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    assert loops == [(0, 1)]

    edges, circuit = TEST_CIRCUITS[3][0], TEST_CIRCUITS[3][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    assert loops == [(0, 1, 2)]

    edges, circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    ans = [(2, 3, 4), (2, 4)]
    assert len(loops) == len(ans)
    for loop in ans:
        assert loop in ans

    edges, circuit = TEST_CIRCUITS[5][0], TEST_CIRCUITS[5][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    ans = [(0, 1, 2, 3), (0, 1, 4), (0, 3), (0, 3, 4)]
    assert len(loops) == len(ans)
    for l in ans:
        assert l in ans

    edges, circuit = TEST_CIRCUITS[6][0], TEST_CIRCUITS[6][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J", "L"])
    assert loops == []


def test_gen_param_dict():

    # Go through test circuits
    for i in range(len(TEST_CIRCUITS)):
        edges, circuit = TEST_CIRCUITS[i][0], TEST_CIRCUITS[i][1]
        param_dict = pi.gen_param_dict(circuit, edges, params=utils.ELEM_DICT)
        counts = utils.count_elems_mapped(circuit)

        assert len(param_dict['c_list']) == counts["C"]
        assert len(param_dict['l_list']) == counts["L"]
        assert len(param_dict['j_list']) == counts["J"]
        assert len(param_dict['cj_list']) == counts["J"]

        assert all(x == utils.ELEM_DICT['C']['default_value']
                   for x in param_dict['c_list'])
        assert all(x == utils.ELEM_DICT['L']['default_value']
                   for x in param_dict['l_list'])
        assert all(x == utils.ELEM_DICT['J']['default_value']
                   for x in param_dict['j_list'])
        assert all(x == utils.ELEM_DICT['CJ']['default_value']
                   for x in param_dict['cj_list'])

        assert utils.ELEM_DICT['C']['default_unit'] == param_dict['c_units']
        assert utils.ELEM_DICT['L']['default_unit'] == param_dict['l_units']
        assert utils.ELEM_DICT['J']['default_unit'] == param_dict['j_units']
        assert utils.ELEM_DICT['CJ']['default_unit'] == param_dict['cj_units']


def test_convert_circuit_to_SQcircuit():
    for i in range(len(TEST_CIRCUITS)):
        assert True


if __name__ == "__main__":
    # edges, circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    edges, circuit = [[(0, 1), (1, 2), (2, 3),
                       (2, 4), (3, 4), (4, 0)],
                      [("C", "J"), ("C", "J"), ("C", "L"),
                      ("C", "J", "L"), ("C", "L"), ("C", "J")]]

    # edges, circuit = [[(0, 1), (1, 2), (2, 3), (3,0)],
    # [("C", "J"), ("C", "J"), ("C", "J"), ("C", "J")]]
    # edges, circuit = [(0, 1)], [("C", "J")]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)

    ind_edges = pi.inductive_subgraph(c2, e2)
    G = nx.from_edgelist(ind_edges)
    cb = nx.cycle_basis(nx.Graph(G))

    # cir = pi.convert_circuit_to_SQcircuit(circuit, edges)
    cir = pi.convert_circuit_to_CircuitQ(circuit, edges)

    # test_single_edge_loop_knitting()
    # test_inductive_subgraph()
    # test_find_loops()
    # test_gen_param_dict()
    # Find loops in the inductive subgraph
    # And filter out any edges that we added
    # loop_lst = [sorted(c) for c in nx.cycle_basis(nx.Graph(G))]
    # loops = pi.find_loops()

    # define the circuit elements
    # C = sq.Capacitor(0.5, 'GHz')
    # JJ = sq.Junction(5.0,'GHz')

    # # define the circuit
    # elements = {
    #     (0, 1): [C, JJ]
    # }

    # cr = sq.Circuit(elements)

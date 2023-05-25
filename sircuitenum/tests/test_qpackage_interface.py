import numpy as np
import pytest
import os
import itertools
import networkx as nx

from sircuitenum import qpackage_interface as pi
from sircuitenum import utils


# Make some test circuits 
TEST_CIRCUITS = [
    [[(0,1)],[("L",)]],
    [[(0,1)],[("L","J")]],
    [[(0,1)],[("C","J","L")]],
    [[(0,1),(1,2),(2,0)],[("L",),("J",),("J",)]],
    [[(0,1), (1,2), (2,3), (2,4), (3,4)],
    [("C",),("J",),("L",), ("J","L"), ("L",)]],
    [[(0,1), (1,2),     (2,3),     (3,0),     (0,4),  (1,4),  (2,4), (3,4)],
    [("L",),("C","L"), ("L",), ("C","J","L"), ("L",), ("L",),("C",),("J",)]],
    [[(0,1)],[("C",)]]
    ]

def test_single_edge_loop_knitting():
    
    # Go through test circuits
    edges,circuit = TEST_CIRCUITS[0][0], TEST_CIRCUITS[0][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == circuit)
    assert(e2 == edges)

    edges,circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == [("J",),("L",),("L",)])
    assert(e2 == [(0,1),(0,2),(2,1)])

    edges,circuit = TEST_CIRCUITS[2][0], TEST_CIRCUITS[2][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == [("C","J"),("L",),("L",)])
    assert(e2 == [(0,1),(0,2),(2,1)])

    edges,circuit = TEST_CIRCUITS[3][0], TEST_CIRCUITS[3][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == circuit)
    assert(e2 == edges)

    edges,circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == [("C",),("J",),("L",), ("J",), ("L",),("L",),("L",)])
    assert(e2 == [(0,1), (1,2), (2,3), (2,4), (2,5), (5,4), (3,4)])


    edges,circuit = TEST_CIRCUITS[5][0], TEST_CIRCUITS[5][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == [("L",),("C","L"), ("L",), ("C","J"),("L",),("L",), ("L",), ("L",),("C",),("J",)])
    assert(e2 == [(0,1), (1,2),     (2,3),   (3,0),    (3,5), (5,0), (0,4),  (1,4),  (2,4), (3,4)])


    edges,circuit = TEST_CIRCUITS[6][0], TEST_CIRCUITS[6][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)
    assert(c2 == circuit)
    assert(e2 == edges)


def test_inductive_subgraph():


    # Go through test circuits
    edges,circuit = TEST_CIRCUITS[0][0], TEST_CIRCUITS[0][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [(0,1)])

    edges,circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [(0,1)])

    edges,circuit = TEST_CIRCUITS[2][0], TEST_CIRCUITS[2][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [(0,1)])

    edges,circuit = TEST_CIRCUITS[3][0], TEST_CIRCUITS[3][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [(0,1),(1,2),(2,0)])

    edges,circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [(1,2), (2,3), (2,4), (3,4)])

    edges,circuit = TEST_CIRCUITS[5][0], TEST_CIRCUITS[5][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [(0,1), (1,2), (2,3), (3,0), (0,4), (1,4), (3,4)])

    edges,circuit = TEST_CIRCUITS[6][0], TEST_CIRCUITS[6][1]
    e2 = pi.inductive_subgraph(circuit, edges, ind_elem=["J","L"])
    assert(e2 == [])




def test_find_loops():
    
    # Go through test circuits
    edges,circuit = TEST_CIRCUITS[0][0], TEST_CIRCUITS[0][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    assert(loops == [])

    edges,circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    assert(loops == [[0,1]])

    edges,circuit = TEST_CIRCUITS[2][0], TEST_CIRCUITS[2][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    assert(loops == [[0,1]])

    edges,circuit = TEST_CIRCUITS[3][0], TEST_CIRCUITS[3][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    assert(loops == [[0,1,2]])

    edges,circuit = TEST_CIRCUITS[4][0], TEST_CIRCUITS[4][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    ans = [[2,3,4], [2,4]]
    assert(len(loops) == len(ans))
    for l in ans:
        assert(l in ans)

    edges,circuit = TEST_CIRCUITS[5][0], TEST_CIRCUITS[5][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    ans = [[0,1,2,3],[0,1,4], [1,2],[0,3],[0,3,4]]
    print(loops)
    assert(len(loops) == len(ans))
    for l in ans:
        assert(l in ans)

    edges,circuit = TEST_CIRCUITS[6][0], TEST_CIRCUITS[6][1]
    loops = pi.find_loops(circuit, edges, ind_elem=["J","L"])
    assert(loops == [])

if __name__ == "__main__":
    edges,circuit = TEST_CIRCUITS[1][0], TEST_CIRCUITS[1][1]
    c2, e2 = pi.single_edge_loop_kiting(circuit, edges)

    ind_edges = pi.inductive_subgraph(c2, e2)
    G = nx.from_edgelist(ind_edges)
    cb = nx.cycle_basis(nx.Graph(G))

    test_single_edge_loop_knitting()
    test_inductive_subgraph()
    test_find_loops()
    # Find loops in the inductive subgraph
    # And filter out any edges that we added
    # loop_lst = [sorted(c) for c in nx.cycle_basis(nx.Graph(G))]
    # loops = pi.find_loops()
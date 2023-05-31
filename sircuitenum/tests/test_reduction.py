import pytest
import itertools

import networkx as nx
import numpy as np
import pandas as pd

from sircuitenum import reduction as red
from sircuitenum import enum
from sircuitenum import utils


ALL_CONNECTED_3 = [[utils.COMBINATION_DICT[c] for c in np.base_repr(i,3).zfill(3)] for i in range(27)]
NON_ISOMORPHIC_3 = [
                  (("L",),("C",),("J",)),
                  (("L",),("J",),("J",)),
                  (("C",),("J",),("J",)),
                  (("J",),("J",),("J",))
                 ]
NON_SERIES_3 = list(itertools.permutations([("L",),("C",),("J",)],3))
NON_SERIES_3 += [ 
                (("L",),("J",),("J",)),
                (("J",),("L",),("J",)),
                (("J",),("J",),("L",))
              ]
NON_SERIES_3 += [ 
                (("C",),("J",),("J",)),
                (("J",),("C",),("J",)),
                (("J",),("J",),("C",))
              ]
NON_SERIES_3 += [
                (("J",),("J",),("J",))
              ]


def test_convert_circuit_to_port_graph():

    # Simple example
    edges = [(0,1)]
    circuit = [("C",)]
    G = red.convert_circuit_to_port_graph(circuit, edges)
    exp_nodes = ["v0_p0", "v1_p0", "C0_p0", "C0_p1"]
    exp_edges = [("v0_p0", "C0_p0"), ("C0_p0", "C0_p1"),("C0_p1", "v1_p0")]
    assert len(G.nodes) == len(exp_nodes)
    assert len(G.edges) == len(exp_edges)
    assert all(x in G.nodes for x in exp_nodes)
    assert all(x in G.edges for x in exp_edges)


    # More complicated example
    edges = [(0,1), (1,2), (2,0)]
    circuit = [("C",),("L",),("C", "L", "J")]
    G = red.convert_circuit_to_port_graph(circuit, edges)
    exp_nodes = ['v0_p0', 'v0_p1', 'v1_p0', 'v1_p1', 'v2_p0',
                 'v2_p1', 'C0_p0', 'C0_p1', 'L0_p0', 'L0_p1',
                 'CJL0_p0', 'CJL0_p1']
    exp_edges = [('v0_p0', 'v0_p1'), ('v0_p0', 'C0_p0'), ('v0_p1', 'CJL0_p1'),
                 ('v1_p0', 'v1_p1'), ('v1_p0', 'C0_p1'), ('v1_p1', 'L0_p0'),
                 ('v2_p0', 'v2_p1'), ('v2_p0', 'L0_p1'), ('v2_p1', 'CJL0_p0'),
                 ('C0_p0', 'C0_p1'), ('L0_p0', 'L0_p1'), ('CJL0_p0', 'CJL0_p1')]
    assert len(G.nodes) == len(exp_nodes)
    assert len(G.edges) == len(exp_edges)
    assert all(x in G.nodes for x in exp_nodes)
    assert all(x in G.edges for x in exp_edges)

def test_find_equiv_cir_series():
    assert(False)
    
def test_remove_series_elems():

    # Test a few obvious cases
    edges = [(0,1), (1,2), (2,0)]
    circuit = [("L",),("L",),("L",)]
    assert red.circuit_series_check(circuit, edges) is False

    edges = [(0,1), (1,2)]
    circuit = [("C",),("L",)]
    assert red.circuit_series_check(circuit, edges) is True

    edges = [(0,1), (1,2)]
    circuit = [("C",),("C",),("C",)]
    assert red.circuit_series_check(circuit, edges) is False

    # Some larger ones -- test the 2,3/3,4 connection
    edges = [(0,1), (1,2), (2,3), (2,4), (3,4)]
    circuit = [("C",),("J",),("C","J"), ("L","J"), ("L",)]
    assert red.circuit_series_check(circuit, edges) is True

    edges = [(0,1), (1,2), (2,3), (2,4), (3,4)]
    circuit = [("C",),("J",),("L",), ("L","J"), ("L",)]
    assert red.circuit_series_check(circuit, edges) is False

    edges = [(0,1), (1,2), (2,3), (2,4), (3,4)]
    circuit = [("C",),("J",),("C","J"), ("L","J"), ("L","J")]
    assert red.circuit_series_check(circuit, edges) is True

    # Test the full set of fully connected three nodes
    edges = [(0,1), (1,2), (2,0)]
    filt = [c for c in ALL_CONNECTED_3 if red.circuit_series_check(c, edges)]
    assert len(filt) == len(NON_SERIES_3)
    assert all(utils.circuit_in_set(c, NON_SERIES_3) for c in filt)

def test_non_isomorphic_set():

    # Test some obvious cases
    edges = [[(0,1), (1,2), (2,0)]]*6
    circuit = list(itertools.permutations([("C",),("L",),("J",)]))
    df = pd.DataFrame({"edges": edges, "circuit": circuit})
    filt =  red.non_isomorphic_set(df)
    assert filt.shape[0] == 1
    assert filt.edges.iloc[0] == [(0,1), (1,2), (2,0)]
    assert utils.circuit_in_set(filt.circuit.iloc[0],circuit)

    edges = [[(0,1), (1,2), (2,0)]]*6
    circuit = list(itertools.permutations([("L","J"),("C","J"),("C","L","J")]))
    df = pd.DataFrame({"edges": edges, "circuit": circuit})
    filt =  red.non_isomorphic_set(df)
    assert filt.shape[0] == 1
    assert filt.edges.iloc[0] == [(0,1), (1,2), (2,0)]
    assert utils.circuit_in_set(filt.circuit.iloc[0],circuit)

    edges = [[(0,1), (1,2), (2,0)]]*6
    circuit = list(itertools.permutations([("J","L"),("J","C"),("C","L","J")]))
    df = pd.DataFrame({"edges": edges, "circuit": circuit})
    filt = red.non_isomorphic_set(df)
    assert filt.shape[0] == 1
    assert filt.edges.iloc[0] == [(0,1), (1,2), (2,0)]
    assert utils.circuit_in_set(filt.circuit.iloc[0],circuit)

    # Test the full set of fully connected three nodes
    edges = [[(0,1), (1,2), (2,0)]]*len(NON_SERIES_3)
    df = pd.DataFrame({"edges": edges, "circuit": NON_SERIES_3})
    filt = red.non_isomorphic_set(df)
    assert filt.shape[0] == len(NON_ISOMORPHIC_3)
    assert all(utils.circuit_in_set(c, NON_ISOMORPHIC_3) for c in filt.circuit.values)


def test_full_reduction():

    # Test some obvious cases
    edges = [[(0,1), (1,2), (2,0)]]*6
    circuit = list(itertools.permutations([("C",),("L",),("J",)]))
    df = pd.DataFrame({"edges": edges, "circuit": circuit})
    filt =  red.full_reduction(df)
    assert filt.shape[0] == 1
    assert filt.edges.iloc[0] == [(0,1), (1,2), (2,0)]
    assert utils.circuit_in_set(filt.circuit.iloc[0],circuit)

    # Test the full set of fully connected three nodes
    edges = [[(0,1), (1,2), (2,0)]]*len(ALL_CONNECTED_3)
    df = pd.DataFrame({"edges": edges, "circuit": ALL_CONNECTED_3, "graph_index":1})
    filt = red.full_reduction(df)
    assert filt.shape[0] == len(NON_ISOMORPHIC_3)
    assert all(red.isomorphic_circuit_in_set(c, edges[0], NON_ISOMORPHIC_3) for c in filt.circuit.values)
    assert all(red.isomorphic_circuit_in_set(c, edges[0], filt.circuit.values) for c in NON_ISOMORPHIC_3)


def test_full_reduction_by_group():

    

    # Test the four node cycle circuit
    graph_index = 3
    G = utils.get_basegraphs(4)[graph_index]
    all_circuits = enum.generate_for_specific_graph(7, G, graph_index, return_vals=True)
    utils.convert_loaded_df(all_circuits, 4)

    filt = red.full_reduction_by_group(all_circuits)


    # A few hand picked examples -- make sure they're there/not
    edges = [(0,1), (1,2), (2,3), (3,0)]
    circuit = [("C",),("L",),("J",), ("L",)]
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values)

    # No JJ
    circuit = [("C",),("L",),("C",), ("L",)]
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values) is False
    circuit = [("C",),("C","L",),("C","L"), ("L",)]
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values) is False

    # Consecutive linear components
    circuit = [("C",),("J",),("L",), ("L",)]
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values) is False
    circuit = [("C",),("J",),("L",), ("J","L")]
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values)
    circuit = [("C",),("J",),("L",), ("C","L")]
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values)

    # Set that should be isomorphic, only one should be there
    circuit_set = []
    circuit_set.append([("J",),("J",),("J",), ("C",)])
    circuit_set.append([("J",),("J",),("C",), ("J",)])
    circuit_set.append([("J",),("C",),("J",), ("J",)])
    circuit_set.append([("C",),("J",),("J",), ("J",)])
    assert sum(utils.circuit_in_set(c, filt.circuit.values) for c in circuit_set) == 1
    assert red.isomorphic_circuit_in_set(circuit, edges, filt.circuit.values, filt.edges.values)



def test_isomorphic_circuit_in_set():
    # Test some obvious cases
    edges = [(0,1), (1,2), (2,0)]
    circuit = list(itertools.permutations([("C",),("L",),("J",)]))
    test_c = circuit.pop()
    assert red.isomorphic_circuit_in_set(test_c, edges, circuit)
    assert red.isomorphic_circuit_in_set([("C",),("J",),("J",)], edges, circuit) is False

    assert red.isomorphic_circuit_in_set(test_c, edges, circuit, [edges]*len(circuit))
    assert red.isomorphic_circuit_in_set([("C",),("J",),("J",)], edges, circuit, [edges]*len(circuit)) is False

def test_jj_present():
    assert red.jj_present([("J","L"),("J","C"),("C","L","J")])
    assert red.jj_present([("C","L"),("C","C"),("C","L","L")]) is False
    assert red.jj_present([("C",),("L",),("J",)])
    assert red.jj_present([("C",),("L",),("Q",)]) is False
    




if __name__ == "__main__":
    test_full_reduction_by_group()
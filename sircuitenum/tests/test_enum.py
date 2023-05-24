import numpy as np
import pytest
import os
import itertools

from sircuitenum import enum, utils
from sircuitenum import reduction as red

import numpy.random
numpy.random.seed(7)  # seed random number generation for all calls to rand_ops


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


MEMFNAME1 = 'file:cachedb?mode=memory&cache=shared'
MEMFNAME2 = 'file:cachedb2?mode=memory&cache=shared'

# =================================================================================================
# Test:  num_possible_circuits
# =================================================================================================
def test_num_possible_circuits():
    assert enum.num_possible_circuits(3, 2) == 3
    assert enum.num_possible_circuits(3, 3) == 36
    assert enum.num_possible_circuits(7, 3) == 392


# =================================================================================================
# Test:  totalNumPossible
# =================================================================================================
def test_num_possible_circuits():
    counts = enum.total_num_possible(7,3)
    print(counts)
    assert  counts['3'] == 36
    assert  counts['7'] == 392

def test_generate_for_specific_graph():

    # Most simple two node graph
    G = utils.get_basegraphs(2)[0]
    df = enum.generate_for_specific_graph(7, G, 0, return_vals=True)
    exp_circuits = ['0', '1', '2', '3', '4', '5', '6']
    assert [x for x in df['circuit'].values] == exp_circuits

    # Fully connected three node with no parallel stuff
    G = utils.get_basegraphs(3)[1]
    df = enum.generate_for_specific_graph(3, G, 1, return_vals=True)
    exp_circuits = ["".join([utils.COMBINATION_TO_CHAR[combo] for combo in circuit]) for circuit in ALL_CONNECTED_3]
    assert [x for x in df['circuit'].values] == exp_circuits

    ## Some random ones
    # Four nodes
    n_trials = 1000
    graph_index = 3
    n_nodes = 4
    base = 7
    G = utils.get_basegraphs(n_nodes)[graph_index]
    df = enum.generate_for_specific_graph(base, G, graph_index, return_vals=True)
    n_edges = len(G.edges)
    choices = [np.base_repr(x, base) for x in range(base)]
    for i in range(n_trials):
        random_circuit = [x for x in np.random.choice(choices, size=n_edges)]
        assert utils.circuit_in_set(random_circuit, df['circuit'].values)

    # Five nodes
    n_trials = 10000
    graph_index = 8
    n_nodes = 5
    base = 7
    G = utils.get_basegraphs(n_nodes)[graph_index]
    df = enum.generate_for_specific_graph(base, G, graph_index, return_vals=True)
    n_edges = len(G.edges)
    choices = [np.base_repr(x, base) for x in range(base)]
    for i in range(n_trials):
        random_circuit = [x for x in np.random.choice(choices, size=n_edges)]
        assert utils.circuit_in_set(random_circuit, df['circuit'].values)


def test_generate_graphs_nodes():
    
    # Most simple two node graph
    G = utils.get_basegraphs(2)[0]
    df = enum.generate_graphs_nodes(7, 2, return_vals=True)
    exp_circuits = ['0', '1', '2', '3', '4', '5', '6']
    assert [x for x in df['circuit'].values] == exp_circuits

    ## Some random ones
    # Three nodes
    n_trials = 100
    n_nodes = 3
    base = 7
    df = enum.generate_graphs_nodes(base, n_nodes, return_vals=True)
    grouped = df.groupby("graph_index")
    for graph_index, G in enumerate(utils.get_basegraphs(n_nodes)):
        subset = grouped.get_group(graph_index)
        n_edges = len(G.edges)
        choices = [np.base_repr(x, base) for x in range(base)]
        for i in range(n_trials):
            random_circuit = [x for x in np.random.choice(choices, size=n_edges)]
            assert utils.circuit_in_set(random_circuit, subset['circuit'].values)

    # Four nodes
    n_trials = 100
    n_nodes = 4
    base = 7
    df = enum.generate_graphs_nodes(base, n_nodes, return_vals=True)
    grouped = df.groupby("graph_index")
    for graph_index, G in enumerate(utils.get_basegraphs(n_nodes)):
        subset = grouped.get_group(graph_index)
        n_edges = len(G.edges)
        choices = [np.base_repr(x, base) for x in range(base)]
        for i in range(n_trials):
            random_circuit = [x for x in np.random.choice(choices, size=n_edges)]
            assert utils.circuit_in_set(random_circuit, subset['circuit'].values)



def test_generate_all_graphs():
    
    enum.generate_all_graphs(MEMFNAME1, MEMFNAME2,2,4,base=7)

    
    # test the 2 nodes I/O
    df_untrimmed = utils.get_circuit_data_batch(MEMFNAME1, n_nodes = 2)
    df_trimmed = utils.get_circuit_data_batch(MEMFNAME2, n_nodes = 2)

    df_untrimmed_good = enum.generate_graphs_nodes(base=7,n_nodes=2,return_vals=True)
    utils.convert_loaded_df(df_untrimmed_good, n_nodes = 2)
    df_trimmed_good = red.full_reduction(df_untrimmed_good)

    df_equality_check(df_untrimmed, df_untrimmed_good)
    df_equality_check(df_trimmed, df_trimmed_good)

    # test the 3 nodes I/0
    df_untrimmed = utils.get_circuit_data_batch(MEMFNAME1, n_nodes = 3)
    df_trimmed = utils.get_circuit_data_batch(MEMFNAME2, n_nodes = 3)

    df_untrimmed_good = enum.generate_graphs_nodes(base=7,n_nodes=3,return_vals=True)
    utils.convert_loaded_df(df_untrimmed_good, n_nodes = 3)
    df_trimmed_good = red.full_reduction(df_untrimmed_good)

    df_untrimmed = df_untrimmed.sort_values(by='unique_key')
    df_untrimmed_good = df_untrimmed_good.sort_values(by='unique_key')
    df_trimmed = df_trimmed.sort_values(by='unique_key')
    df_trimmed_good = df_trimmed_good.sort_values(by='unique_key')

    df_equality_check(df_untrimmed, df_untrimmed_good)
    df_equality_check(df_trimmed, df_trimmed_good)

    os.remove(MEMFNAME1)
    os.remove(MEMFNAME2)


def df_equality_check(df1, df2):
    assert(df1.shape == df2.shape)
    for i in range(df1.shape[0]):
        for k in df1.columns:
            v1 = df1.iloc[i][k]
            v2 = df2.iloc[i][k]
            if isinstance(v1, list):
                assert(len(v1) == len(v2))
                assert(all(x in v2 for x in v1))
                assert(all(x in v1 for x in v2))
            else:
                assert(v1==v2)



if __name__ == "__main__":
    test_generate_all_graphs()
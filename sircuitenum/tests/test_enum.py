import os
import itertools
from pathlib import Path

import numpy as np
import pandas as pd

from sircuitenum import enum, utils
from sircuitenum import reduction as red

import numpy.random
numpy.random.seed(7)  # seed random number generation for all calls to rand_ops


ALL_CONNECTED_3 = [[utils.COMBINATION_DICT[c]
                    for c in np.base_repr(i, 3).zfill(3)] for i in range(27)]
NON_ISOMORPHIC_3 = [
                  (("L",), ("C",), ("J",)),
                  (("L",), ("J",), ("J",)),
                  (("C",), ("J",), ("J",)),
                  (("J",), ("J",), ("J",))
                 ]
NON_SERIES_3 = list(itertools.permutations([("L",), ("C",), ("J",)], 3))
NON_SERIES_3 += [
                (("L",), ("J",), ("J",)),
                (("J",), ("L",), ("J",)),
                (("J",), ("J",), ("L",))
              ]
NON_SERIES_3 += [
                (("C",), ("J",), ("J",)),
                (("J",), ("C",), ("J",)),
                (("J",), ("J",), ("C",))
              ]
NON_SERIES_3 += [
                (("J",), ("J",), ("J",))
              ]


TEMP_FILE = "temp.db"


def test_num_possible_circuits():

    assert enum.num_possible_circuits(3, 2) == 3
    assert enum.num_possible_circuits(3, 3) == 36
    assert enum.num_possible_circuits(7, 3) == 392


def test_generate_for_specific_graph():

    # Most simple two node graph
    G = utils.get_basegraphs(2)[0]
    df = enum.generate_for_specific_graph(7, G, 0, return_vals=True)
    exp_circuits = ['0', '1', '2', '3', '4', '5', '6']
    assert [x for x in df['circuit'].values] == exp_circuits

    # Fully connected three node with no parallel stuff
    G = utils.get_basegraphs(3)[1]
    df = enum.generate_for_specific_graph(3, G, 1, return_vals=True)
    exp_circuits = ["".join([utils.COMBINATION_TO_CHAR[combo]
                             for combo in circuit])
                    for circuit in ALL_CONNECTED_3]
    assert [x for x in df['circuit'].values] == exp_circuits

    # Four nodes
    n_trials = 1000
    graph_index = 3
    n_nodes = 4
    base = 7
    G = utils.get_basegraphs(n_nodes)[graph_index]
    df = enum.generate_for_specific_graph(base, G, graph_index,
                                          return_vals=True)
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
    df = enum.generate_for_specific_graph(base, G, graph_index,
                                          return_vals=True)
    n_edges = len(G.edges)
    choices = [np.base_repr(x, base) for x in range(base)]
    for i in range(n_trials):
        random_circuit = [x for x in np.random.choice(choices, size=n_edges)]
        assert utils.circuit_in_set(random_circuit, df['circuit'].values)


def test_delete_table():

    # Generate 2 node circuits
    enum.generate_graphs_node(TEMP_FILE, 2, 7)
    # Should be one table in the file
    t1 = utils.list_all_tables(TEMP_FILE)
    enum.delete_table(TEMP_FILE, 2)
    # Should be zero tables in the file
    t2 = utils.list_all_tables(TEMP_FILE)

    assert len(t1) == 1
    assert len(t2) == 0

    os.remove(TEMP_FILE)


def test_find_equiv_cir_series():

    if Path(TEMP_FILE).exists():
        os.remove(TEMP_FILE)

    # Generate all the 2/3 node circuits
    enum.generate_all_graphs(TEMP_FILE, 2, 3, base=7)

    # Find the equivalent circuits for ones that would
    # be reduced
    edges = [(0, 2), (2, 1), (0, 1)]
    circuit = [("L",), ("L",), ("L",)]
    breakpoint()
    uid = enum.find_equiv_cir_series(TEMP_FILE, circuit, edges)
    c, e = red.remove_series_elems(circuit, edges)
    c2, e2 = utils.get_circuit_data(TEMP_FILE, uid)
    assert red.isomorphic_circuit_in_set(c, e, [c2])

    edges = [(0, 2), (2, 1), (0, 1)]
    circuit = [("C",), ("L",), ("L",)]
    uid = enum.find_equiv_cir_series(TEMP_FILE, circuit, edges)
    c, e = red.remove_series_elems(circuit, edges)
    c2, e2 = utils.get_circuit_data(TEMP_FILE, uid)
    assert red.isomorphic_circuit_in_set(c, e, [c2])

    edges = [(0, 2), (2, 1), (0, 1)]
    circuit = [("C",), ("C",), ("J",)]
    uid = enum.find_equiv_cir_series(TEMP_FILE, circuit, edges)
    c, e = red.remove_series_elems(circuit, edges)
    c2, e2 = utils.get_circuit_data(TEMP_FILE, uid)
    assert red.isomorphic_circuit_in_set(c, e, [c2])

    edges = [(0, 1), (1, 2), (2, 3)]
    circuit = [("C",), ("C",), ("J",)]
    uid = enum.find_equiv_cir_series(TEMP_FILE, circuit, edges)
    c, e = red.remove_series_elems(circuit, edges)
    c2, e2 = utils.get_circuit_data(TEMP_FILE, uid)
    assert red.isomorphic_circuit_in_set(c, e, [c2])

    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    circuit = [("C",), ("C",), ("J",), ("L",)]
    uid = enum.find_equiv_cir_series(TEMP_FILE, circuit, edges)
    c, e = red.remove_series_elems(circuit, edges)
    c2, e2 = utils.get_circuit_data(TEMP_FILE, uid)
    assert red.isomorphic_circuit_in_set(c, e, [c2])


def test_generate_graphs_node():

    # Most simple two node graph
    G = utils.get_basegraphs(2)[0]
    df = enum.generate_graphs_node(None, 2, 7, return_vals=True)
    exp_circuits = ['0', '1', '2', '3', '4', '5', '6']
    assert [x for x in df['circuit'].values] == exp_circuits

    # Three nodes
    n_trials = 100
    n_nodes = 3
    base = 7
    df = enum.generate_graphs_node(None, n_nodes, base, return_vals=True)
    grouped = df.groupby("graph_index")
    for graph_index, G in enumerate(utils.get_basegraphs(n_nodes)):
        subset = grouped.get_group(graph_index)
        n_edges = len(G.edges)
        choices = [np.base_repr(x, base) for x in range(base)]
        for i in range(n_trials):
            random_circuit = [x for x in
                              np.random.choice(choices, size=n_edges)]
            assert utils.circuit_in_set(random_circuit,
                                        subset['circuit'].values)

    # Four nodes
    n_trials = 100
    n_nodes = 4
    base = 7
    df = enum.generate_graphs_node(None, n_nodes, base, return_vals=True)
    grouped = df.groupby("graph_index")
    for graph_index, G in enumerate(utils.get_basegraphs(n_nodes)):
        subset = grouped.get_group(graph_index)
        n_edges = len(G.edges)
        choices = [np.base_repr(x, base) for x in range(base)]
        for i in range(n_trials):
            random_circuit = [x for x in
                              np.random.choice(choices, size=n_edges)]
            assert utils.circuit_in_set(random_circuit,
                                        subset['circuit'].values)


def test_generate_all_graphs():

    if Path(TEMP_FILE).exists():
        os.remove(TEMP_FILE)

    # Generate all the 2 and 3 node circuits
    enum.generate_all_graphs(TEMP_FILE, 2, 4, base=3)

    # Test the 2 nodes I/O
    df_untrimmed = utils.get_circuit_data_batch(TEMP_FILE, n_nodes=2)
    df_trimmed = utils.get_unique_qubits(TEMP_FILE, n_nodes=2)

    df_untrimmed_good = enum.generate_graphs_node(None, 2, 3, True)
    utils.convert_loaded_df(df_untrimmed_good, n_nodes=2)
    red.full_reduction(df_untrimmed_good)
    unique_qubits = np.logical_and(np.logical_and(
        df_untrimmed_good['in_non_iso_set'],
        df_untrimmed_good['has_jj']),
        df_untrimmed_good['no_series'])
    df_trimmed_good = df_untrimmed_good[unique_qubits]
    df_equality_check(df_untrimmed, df_untrimmed_good)
    df_equality_check(df_trimmed, df_trimmed_good)

    # Test the 3 nodes I/0
    df_untrimmed = utils.get_circuit_data_batch(TEMP_FILE, n_nodes=3)
    df_trimmed = utils.get_unique_qubits(TEMP_FILE, n_nodes=3)

    df_untrimmed_good = enum.generate_graphs_node(None, 3, 3, True)
    utils.convert_loaded_df(df_untrimmed_good, n_nodes=3)
    red.full_reduction(df_untrimmed_good)
    unique_qubits = np.logical_and(np.logical_and(
        df_untrimmed_good['in_non_iso_set'],
        df_untrimmed_good['has_jj']),
        df_untrimmed_good['no_series'])
    df_trimmed_good = df_untrimmed_good[unique_qubits]

    # Find equivalent circuits for the series reduced circuits
    equiv_cir = df_untrimmed_good['equiv_circuit'].values
    yes_series = np.logical_not(df_untrimmed_good['no_series'].values)
    for i in range(df_untrimmed_good.shape[0]):
        if yes_series[i]:
            row = df_untrimmed_good.iloc[i]
            equiv_cir[i] = enum.find_equiv_cir_series(TEMP_FILE,
                                                      row['circuit'],
                                                      row['edges']
                                                      )

    df_untrimmed = df_untrimmed.sort_index()
    df_untrimmed_good = df_untrimmed_good.sort_values(by="unique_key")
    df_trimmed = df_trimmed.sort_index()
    df_trimmed_good = df_trimmed_good.sort_values(by="unique_key")

    df_equality_check(df_untrimmed, df_untrimmed_good)
    df_equality_check(df_trimmed, df_trimmed_good)

    # Test the accuracy
    df2 = utils.get_unique_qubits(TEMP_FILE, n_nodes=2)
    df3 = utils.get_unique_qubits(TEMP_FILE, n_nodes=3)
    df3 = df3[df3['graph_index'] == 1]
    df4 = utils.get_unique_qubits(TEMP_FILE, n_nodes=4)
    df4 = df4[df4['graph_index'] == 3]

    assert df2.shape[0] == 1
    assert df3.shape[0] == len(NON_ISOMORPHIC_3)

    edges = [(0, 1), (1, 2), (2, 0)]
    for c in NON_ISOMORPHIC_3:
        assert red.isomorphic_circuit_in_set(c, edges, df3.circuit.values)

    # A set of four 4 element circuits that should be there
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    circuit = [("J",), ("J",), ("C",), ("J",)]
    equiv_cirs = utils.get_equiv_circuits(TEMP_FILE, circuit, edges)
    assert equiv_cirs.shape[0] == 4
    assert all(equiv_cirs['equiv_circuit'].iloc[1:] ==
               equiv_cirs['unique_key'].iloc[0])

    # Test a few random circuits for 4
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    circuit = [("L",), ("J",), ("C",), ("J",)]
    assert red.isomorphic_circuit_in_set(circuit, edges,
                                         df4.circuit.values,
                                         df4.edges.values)
    circuit = [("J",), ("J",), ("C",), ("J",)]
    assert red.isomorphic_circuit_in_set(circuit, edges,
                                         df4.circuit.values,
                                         df4.edges.values)
    circuit = [("J",), ("C",), ("C",), ("J",)]
    assert red.isomorphic_circuit_in_set(circuit, edges,
                                         df4.circuit.values,
                                         df4.edges.values) is False
    circuit = [("L",), ("C",), ("L",), ("J",)]
    assert red.isomorphic_circuit_in_set(circuit, edges,
                                         df4.circuit.values,
                                         df4.edges.values)
    os.remove(TEMP_FILE)





def test_gen_hamiltonian():

    raise NotImplementedError

def test_categorize_hamiltonian():
    
    raise NotImplementedError




def df_equality_check(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Helper function that tests whether every entry of
    every row of two dataframes are equal

    Args:
        df1 (pd.DataFrame): dataframe 1 to compare
        df2 (pd.DataFrame): dataframe 2 to compare
    """
    assert df1.shape == df2.shape
    for i in range(df1.shape[0]):
        for k in df1.columns:
            v1 = df1.iloc[i][k]
            v2 = df2.iloc[i][k]
            if isinstance(v1, list):
                assert len(v1) == len(v2)
                assert all(x in v2 for x in v1)
                assert all(x in v1 for x in v2)
            else:
                assert v1 == v2


if __name__ == "__main__":
    # test_generate_graphs_node()
    test_generate_all_graphs()

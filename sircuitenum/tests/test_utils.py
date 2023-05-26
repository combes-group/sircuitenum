import pytest
import os
import itertools
import sqlite3
import time

import numpy as np
import networkx as nx
import pandas as pd
from pathlib import Path

from sircuitenum import enum, utils

import numpy.random
numpy.random.seed(7)  # seed random number generation for all calls to rand_ops


ALL_CONNECTED_3_RAW = [[c
                    for c in np.base_repr(i, 3).zfill(3)] for i in range(27)]
ALL_CONNECTED_3 = [[utils.COMBINATION_DICT[c] for c in x] for x in ALL_CONNECTED_3_RAW]
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

TEST_C = ["0","1","2"]
TEST_MAPPED_C = utils.circuit_to_components(TEST_C)
TEST_GI = 1
TEST_NN = 3
TEST_B = 7
TEST_CN = 16
TEST_ENTRY = utils.circuit_entry_dict(TEST_C, TEST_GI, TEST_NN,
                    TEST_CN, TEST_B)

MEMFNAME1 = 'file:cachedb?mode=memory&cache=shared'
MEMFNAME2 = 'file:cachedb2?mode=memory&cache=shared'


def test_get_basegraphs():
    # Most simple two node graph
    G = utils.get_basegraphs(2)[0]
    assert(x in G.edges for x in [(0, 1)])

    # test three node graphs
    G = utils.get_basegraphs(3)[0]
    assert(x in G.edges for x in [(0, 1), (1, 2)])

    G = utils.get_basegraphs(3)[1]
    assert(x in G.edges for x in [(0, 1), (1, 2), (0, 2)])

    # and a four node one too
    G = utils.get_basegraphs(4)[0]
    assert(x in G.edges for x in [(0, 1), (1, 2), (2, 3)])

    return


def test_graph_index_to_edges():
    # test done assuming get_basegraphs is working

    G = utils.get_basegraphs(2)[0]
    g = utils.graph_index_to_edges(0, 2)
    assert(x in G.edges for x in g)

    G = utils.get_basegraphs(3)[0]
    g = utils.graph_index_to_edges(0, 3)
    assert(x in G.edges for x in g)

    G = utils.get_basegraphs(3)[1]
    g = utils.graph_index_to_edges(1, 3)
    assert(x in G.edges for x in g)

    G = utils.get_basegraphs(4)[0]
    g = utils.graph_index_to_edges(0, 4)
    assert(x in G.edges for x in g)

    G = utils.get_basegraphs(5)[3]
    g = utils.graph_index_to_edges(3, 5)
    assert(x in G.edges for x in g)

    return


def test_circuit_to_components():
    components = utils.circuit_to_components("261")
    assert(components == [("L",), ("C", "J", "L"), ("J",)])

    components = utils.circuit_to_components("234")
    assert(components == [("L",), ("C", "J"), ("C", "L")])

    components = utils.circuit_to_components("2345")
    assert(components == [("L",), ("C", "J"), ("C", "L"), ("J", "L")])

    return


def test_count_elems():

    assert(utils.count_elems(['0', '2', '5', '1'], 7)
           == [1, 1, 1, 0, 0, 1, 0])

    assert(utils.count_elems(['4', '2', '2', '1'], 7)
           == [0, 1, 2, 0, 1, 0, 0])

    assert(utils.count_elems(['4', '4', '4'], 7) == [0, 0, 0, 0, 3, 0, 0])

    return

def test_count_elems_mapped():

    circuit = [("C",)]
    counts = utils.count_elems_mapped(circuit)

    assert(len(counts) == 3)
    assert(counts["C"] == 1)
    assert(counts["J"] == 0)
    assert(counts["L"] == 0)

    circuit = [("C",),("C","J"),("C","L"), ("C","J","L"), ("C","L"), ("C",)]
    counts = utils.count_elems_mapped(circuit)

    assert(len(counts) == 3)
    assert(counts["C"] == 6)
    assert(counts["J"] == 2)
    assert(counts["L"] == 3)

def test_get_num_nodes():
    assert(utils.get_num_nodes([(0, 1)]) == 2)

    assert(utils.get_num_nodes([(0, 1), (1, 2)]) == 3)

    assert(utils.get_num_nodes([(0, 1), (1, 2), (2, 3)]) == 4)

    assert(utils.get_num_nodes([(0,1),(0,2),(1,2),(1,3)]) == 4)
    assert(utils.get_num_nodes([(0,1),(45,2),(1,2),(1,3)]) == 46)

    return


def test_circuit_in_set():
    assert(utils.circuit_in_set(
        [("L",), ("J",), ("J",)], NON_ISOMORPHIC_3) == True)

    assert(utils.circuit_in_set(
        [("C",), ("J",), ("J",)], NON_ISOMORPHIC_3) == True)

    assert(utils.circuit_in_set(
        [("L",), ("L",), ("L",)], NON_ISOMORPHIC_3) == False)

    assert(utils.circuit_in_set(
        [("L",), ("C",), ("L",)], NON_ISOMORPHIC_3) == False)

    return


def test_convert_circuit_to_graph():
    G = nx.MultiGraph()
    G.add_edges_from([(0, 1, 0), (1, 2, 0), (1, 2, 1), (2, 3, 0), (2, 3, 1)])
    assert(utils.convert_circuit_to_graph(
        [["J"], ["C", "J"], ["C", "L"]], [(0, 1), (1, 2), (2, 3)]).edges == G.edges)
    G = nx.MultiGraph()
    G.add_edges_from([(0, 1, 0), (0, 1, 1), (1, 2, 0), (1, 4, 0), (2, 3, 0), (2, 3, 1)])
    assert(utils.convert_circuit_to_graph(
        [["J", "L"], ["C"], ["C", "J"], ["L",]], [(0, 1), (1, 2), (2, 3), (1, 4)]).edges == G.edges)
    G = nx.MultiGraph()
    G.add_edges_from([(0, 1, 0), (1, 2, 0), (1, 2, 1), (1, 2, 2)])
    assert(utils.convert_circuit_to_graph(
        [["C"], ["C", "J", "L"]], [(0, 1), (1, 2)]).edges == G.edges)
    return


def test_circuit_node_representation():
    assert(utils.circuit_node_representation(
        [["J"], ["C", "J"], ["C", "L"]], [(0, 1), (1, 2), (2, 3)]) == {'C': [0, 1, 2, 1], 'J': [1, 2, 1, 0], 'L': [0, 0, 1, 1]})
    assert(utils.circuit_node_representation(
        [["J", "L"], ["C"], ["C", "J"], ["L",]], [(0, 1), (1, 2), (2, 3), (1, 4)]) == {'C': [0, 1, 2, 1, 0], 'J': [1, 1, 1, 1, 0], 'L': [1, 2, 0, 0, 1]})
    assert(utils.circuit_node_representation(
        [["C"], ["C", "J", "L"]], [(0, 1), (1, 2)]) == {'C': [1, 2, 1], 'J': [0, 1, 1], 'L': [0, 1, 1]})  
    return


def test_circuit_entry_dict():
    circuit = ["0","1","2"]
    graph_index = 0
    n_nodes = 3
    base = 7
    circuit_num = 16
    entry = utils.circuit_entry_dict(circuit, graph_index, n_nodes,
                       circuit_num, base)
    assert(entry['circuit'] == "".join(circuit))
    assert(entry['graph_index'] == graph_index)
    assert(entry['unique_key'] == f"g0_c16")
    assert(entry['edge_counts'] == "1,1,1,0,0,0,0")
    assert(entry['n_nodes'] == n_nodes)
    assert(entry['base'] == base)

    return


def test_convert_loaded_df():
    df = pd.DataFrame([TEST_ENTRY])
    utils.convert_loaded_df(df, 3)
    assert(df['circuit'].iloc[0] == [('C',), ('J',), ('L',)])
    assert(df['circuit_encoding'].iloc[0] == '012')
    assert(df['edges'].iloc[0] ==  [(0, 1), (0, 2), (1, 2)])
    return


def test_write_df():

    if Path(MEMFNAME1).exists():
      os.remove(MEMFNAME1)
    
    df = write_test_df_in_mem()
    
    df2 = utils.get_circuit_data_batch(MEMFNAME1,3)

    assert(df.shape == df2.shape)

    write_test_df_in_mem(overwrite=False)

    
    df2 = utils.get_circuit_data_batch(MEMFNAME1,3)

    
    assert(2*df.shape[0] == df2.shape[0])
    assert(df.shape[1] == df2.shape[1])

    
    write_test_df_in_mem(overwrite=True)

    
    df2 = utils.get_circuit_data_batch(MEMFNAME1,3)

    
    assert(df.shape[0] == df2.shape[0])
    assert(df.shape[1] == df2.shape[1])

    
    os.remove(MEMFNAME1)

    return


def test_delete_circuit_data():

    df = write_test_df_in_mem(MEMFNAME1, overwrite=True)

    uid = 'g1_c21'
    utils.delete_circuit_data(MEMFNAME1, 3, uid)

    df2 = utils.get_circuit_data_batch(MEMFNAME1, 3)

    assert(df2.shape[0] == df.shape[0]-1)
    assert(uid not in df2.unique_key)

    df = write_test_df_in_mem(MEMFNAME1, overwrite=True)

    n_delete = 10
    uid = sorted([f'g1_c{str(i).zfill(2)}' for i in np.random.choice(np.arange(df.shape[0]),
                     size=n_delete, replace=False)])
    utils.delete_circuit_data(MEMFNAME1, 3, uid)

    df2 = utils.get_circuit_data_batch(MEMFNAME1, 3)

    assert(df2.shape[0] == df.shape[0]-n_delete)
    assert(all(u not in df2.unique_key for u in uid))

    os.remove(MEMFNAME1)

    return


def test_get_circuit_data():

   
    con, cur = write_test_circuit_in_mem(MEMFNAME1)

    circuit, edges = utils.get_circuit_data(MEMFNAME1,TEST_NN,TEST_ENTRY['unique_key'])

    assert(circuit==TEST_MAPPED_C)
    test_edges = [(0,1), (1,2), (2,0)]
    assert(len(edges) == len(test_edges))
    assert(all(utils.circuit_in_set(x, test_edges) or utils.circuit_in_set(x[::-1], test_edges) for x in edges))
    assert(all(utils.circuit_in_set(x, edges) or utils.circuit_in_set(x[::-1], edges) for x in test_edges))

    # Try loading and re-writing with batch function to make sure it doesn't break anything
    df = utils.get_circuit_data_batch(MEMFNAME1, 3)
    utils.write_df(MEMFNAME1, df,3,overwrite=True)
    
    circuit, edges = utils.get_circuit_data(MEMFNAME1,TEST_NN,TEST_ENTRY['unique_key'])

    assert(circuit==TEST_MAPPED_C)
    test_edges = [(0,1), (1,2), (2,0)]
    assert(len(edges) == len(test_edges))
    assert(all(utils.circuit_in_set(x, test_edges) or utils.circuit_in_set(x[::-1], test_edges) for x in edges))
    assert(all(utils.circuit_in_set(x, edges) or utils.circuit_in_set(x[::-1], edges) for x in test_edges))


    # Load elements of the full dataframe individually
    df = write_test_df_in_mem(MEMFNAME1, overwrite=True)
    for i, row in df.iterrows():
      circuit, edges = utils.get_circuit_data(MEMFNAME1,row['n_nodes'],row['unique_key'])
      test_edges = row['edges']
      test_circuit = row['circuit']
      assert(circuit==test_circuit)
      assert(len(edges) == len(test_edges))
      assert(all(utils.circuit_in_set(x, test_edges) or utils.circuit_in_set(x[::-1], test_edges) for x in edges))
      assert(all(utils.circuit_in_set(x, edges) or utils.circuit_in_set(x[::-1], edges) for x in test_edges))


    # Cleanup
    con.close()
    os.remove(MEMFNAME1)



    return


def test_get_circuit_data_batch():
  
    if Path(MEMFNAME1).exists():
        os.remove(MEMFNAME1)
      
    df = write_test_df_in_mem()
    df2 = utils.get_circuit_data_batch(MEMFNAME1,3)

      


    assert(df.shape == df2.shape)
    for i in range(df2.shape[0]):
      for k in df2.columns:
        v1 = df.iloc[i][k]
        v2 = df2.iloc[i][k]
        if isinstance(v1, list):
          assert(len(v1) == len(v2))
          assert(all(x in v2 for x in v1))
          assert(all(x in v1 for x in v2))
        else:
          assert(v1==v2)

      
    os.remove(MEMFNAME1)

    return


def test_write_circuit():
    
    con, cur = write_test_circuit_in_mem(MEMFNAME1)
    df = pd.read_sql_query("select * from CIRCUITS_3_NODES", con = con)
  
    for k in df.columns:
      assert(df.iloc[0][k] == TEST_ENTRY[k])

    # Cleanup
    con.close()
    os.remove(MEMFNAME1)

    # Write multiple rows
    con, cur = write_test_circuit_in_mem(MEMFNAME1, reps=10)
    df = pd.read_sql_query("select * from CIRCUITS_3_NODES", con = con)
    
    for i in range(df.shape[0]):
      for k in df.columns:
        assert(df.iloc[i][k] == TEST_ENTRY[k])

    # Cleanup
    con.close()
    os.remove(MEMFNAME1)

    return

def write_test_circuit_in_mem(fname=MEMFNAME1, reps = 1):

    if Path(fname).exists():
      os.remove(fname)
    
    con = sqlite3.connect(fname)
    cur  = con.cursor()

    
    table_name = "CIRCUITS_3_NODES"
    cur.execute(
           "CREATE TABLE {table} (circuit, graph_index int, edge_counts, unique_key, n_nodes int, base int)".format(table=table_name))
    
    for i in range(reps):
      utils.write_circuit(cur, TEST_ENTRY, True)
    
    return con, cur

def write_test_df_in_mem(fname=MEMFNAME1, overwrite=False):
    # Make test dataframe
    df = pd.DataFrame({"circuit":ALL_CONNECTED_3})
    df['circuit_encoding'] = ["".join(x) for x in ALL_CONNECTED_3_RAW]
    df['graph_index'] = 1
    edges =  [[(0,1), (1,2), (0,2)]]*df.shape[0]
    df['edges'] = edges
    df['n_nodes'] = 3
    df['base'] = 7
    df['unique_key'] = [f"g1_c{str(i).zfill(2)}" for i in range(df.shape[0])]

    utils.write_df(MEMFNAME1, df, 3, overwrite=overwrite)

    return df

if __name__ == "__main__":
    test_circuit_node_representation()

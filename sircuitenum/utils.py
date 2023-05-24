import sqlite3

from typing import Union
import numpy as np
from pathlib import Path
import networkx as nx
import pandas as pd


COMBINATION_LIST = """
# Combination abbreviations(Base = 3):
# 0 : 0 = Capacitor
# 1 : 1 = Josephson Junction
# 2 : 2 = Inductor
# Extended(Base = 7):
# 3 : 3 = Capacitor | Josephson Junction
# 4 : 4 = Capacitor | Inductor
# 5 : 5 = Inductor  | Josephson Junction
# 6 : 6 = Capacitor | Inductor  | Josephson Junction
# Extended Classical(Base = 15):            //  NOT IMPLEMENTED
# 7 : 7 = Resistor
# 8 : 8 = Capacitor | R = Resistor
# 9 : 9 = Inductor  | R = Resistor
# 10 : A = Josephson Junction | R = Resistor
# 11 : B = Capacitor | Inductor | R = Resistor
# 12 : C = Capacitor | Josephson Junction | R = Resistor
# 13 : D = Inductor  | Josephson Junction | R = Resistor
# 14 : E = Capacitor | Inductor  | Josephson Junction | R = Resistor
"""


COMBINATION_DICT = {
    '0': ('C',),
    '1': ('J',),
    '2': ('L',),
    '3': ('C', 'J'),
    '4': ('C', 'L'),
    '5': ('J', 'L'),
    '6': ('C', 'J', 'L'),
}


COMBINATION_TO_CHAR = {}
for c in COMBINATION_DICT:
    COMBINATION_TO_CHAR[COMBINATION_DICT[c]] = c


EDGE_COLOR_DICT = {
    'C': 0,
    'J': 1,
    'L': 2,
    'CJ': 3,
    'CL': 4,
    'JL': 5,
    'CJL': 6,
}


ELEM_DICT = {
    'C': {'default_unit': 'GHz', 'default_value': 0.2},
    'L': {'default_unit': 'GHz', 'default_value': 0.5},
    'J': {'default_unit': 'GHz', 'default_value': 5.0}
}

DOWNLOAD_PATH = Path(__file__).parent.parent


def graph_index_to_edges(graph_index: int, n_nodes: int, all_graphs: list = []):
    """
    Returns a list of edges [(from, to), (from, to)] 
    for the specified base graph

    Args:
        graph_index (int): base graph number
        n_nodes (int): number of nodes in the base graph
        all_graphs (list of nx graphs): optionally preload the list to avoid loading it in every call

    Returns:
        list of len 2 tuples where each tuple represents 
        the starting and ending nodes for an edge in the graph
        [(from, to), (from, to),...]
    """
    if len(all_graphs) == 0:
        all_graphs = get_basegraphs(n_nodes)
    edges = all_graphs[graph_index].edges
    return list(edges)


def circuit_to_components(circuit_raw: str, elem_mapping: dict = COMBINATION_DICT):
    """Maps the raw circuit encoding to a list of lists of elements
    e.g. 261 -> [["J"], ["C", "J", "L"], ["L"]]

    Args:
        circuit_raw (str): string that represents base n number where each character  
                                maps to a combination of circuit componenets
        elem_mapping (dict, optional): mapping between circuit components and characters
                                        . Defaults to COMBINATION_DICT.

    Returns:
        list of lists that represent the circuit elements along an edge:
        e.g. [["J"], ["C", "J", "L"], ["L"]]
    """
    return [elem_mapping[e] for e in circuit_raw]


def convert_loaded_df(df: pd.DataFrame, n_nodes: int, elem_mapping: dict = COMBINATION_DICT):
    """Load the edges/circuit element labels for a freshly-loaded df


    Args:
        df (pd.Dataframe): dataframe of circuits
        n_nodes (int): number of nodes in the circuits

    Returns:
        Nothing, modifies the dataframe
    """
    # Load basegraph to get the edges
    all_graphs = get_basegraphs(n_nodes)
    df['edges'] = [graph_index_to_edges(
        int(i), n_nodes, all_graphs) for i in df.graph_index.values]
    df['circuit_encoding'] = df.circuit.values.copy()
    df['circuit'] = [circuit_to_components(
        c, elem_mapping=elem_mapping) for c in df.circuit.values]


def get_basegraphs(n_nodes: int):
    """Loads the base graphs for a specific number of nodes 

    Args:
        n_nodes (int): number of nodes in the graph
    """
    f = Path(DOWNLOAD_PATH, 'sircuitenum', 'graphs', f"graph{n_nodes}c.g6")
    all_graphs = nx.read_graph6(f)

    # Fix two vertex case so it always returns a list
    if n_nodes == 2:
        all_graphs = [all_graphs]

    return all_graphs


def count_elems(circuit: list, base: int):
    """
    Counts the total number of each element
    label in the circuit

    Args:
        circuit (list of str): a list of element labels for the desired circuit
                                (i.e., ['0','2','5','1'])
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)

    Returns:
        list of length base, where each entry is the number of that element present
    """
    counts = [0]*base
    for part in circuit:
        counts[int(part)] += 1
    return counts


def circuit_entry_dict(circuit: list, graph_index: int, n_nodes: int,
                       circuit_num: int, base: int):
    """Creates a dictionary that can serve as a row of a dataframe of
    circuits, or can be used to write an individual row to a database

    Args:
        circuit (list of str): a list of element labels for the desired circuit
                                (i.e., ['0','2','5','1'])
        graph index (int): the index of the graph for the written circuit
                                within the file for the number of nodes
        n_nodes (int): Number of nodes in circuit
        circuit_num (int): n-th circuit generated from the basegraph, to make
                           a unique key.
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)

    Returns:
        dictionary with circuit, graph_index, edge_counts, n_nodes
    """
    c_dict = {}
    c_dict['circuit'] = "".join(circuit)
    c_dict['graph_index'] = graph_index
    c_dict['unique_key'] = f"g{graph_index}_c{circuit_num}"

    counts = [str(c) for c in count_elems(circuit, base)]
    c_dict['edge_counts'] = ",".join(counts)
    c_dict['n_nodes'] = n_nodes
    c_dict['base'] = base
    return c_dict


def convert_circuit_to_graph(circuit: list, edges: list):
    """
    Encodes a circuit as a simple, undirected nx graph

    Args:
        circuit (list of str): a list of elements for the desired circuit (i.e., [[['C'],['C'],['L'],['C','J']])
        edges (list of tuples of ints): a list of edge connections for the desired circuit (i.e., [(0,1),(1,2),(2,3),(3,0)])
    """

    circuit_graph = nx.MultiGraph()
    for i in range(len(circuit)):
        edge = edges[i]
        elements = circuit[i]
        for elem in elements:
            circuit_graph.add_edge(edge[0], edge[1], element=elem, unit=ELEM_DICT[elem]
                                   ['default_unit'], value=ELEM_DICT[elem]['default_value'])
    return circuit_graph


def circuit_node_representation(circuit, edges):
    """
    Converts a circuit into its "node representation"
    that shows how many of each component are connected
    to each node.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        dictionary that maps component label to how many are
        connected to each node: e.g. {'J': [0,0,1,2,0]}
    """

    # Extract number of nodes from edge list
    n_nodes = get_num_nodes(edges)

    # Dictionary that maps component to a list that says
    # how many of that component connect to a given node
    # i.e. 'J': [0,0,1,2,0]
    component_counts = {}
    for component in ELEM_DICT:
        component_counts[component] = [0] * n_nodes

    # Go through each component code in the circuit
    # and loop through the circuit element that it entails
    # and add counts to the appropriate nodes
    for component_combo, edge in zip(circuit, edges):
        for component in component_combo:
            component_counts[component][edge[0]] += 1
            component_counts[component][edge[1]] += 1

    return component_counts


def get_num_nodes(edges: list):
    """Simple function that returns the number of nodes in the graph, given the edge list"""
    return np.max(np.array(edges)) + 1


def circuit_in_set(circuit: list, c_set: list):
    """Helper function to see if a particular circuit
    (list/tuple of tuples) is in a set of circuits
    (list of list/tuple of tuples)

    Args:
        cir (list): a list of element labels for the desired circuit
                        e.g. [("J"),("L", "J"), ("C")]
        c_set (list of lists): list of cir-like elements

    Returns:
        True if cir is present in c_set, False if it isn't
    """
    for c2 in c_set:
        if len(circuit) == len(c2):
            if all(circuit[i] == c2[i] for i in range(len(circuit))):
                return True
    return False


################################################################################
# I/O Functions for Circuit Database
################################################################################


def write_df(file: str, df: pd.DataFrame, n_nodes: int, overwrite=False):
    """
    Writes the given dataframe to a database file. Appends it if the 
    table is already there.

    Args:
        df (pd.Dataframe): dataframe that represents the circuit entries
        n_nodes (int, optional): number of nodes in the circuit. Defaults to 7.
        file (str, optional): database file to write to. Defaults to "circuits.db".
        overwrite (bool, optional): overwrite the table or append to it if it exists

    Returns:
        None, writes the dataframe to the database

    """

    to_write = df.copy()

    # drop list columns to save circuit back into saving format
    del to_write['edges']

    # Rename circuit encoding column
    to_write['circuit'] = to_write['circuit_encoding']
    del to_write['circuit_encoding']
    if_exists = "append"
    if overwrite:
        if_exists = "replace"
    
    with sqlite3.connect(file) as con:
        to_write.to_sql(f"CIRCUITS_{n_nodes}_NODES",
                        con, if_exists=if_exists, index=False)


def delete_circuit_data(file: str, n_nodes: int, indices: Union[list,str]):
    """
    Deletes the specified graphs (num nodes/indices) from the database file

    Args:
        file (str, optional): path to the databse file. 
        n_nodes (int): number of nodes for the graph
        indices (list or str): unique key (or list of keys) of the graph(s) to be deleted

    Returns:
        None, just modifies the database
    """

    # Convert individual entry for batch use
    if isinstance(indices, str):
        indices = [indices]

    connection_obj = sqlite3.connect(file)
    cursor_obj = connection_obj.cursor()
    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    for index in indices:
        cursor_obj.execute('''DELETE FROM {table} WHERE unique_key = '{index}';
                       '''.format(table=table_name, index=str(index)))
    connection_obj.commit()
    connection_obj.close()

    return


def get_circuit_data(file: str, n_nodes: int, index: str, elem_mapping: dict = COMBINATION_DICT):
    """ gets circuit data from database

    Args:
        n_nodes (int): The number of nodes in the circuit
        index (str): Unique Idenitifier of the circuit within the table for the number of nodes
        file (str): path to the database to get circuit from
        elem_mapping (dict, optional): mapping from character to list of circuit elements

    Returns:
        circuit (list) : a list of element labels for the desired circuit (i.e., ['0','2','5','1'])
        edges (list of tuples of ints): a list of edge connections for the desired circuit (i.e., [(0,1),(1,2),(2,3),(3,0)])
    """

    # Fetch entry from database
    connection_obj = sqlite3.connect(file)
    cursor_obj = connection_obj.cursor()
    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    query_str = f"SELECT * FROM {table_name} WHERE unique_key = '{index}'"
    cursor_obj.execute(query_str)
    output = cursor_obj.fetchone()
    connection_obj.commit()
    connection_obj.close()

    # Map the edges and circuit component info
    edges = graph_index_to_edges(int(output[1]), n_nodes)
    circuit = circuit_to_components(output[0], elem_mapping=elem_mapping)


    return circuit, edges


def get_circuit_data_batch(file: str, n_nodes: int, elem_mapping: dict = COMBINATION_DICT, filter_str: str = ''):
    """
    Returns all the circuits present in the database for the specified number of nodes,
    and any other filter statements given.

    Args:
        n_nodes (int): number of nodes in the circuit
        file (str, optional): sqlite file to look in. Defaults to "circuits.db".
        elem_mapping (dict, optional): mapping from character to list of circuit elements
        filters (list, optional): list of SQL filter statements (i.e. WHERE circuit_index = 100) Defaults to [].

    Returns:
        pandas dataframe containing each circuit as a row
    """

    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    connection_obj = sqlite3.connect(file)
    query = "SELECT * FROM {table} {filter_str}".format(
        table=table_name, filter_str=filter_str)
    df = pd.read_sql_query(query, connection_obj)
    connection_obj.commit()
    connection_obj.close()

    convert_loaded_df(df, n_nodes, elem_mapping)

    # Make a useful index if it's there
    if 'unique_key' in df.columns:
        df.index = df['unique_key']

    return df


def write_circuit(cursor_obj, c_dict: dict, to_commit: bool = False):
    """Appends an individual circuit to a database

    Args:
        cursor_obj: sqllite cursor object pointing to the desired database
        c_dict: dictionary that represents a circuit entry
        to_commit: commit the database (i.e., save changes)
    """
    cursor_obj.execute("INSERT INTO {table} VALUES ('{circuit}',"
                       "'{graph_index}', '{edge_counts}', '{unique_key}', '{n_nodes}', '{base}')".format(
                           table=f"CIRCUITS_{c_dict['n_nodes']}_NODES",
                           circuit=c_dict['circuit'], 
                           graph_index=c_dict['graph_index'],
                           edge_counts=c_dict['edge_counts'],
                           unique_key=c_dict['unique_key'],
                           n_nodes=c_dict['n_nodes'],
                           base=c_dict['base']
                        )
                       )
    if to_commit:
        cursor_obj.connection.commit()


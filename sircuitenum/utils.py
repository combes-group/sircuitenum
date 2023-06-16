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
    'L': {'default_unit': 'GHz', 'default_value': 1.0},
    'J': {'default_unit': 'GHz', 'default_value': 5.0},
    'CJ': {'default_unit': 'GHz', 'default_value': 20.0}
    # 'CJ': {'default_unit': 'GHz', 'default_value': 0.0}
}

DOWNLOAD_PATH = Path(__file__).parent.parent

# Dictionary to store loaded basegraphs, so
# you don't have to load them from storage
# every time
LOADED_BASEGRAPHS = {}


def graph_index_to_edges(graph_index: int, n_nodes: int):
    """
    Returns a list of edges [(from, to), (from, to)]
    for the specified base graph

    Args:
        graph_index (int): base graph number
        n_nodes (int): number of nodes in the base graph


    Returns:
        list of len 2 tuples where each tuple represents
        the starting and ending nodes for an edge in the graph
        [(from, to), (from, to),...]
    """
    return list(get_basegraphs(n_nodes)[graph_index].edges)


def edges_to_graph_index(edges: list):
    """
    Matches a set of edges to a basegraph that's isomorphic to it

    Args:
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
    """
    # Graph object to use in comparison
    G1 = nx.Graph()
    G1.add_edges_from(edges)

    n_nodes = get_num_nodes(edges)
    n_edges = len(edges)
    possible_graphs = get_basegraphs(n_nodes)
    for i, G2 in enumerate(possible_graphs):
        if G2.number_of_edges() == n_edges:
            if nx.is_isomorphic(G1, G2):
                return i

    raise ValueError("Error: No Isomorphic Graph Found")


def encoding_to_components(circuit_raw: str,
                           elem_mapping: dict = COMBINATION_DICT):
    """Maps the raw circuit encoding to a list of lists of elements
    e.g. 261 -> [["J"], ["C", "J", "L"], ["L"]]

    Args:
        circuit_raw (str): string that represents base n number
                           where each character maps to a combination
                           of circuit componenets
        elem_mapping (dict, optional): mapping from characters to
                                       circuit components.
                                       Defaults to COMBINATION_TO_CHAR.

    Returns:
        list of lists that represent the circuit elements along an edge:
        e.g. [["J"], ["C", "J", "L"], ["L"]]
    """
    return [elem_mapping[str(e)] for e in circuit_raw]


def components_to_encoding(circuit: list,
                           elem_mapping: dict = COMBINATION_TO_CHAR):
    """Maps the list of circuit components to the database encoding
    e.g. [["J"], ["C", "J", "L"], ["L"]] -> 261

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        elem_mapping (dict, optional): mapping from circuit
                                       components to characters.
                                       Defaults to COMBINATION_TO_CHAR.

    Returns:
        list of lists that represent the circuit elements along an edge:
        e.g. [["J"], ["C", "J", "L"], ["L"]]
    """
    return "".join([elem_mapping[tuple(comps)] for comps in circuit])


def convert_loaded_df(df: pd.DataFrame, n_nodes: int,
                      elem_mapping: dict = COMBINATION_DICT):
    """Load the edges/circuit element labels for a freshly-loaded df


    Args:
        df (pd.Dataframe): dataframe of circuits
        n_nodes (int): number of nodes in the circuits

    Returns:
        Nothing, modifies the dataframe
    """
    # Get the edges
    df['edges'] = [graph_index_to_edges(int(i), n_nodes)
                   for i in df.graph_index.values]
    df['circuit_encoding'] = df.circuit.values.copy()
    df['circuit'] = [encoding_to_components(c, elem_mapping=elem_mapping)
                     for c in df.circuit.values]


def get_basegraphs(n_nodes: int):
    """
    Loads the base graphs for a specific number of nodes

    Args:
        n_nodes (int): number of nodes in the graph
    """
    # Load it if it hasn't been loaded
    if str(n_nodes) not in LOADED_BASEGRAPHS:
        f = Path(DOWNLOAD_PATH, 'sircuitenum', 'graphs', f"graph{n_nodes}c.g6")
        all_graphs = nx.read_graph6(f)
        # Fix two vertex case so it always returns a list
        if n_nodes == 2:
            all_graphs = [all_graphs]
        LOADED_BASEGRAPHS[str(n_nodes)] = all_graphs

    # Return if it has already been loaded
    return LOADED_BASEGRAPHS[str(n_nodes)]


def count_elems(circuit: list, base: int):
    """
    Counts the total number of each element
    label in the circuit, for use with the unmapped
    integer labels

    Args:
        circuit (list of str): a list of element labels for the desired circuit
                                (i.e., ['0','2','5','1'])
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)

    Returns:
        list of length base, where each entry is the number of that
        element present
    """
    counts = [0]*base
    for part in circuit:
        counts[int(part)] += 1
    return counts


def count_elems_mapped(circuit: list, **kwargs):
    """
    Counts the total number of each mapped circuit
    element in the circuit

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        possible_elems (list): list of possible elements, default
                               is the unique set in COMBINATION_DICT

    Returns:
        list of length base, where each entry is the number
        of that element present
    """
    default_elems = np.unique(np.concatenate(list(COMBINATION_DICT.values())))
    possible_elems = kwargs.get("possible_elems", default_elems)
    counts = {}
    for elem in possible_elems:
        counts[elem] = 0

    for elems in circuit:
        for elem in elems:
            counts[elem] += 1

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
    c_dict['unique_key'] = f"n{n_nodes}_g{graph_index}_c{circuit_num}"
    c_dict['in_non_iso_set'] = 0
    c_dict['no_series'] = 0
    c_dict['has_jj'] = 0
    c_dict['equiv_circuit'] = ""

    counts = [str(c) for c in count_elems(circuit, base)]
    c_dict['edge_counts'] = ",".join(counts)
    c_dict['n_nodes'] = n_nodes
    c_dict['base'] = base
    return c_dict


def gen_param_dict(circuit, edges, vals=ELEM_DICT):
    """
    Generates a dictionary of parameters for use with
    the circuit conversion functions. Sets all components
    to the same values.

    Maps (edge, elem) to (value, unit):

    i.e., ((0,1), "J") -> (5.0, "GHz")

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        vals (dict of dicts): Dictionary with entries for each circuit
                                element. Shows default values
    """
    param_dict = {}
    for elems, edge in zip(circuit, edges):
        for elem in elems:
            key = (edge, elem)
            param_dict[key] = (vals[elem]['default_value'],
                               vals[elem]['default_unit'])

            # Junction capacitance
            key = (edge, "CJ")
            if elem == "J" and key in vals:
                param_dict[key] = (vals["CJ"]['default_value'],
                                   vals["CJ"]['default_unit'])

    return param_dict


def convert_circuit_to_graph(circuit: list, edges: list, **kwargs):
    """
    Encodes a circuit as a simple, undirected nx graph with labels
    on the edges for the circuit element, unit, and value

    Args:
        circuit (list of str): a list of elements for the desired circuit
                               (i.e., [[['C'],['C'],['L'],['C','J']])
        edges (list of tuples of ints): a list of edge connections for the
                                        desired circuit
                                        (i.e., [(0,1),(1,2),(2,3),(3,0)])
        params (dict): dictionary with entries C, L, J, CJ,
                    which represent the paramaters for the circuit elements.
                    Additionally entries of C_units, L_units, J_units,
                    and CJ_units. Inputting nothing uses the default parameter
                    values/units from utils.ELEM_DICT.

    """

    params = kwargs.get("params", gen_param_dict(circuit, edges, ELEM_DICT))

    circuit_graph = nx.MultiGraph()
    for elems, edge in zip(circuit, edges):
        for elem in elems:
            value, unit = params[(edge, elem)]
            circuit_graph.add_edge(edge[0], edge[1], element=elem,
                                   unit=unit,
                                   value=value)
            # Junction capacitance
            if elem == "J":
                if (edge, "CJ") in params:
                    value, unit = params[(edge, "CJ")]
                    if value > 0:
                        circuit_graph.add_edge(edge[0], edge[1],
                                               element="CJ",
                                               unit=unit,
                                               value=value)
    return circuit_graph


def circuit_node_representation(circuit: list, edges: list):
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
    for comp in np.unique(np.concatenate(list(COMBINATION_DICT.values()))):
        component_counts[comp] = [0] * n_nodes

    # Go through each component code in the circuit
    # and loop through the circuit element that it entails
    # and add counts to the appropriate nodes
    for components, edge in zip(circuit, edges):
        for comp in components:
            component_counts[comp][edge[0]] += 1
            component_counts[comp][edge[1]] += 1

    return component_counts


def get_num_nodes(edges: list):
    """
    Simple function that returns the number of unique nodes
    in edges
    """
    return np.unique(np.concatenate(edges)).size


def renumber_nodes(edges: list):
    """
    Renumbers nodes so that there is a continuous range
    of integers between 0 and the max number

    Args:
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        new version of edges with nodes relabeled so that the max
        number present is equal to the number of nodes + 1
    """
    new_edges = edges[:]
    nodes = np.unique(np.concatenate(new_edges))
    if nodes[-1] != nodes.shape[0]-1:
        relabel_map = {}
        for i in range(len(nodes)):
            relabel_map[nodes[i]] = i
        for i in range(len(new_edges)):
            edge = new_edges[i]
            new_edges[i] = tuple([relabel_map[x] for x in edge])

    return new_edges


def combine_redundant_edges(circuit: list, edges: list):
    """
    Combines edges that are between the same two nodes

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        New version of circuit/edges with any redundant edges combined.
        If multiple edges have the same element, then a single

    """
    edge_dict = {}
    for i in range(len(edges)):
        edge = tuple(sorted(edges[i]))
        comps = circuit[i]
        if edge in edge_dict:
            edge_dict[edge] = edge_dict[edge] + comps
        else:
            edge_dict[edge] = comps
    new_edges = list(edge_dict.keys())
    new_circuit = [tuple(sorted(set(edge_dict[x]))) for x in new_edges]

    return new_circuit, new_edges


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


###############################################################################
# I/O Functions for Circuit Database
###############################################################################


def write_df(file: str, df: pd.DataFrame, n_nodes: int, overwrite=False):
    """
    Writes the given dataframe to a database file. Appends it if the
    table is already there.

    Args:
        file (str, optional): Database file to write to.
        df (pd.Dataframe): dataframe that represents the circuit entries
        n_nodes (int, optional): number of nodes in the circuit. Defaults to 7.
        overwrite (bool, optional): overwrite the table or
                                    append to it if it exists

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


def update_db_from_df(file: str, df: pd.DataFrame):
    """
    Updates the no_series, has_jj, in_non_iso_set, and
    equiv_circuit columns for every entry in df

    Args:
        file (str, optional): Database file to write to.
        df (pd.Dataframe): dataframe that represents the circuit entries

    Returns:
        None, writes the dataframe info to the database

    """

    to_update = ["no_series", "has_jj", "in_non_iso_set", "equiv_circuit"]
    n_fields = len(to_update)

    with sqlite3.connect(file) as con:
        cur = con.cursor()
        for _, row in df.iterrows():
            n_nodes = row['n_nodes']
            sql_str = f"UPDATE CIRCUITS_{n_nodes}_NODES SET "
            for i, col in enumerate(to_update):
                val = row[col]
                if col != "equiv_circuit":
                    val = int(val)
                if i < n_fields - 1:
                    sql_str += f"{col} = '{val}', "
                else:
                    sql_str += f"{col} = '{val}' "
                    sql_str += f"WHERE unique_key = '{row['unique_key']}';"
            cur.execute(sql_str)


def delete_circuit_data(file: str, n_nodes: int, indices: Union[list, str]):
    """
    Deletes the specified graphs (num nodes/indices) from the database file

    Args:
        file (str, optional): path to the databse file.
        n_nodes (int): number of nodes for the graph
        indices (list or str): unique key (or list of keys) of the graph(s)
                                to be deleted

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


def get_circuit_data(file: str, unique_key: str,
                     elem_mapping: dict = COMBINATION_DICT):
    """ gets circuit data from database

    Args:
        n_nodes (int): The number of nodes in the circuit
        unique_key (str): Unique Idenitifier of the circuit
        file (str): path to the database to get circuit from
        elem_mapping (dict, optional): mapping from character to list of
                                       circuit elements

    Returns:
        circuit (list) : a list of element labels for the desired circuit
                         (i.e., ['0','2','5','1'])
        edges (list of tuples of ints): a list of edge connections for the
                                        desired circuit
                                        (i.e., [(0,1),(1,2),(2,3),(3,0)])
    """
    # Parse uid to get number of nodes
    n_nodes = unique_key[unique_key.find("n") + 1:unique_key.find("_")]

    # Fetch entry from database
    connection_obj = sqlite3.connect(file, uri=True)
    cursor_obj = connection_obj.cursor()
    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    query_str = f"SELECT * FROM {table_name} WHERE unique_key = '{unique_key}'"
    cursor_obj.execute(query_str)
    output = cursor_obj.fetchone()
    connection_obj.commit()
    connection_obj.close()

    # Map the edges and circuit component info
    edges = graph_index_to_edges(int(output[1]), n_nodes)
    circuit = encoding_to_components(output[0], elem_mapping=elem_mapping)

    return circuit, edges


def get_circuit_data_batch(db_file: str, n_nodes: int,
                           elem_mapping: dict = COMBINATION_DICT,
                           filter_str: str = ''):
    """
    Returns all the circuits present in the database for the specified
    number of nodes, and any other filter statements given.

    Args:
        db_file (str, optional): sqlite db_file to look in.
                                Defaults to "circuits.db"
        n_nodes (int): number of nodes in the circuit
        elem_mapping (dict, optional): mapping from character to
                                       list of circuit elements
        filters (str, optional): SQL filter statement
                                (i.e. WHERE circuit_index = 100).

    Returns:
        pandas dataframe containing each circuit as a row
    """

    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    connection_obj = sqlite3.connect(db_file)
    query = "SELECT * FROM {table} {filter_str}".format(
        table=table_name, filter_str=filter_str)
    df = pd.read_sql_query(query, connection_obj)
    connection_obj.commit()
    connection_obj.close()

    convert_loaded_df(df, n_nodes, elem_mapping)

    # Make a useful index if it's there
    if 'unique_key' in df.columns:
        df.index = df['unique_key']

    # Convert int to bool columns
    int_to_bool = ["no_series", "has_jj", "in_non_iso_set"]
    for col in int_to_bool:
        df[col] = df[col].astype(bool)

    return df


def get_unique_qubits(db_file: str, n_nodes: str):
    """
    Loads all entries corresponding to unique qubits
    from the specified file for the specified number
    of nodes

    Args:
        db_file (str): sqlite db_file to look in.
                                Defaults to "circuits.db"
        n_nodes (int): number of nodes in the circuit

    Returns:
        pd.DataFrame: set of unique qubit circuits
    """
    filter_str = "WHERE in_non_iso_set = 1 AND "
    filter_str += "has_jj = 1 AND no_series = 1"
    return get_circuit_data_batch(db_file, n_nodes, filter_str=filter_str)


def get_equiv_circuits_uid(db_file: str, unique_key: str):
    """
    Finds all circuits in the database with either the
    given unique key, or with it as the equiv circuit

    Args:
        db_file (str): sqlite db_file to look in.
                                Defaults to "circuits.db"
        unique_key (str): unique identifier for the circuit
    """
    tables = list_all_tables(db_file)
    entries = []
    filt_str = f"WHERE equiv_circuit LIKE '{unique_key}'\
                 OR unique_key LIKE '{unique_key}'"
    for tbl in tables:
        start = tbl[0].find("_") + 1
        end = start + 1
        n_nodes = int(tbl[0][start:end])
        entries.append(get_circuit_data_batch(db_file, n_nodes,
                                              filter_str=filt_str))

    return pd.concat(entries).sort_values(by="equiv_circuit")


def get_equiv_circuits(db_file: str, circuit: list, edges: list):
    """
    Finds all circuits equivalent to the one provided
    that are present in the database.
    Returns None if none are found.

    Args:
        db_file (str): sqlite db_file to look in.
                                Defaults to "circuits.db"
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
    """

    entry = find_circuit_in_db(db_file, circuit, edges)
    if entry.shape[0] > 1:
        raise ValueError("Getting too many circuits")
    elif entry.empty:
        return None
    else:
        entry = entry.iloc[0]

    if entry["in_non_iso_set"]:
        uid = entry["unique_key"]
    elif entry["equiv_circuit"] != "not found":
        uid = entry["equiv_circuit"]
    else:
        return [entry]

    return get_equiv_circuits_uid(db_file, uid)


def find_circuit_in_db(db_file: str, circuit: list, edges: list):
    """
    Finds the database entry for a given circuit/edges combination

    Args:
        db_file (str): sqlite db_file to look in.
                                Defaults to "circuits.db"
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
    """

    encoding = components_to_encoding(circuit)
    n_nodes = get_num_nodes(edges)
    graph_index = edges_to_graph_index(edges)
    filters = f"WHERE circuit LIKE '{encoding}' AND\
                graph_index = '{graph_index}'"
    return get_circuit_data_batch(db_file, n_nodes, filter_str=filters)


def write_circuit(cursor_obj, c_dict: dict, to_commit: bool = False):
    """Appends an individual circuit to a database

    Args:
        cursor_obj: sqllite cursor object pointing to the desired database
        c_dict: dictionary that represents a circuit entry
        to_commit: commit the database (i.e., save changes)
    """
    table = f"CIRCUITS_{c_dict['n_nodes']}_NODES"
    sql_str = f"INSERT INTO {table} VALUES ("
    sql_fields = ["circuit", "graph_index", "edge_counts",
                  "unique_key", "n_nodes", "base",
                  "no_series", "has_jj", "in_non_iso_set",
                  "equiv_circuit"]
    n_fields = len(sql_fields)
    for i, field in enumerate(sql_fields):
        if i < n_fields - 1:
            sql_str += f"'{c_dict[field]}', "
        else:
            sql_str += f"'{c_dict[field]}')"
    cursor_obj.execute(sql_str)

    if to_commit:
        cursor_obj.connection.commit()


def list_all_tables(db_file: str):
    """
    Lists all the tables in the database file

    Args:
        db_file (str): file to examine
    """
    with sqlite3.connect(db_file, uri=True) as connection_obj:
        cursor_obj = connection_obj.cursor()
        tables = cursor_obj.execute("SELECT name FROM sqlite_master\
                                WHERE type='table'").fetchall()
    return tables

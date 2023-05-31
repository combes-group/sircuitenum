#!/usr/bin/env python
"edge_enumerate.py: Contains functions to enumerated edges of quantum circuits"
__author__ = "Mohit Bhat, Eli Weissler"
__version__ = "0.1.0"
__status__ = "Development"

# -------------------------------------------------------------------
# Import Statements
# -------------------------------------------------------------------
import sqlite3
import itertools

import networkx as nx
import numpy as np
import pandas as pd

from tqdm import tqdm

from sircuitenum import utils
from sircuitenum import reduction as red


# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------

def num_possible_circuits(base: int, n_nodes: int, quiet: bool = True):
    """ Calculates the number of possible circuits for a given number
    # of edges and vertices, may overestimate.

    Args:
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
        n_nodes (int): the number of vertices in a graph.
        quiet (bool): print the number of circuits or not

    Returns:
        n_circuits (int): a list of networkx graphs
    """
    all_graphs = utils.get_basegraphs(n_nodes)
    n_circuits = 0
    for graph in all_graphs:
        n_circuits += base**len(graph.edges)
    if not quiet:
        print("With " + str(base) + " elements and " + str(n_nodes) +
              " nodes there are " + str(n_circuits) + " possible circuits")
    return n_circuits


def total_num_possible(max_base: int, n_nodes: int, quiet: bool = True):
    """ Calculates the number of possible circuits for a given number
        of possible edges, assuming a specific number of nodes.

    Args:
        max_base (int): maximum number of possible edges to loop until
        n_nodes (int): the number of vertices in a graph.
        quiet (bool): whether to print the number possible or not

    Returns:
        counts (dict): dictionary that contains the number of possible circuits
                        with each number of edges.
    """
    total = 0
    counts = {}
    # Iterate over all possible number of edges
    for i in range(max_base+1):
        counts[str(i)] = num_possible_circuits(i, n_nodes, quiet=quiet)
        total += counts[str(i)]
    if not quiet:
        print("There are: ", total, " Elements")
    counts["total"] = total
    return counts


def generate_for_specific_graph(base: int, graph: nx.Graph,
                                graph_index: int,
                                cursor_obj=None,
                                return_vals: bool = False):
    """Generates all circuits derived from a given graph

    Args:
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
        graph (nx Graph) : base graph to generate circuits for
        graph index (int): the index of the graph for the written
                           circuit within the file for the number of nodes
        n_nodes (int): Number of nodes in circuit
        cursor_obj: sqllite cursor object pointing to the desired database.
        return_vals (bool): return the circuits as a dataframe
    """

    n_nodes = len(graph.nodes)

    if cursor_obj is None and return_vals is False:
        raise ValueError("Graphs are generating but neither \
                          being returned nor saved")

    edges = graph.edges
    n_edges = len(edges)
    if return_vals:
        data = []
    num_configs = np.power(base, n_edges)
    for i in tqdm(range(num_configs)):
        circuit = list(np.base_repr(i, base).zfill(n_edges))
        c_dict = utils.circuit_entry_dict(circuit, graph_index,
                                          n_nodes, i, base)
        # Commit for the last one in the set
        if cursor_obj is not None:
            utils.write_circuit(cursor_obj, c_dict,
                                to_commit=i == (num_configs-1))
        if return_vals:
            data.append(c_dict)

    if return_vals:
        return pd.DataFrame(data)


def delete_table(db_file: str, n_nodes: int):
    """Deletes table in sql database

    Args:
        n_nodes (int): Number of nodes for table
        db_file (str): sql database to delete table from
    """
    connection_obj = sqlite3.connect(db_file)
    cursor_obj = connection_obj.cursor()
    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    cursor_obj.execute("DROP TABLE IF EXISTS {table}".format(table=table_name))
    connection_obj.commit()
    connection_obj.close()
    return


def generate_graphs_nodes(base: int, n_nodes: int,
                          db_file: str = None, return_vals: bool = False):
    """ Generates circuits for all graphs for a given number of nodes
        Stores circuits in table in sql database for the number of nodes
        Table labeled: 'CIRCUITS_' + str(n_nodes) + '_NODES'

    Args:
        n_nodes (int): Number of nodes for table
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
        db_file (str): sql database to store data in
        return_vals (bool): return the values in a dataframe or not
    """

    # Initialize table
    if db_file is not None:
        delete_table(db_file, n_nodes)
        table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
        connection_obj = sqlite3.connect(db_file)
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute(
           "CREATE TABLE {table} (circuit, graph_index int, edge_counts, \
            unique_key, n_nodes int, base int, no_series int, \
            has_jj int, in_non_isomorphic_set int, \
            equivalent_circuit)".format(table=table_name))
        connection_obj.commit()
    else:
        cursor_obj = None

    all_graphs = utils.get_basegraphs(n_nodes)
    data = []
    for graph_index, G in tqdm(enumerate(all_graphs)):
        data.append(generate_for_specific_graph(base, G,
                                                graph_index,
                                                cursor_obj,
                                                return_vals))

    if cursor_obj is not None:
        connection_obj.close()

    if return_vals:
        return pd.concat(data)


def trim_graph_node(db_file: str, n_nodes: int,
                    base: int = len(utils.COMBINATION_DICT)):
    """
    Marks the circuits in the database as having
    jj-s, series linear components, and being in a
    non-isomorphic set of circuits. If the circuit
    is not in the non-isomorphic set, an equivalent
    one that is in the set is recorded.

    All three must be true for the desired final set.

    Args:
        db_file (str): path to database to trim
        n_nodes (int): Number of nodes to consider
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
    """

    # Get the max number of edges
    # from fully connected graph
    all_graphs = utils.get_basegraphs(n_nodes)
    n_edges_in_graph = [len(g.edges) for g in all_graphs]
    max_edges = max(n_edges_in_graph)

    # Loop through all possible numbers of each component
    # For all unique base graphs and create non-isomorphic
    # Sets within these slices
    print("Trimming graphs with no jj's, linear elements in series",
          "and reducing isomorphic graphs...")
    is_first_write = True
    n_set = set(n_edges_in_graph)
    counts_to_consider = [x for x in itertools.product(range(max_edges+1),
                          repeat=base) if sum(x) in n_set]
    for edge_counts in tqdm(counts_to_consider):

        # Start from index 0 instead of the max one
        edge_counts = edge_counts[::-1]

        counts_str = ','.join([str(c) for c in edge_counts])
        for graph_index in range(len(all_graphs)):

            # Skip entries without the right number of edges
            # in edge counts
            if sum(edge_counts) != n_edges_in_graph[graph_index]:
                continue

            # Load the graphs with the specified edges counts and graph index
            filter_str = f"WHERE edge_counts = '{counts_str}' AND graph_index \
                           = {graph_index}"
            mapping = utils.COMBINATION_DICT
            df = utils.get_circuit_data_batch(db_file, n_nodes,
                                              elem_mapping=mapping,
                                              filter_str=filter_str)

            if df.empty:
                raise ValueError("Empty Dataframe when there shouldn't be")

            # Mark up the set
            red.full_reduction(df)

            # Find equivalent circuits for the series reduced circuits
            equiv_cir = df['equivalent_circuit'].values
            yes_series = np.logical_not(df['no_series'].values)
            for i in range(df.shape[0]):
                if yes_series:
                    row = df.iloc[i]
                    equiv_cir[i] = red.find_equiv_cir_series(db_file,
                                                             row['circuit'],
                                                             row['edges'],
                                                             row['graph_index']
                                                             )

            # Overwrite the table on the first instance
            utils.write_df(db_file, df, n_nodes,
                           overwrite=is_first_write)
            is_first_write = False


def generate_and_trim(n_nodes: int, db_file: str = "circuits.db",
                      base: int = len(utils.COMBINATION_DICT)):
    """ Generates circuits for all graphs for a given number of nodes
        Then trims identical circuits from database.
        Stores circuits in sql database

    Args:
        n_nodes (int): Number of nodes for table
        db_file (str): sql database to store data in
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
    """
    print("----------------------------------------")
    print('Starting generating ' + str(n_nodes) + ' node circuits.')
    generate_graphs_nodes(base, n_nodes, db_file)
    print("Circuits Generated for " +
          str(n_nodes) + " node circuits.")
    print("Now Trimming.")
    trim_graph_node(db_file=db_file, n_nodes=n_nodes)
    print("Finished trimming " + str(n_nodes) + " node circuits.")
    return True


def generate_all_graphs(db_file: str = "circuits.db",
                        n_nodes_start: int = 2,
                        n_nodes_stop: int = 4,
                        base: int = len(utils.COMBINATION_DICT)):
    """ Generates all circuits with numbers of nodes between
        `n_nodes_start` and `n_nodes_stop`, then removes identical
        circuits the generated circuits.

        The circuits with and without the identcal elemements removed
        are saved in sql database.

    Args:
        file (str): sql database file to store data in
        n_nodes_start (int) : Min number of nodes to generate circuits for.
        n_nodes_stop (int) : Max number of nodes to generate circuits for.
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
    """

    for n in range(n_nodes_start, n_nodes_stop+1):
        generate_and_trim(n, db_file=db_file, base=base)


if __name__ == "__main__":

    # Simple command line interface
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--db_file", type=str, default="circuits.db",
                        help="Database file to enumeration to")
    parser.add_argument("-b", "--base", type=int, default=7,
                        help="How many different types of edges to allow")
    parser.add_argument("-s", "--start", type=int, default=2,
                        help="Min number of nodes to generate circuits for")
    parser.add_argument("-p", "--stop", type=int, default=4,
                        help="Max number of nodes to generate circuits for")
    args = parser.parse_args()

    generate_all_graphs(args.db_file, args.start, args.stop, args.base)

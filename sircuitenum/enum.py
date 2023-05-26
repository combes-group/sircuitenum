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

import matplotlib.pyplot as plt
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
                                cursor_obj = None,
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
        raise ValueError("Graphs are generating but neither being returned nor saved")

    edges = graph.edges
    n_edges = len(edges)
    if return_vals:
        data = []
    num_configs = np.power(base, n_edges)
    for i in tqdm(range(num_configs)):
        circuit = list(np.base_repr(i, base).zfill(n_edges))
        c_dict = utils.circuit_entry_dict(circuit, graph_index, n_nodes, i, base)
        # Commit for the last one in the set
        if not cursor_obj is None:
            utils.write_circuit(cursor_obj, c_dict, to_commit = i==(num_configs-1))
        if return_vals:
            data.append(c_dict)
    
    if return_vals:
        return pd.DataFrame(data)


def delete_table(file: str, n_nodes: int):
    """Deletes table in sql database

    Args:
        n_nodes (int): Number of nodes for table
        file (str): sql database to delete table from
    """
    connection_obj = sqlite3.connect(file)
    cursor_obj = connection_obj.cursor()
    table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
    cursor_obj.execute("DROP TABLE IF EXISTS {table}".format(table=table_name))
    connection_obj.commit()
    connection_obj.close()
    return



def generate_graphs_nodes(base: int, n_nodes: int,
                          file: str = None, return_vals = False):
    """ Generates circuits for all graphs for a given number of nodes
        Stores circuits in table in sql database for the number of nodes
        Table labeled: 'CIRCUITS_' + str(n_nodes) + '_NODES'

    Args:
        n_nodes (int): Number of nodes for table
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
        file (str): sql database to store data in
        return_vals (bool): return the values in a dataframe or not
    """

    if not file is None:
        connection_obj = sqlite3.connect(file)
        cursor_obj = connection_obj.cursor()
        table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
        cursor_obj.execute(
                "DROP TABLE IF EXISTS {table}".format(table=table_name))
        cursor_obj.execute(
           "CREATE TABLE {table} (circuit, graph_index int, edge_counts, unique_key, n_nodes int, base int)".format(table=table_name))
        connection_obj.commit()
    else:
        cursor_obj = None

    all_graphs = utils.get_basegraphs(n_nodes)
    print("Generating circuits for", n_nodes, "nodes, base:", base)
    data = []
    for graph_index, G in tqdm(enumerate(all_graphs)):
        data.append(generate_for_specific_graph(base, G,
                                 graph_index, cursor_obj, return_vals))

    if not cursor_obj is None:
        connection_obj.close()


    if return_vals:
        return pd.concat(data)

    


def trim_graph_node(in_file: str, out_file: str, n_nodes: int, 
                        base: int = len(utils.COMBINATION_DICT)):
    """
    Trims the graphs generated from the database in_file
    to contain only non-isomorphic graphs that don't have
    linear elements in series, and then saves them to out_file.

    Args:
        n_nodes (int): Number of nodes to consider
        in_file (str): path to database to trim
        out_file (str): path to database file to save the non-isomorphic graphs
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
    counts_to_consider = [x for x in itertools.product(range(max_edges+1), repeat = base) if sum(x) in n_set]
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
            filter_str = f"WHERE edge_counts = '{counts_str}' AND graph_index = {graph_index}"
            df = utils.get_circuit_data_batch(in_file, n_nodes, elem_mapping=utils.COMBINATION_DICT,
                                                filter_str=filter_str)

            
            if df.empty:
                raise ValueError("Empty Dataframe when there shouldn't be")

            reduced = red.full_reduction(df)

            if not reduced.empty:

                # Overwrite the table on the first instance
                utils.write_df(out_file, reduced, n_nodes, overwrite=is_first_write)
                is_first_write = False


def generate_and_trim(n_nodes: int, file_untrimmed: str = "circuits.db",
                      file_trimmed: str = "circuits_trimmed.db",
                      base: int = len(utils.COMBINATION_DICT)):
    """ Generates circuits for all graphs for a given number of nodes
        Then trims identical circuits from database.
        Stores circuits in sql database

    Args:
        n_nodes (int): Number of nodes for table
        file (str): sql database to store data in
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
    """
    print('Starting generating ' + str(n_nodes) + ' node circuits.')
    generate_graphs_nodes(base, n_nodes, file_untrimmed)
    print("Circuits Generated for " +
          str(n_nodes) + " node circuits.")
    print("Now Trimming.")
    trim_graph_node(in_file=file_untrimmed, out_file=file_trimmed, n_nodes=n_nodes)
    print("Finished trimming " + str(n_nodes) + " node circuits.")
    return True


def generate_all_graphs(file_untrimmed: str = "circuits.db",
                        file_trimmed: str = "circuits_trimmed.db",
                        n_nodes_start: int = 3, 
                        n_nodes_stop: int = 4,
                        base: int = len(utils.COMBINATION_DICT)):
    """ Generates all circuits with numbers of nodes between 
        `n_nodes_start` and `n_nodes_stop`, then removes identical 
        circuits the generated circuits. 
        
        The circuits with and without the identcal elemements removed
        are saved in sql database.

    Args:
        file (str): sql database to store data in
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
        n_nodes_start (int) : The number of nodes to start generating circuits for
        stop (int) : The number of nodes to stop generating circuits at.
                        generates without ending if stop < start
    """

    current_n_nodes = n_nodes_start
    while generate_and_trim(current_n_nodes, file_untrimmed=file_untrimmed,
                            file_trimmed=file_trimmed, base=base):
        current_n_nodes = current_n_nodes + 1
        if current_n_nodes == n_nodes_stop:
            print(f"Software finished creating up until {n_nodes_stop} Nodes.")
            print("Goodbye.")
            return
    print("Software gave up.")
    print("Deleting unfinished section.")
    delete_table(file_trimmed, current_n_nodes)
    delete_table(file_untrimmed, current_n_nodes)
    print("Goodbye.")
    return


if __name__ == "__main__":
    # Simple command line interface
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--db_untrimmed", type=str, default="circuits.db",
                        help="Database file to save raw enumeration out to")
    parser.add_argument("-t", "--db_trimmed", type=str, default="circuits_trimmed.db",
                        help="Database file to save reduced enumeration out to")
    parser.add_argument("-b", "--base", type=int, default=7,
                        help="How many different types of edges to allow")
    parser.add_argument("-s", "--start", type=int, default=2,
                        help="Number of nodes to start generating from")
    parser.add_argument("-p", "--stop", type=int, default=5,
                        help="Number of nodes to stop generating at (does not do this number)")
    args = parser.parse_args()

    generate_all_graphs(args.db_untrimmed, args.db_trimmed, 
                        args.start, args.stop, args.base)
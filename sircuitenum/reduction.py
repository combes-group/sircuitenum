#!/usr/bin/env python
"""circuit_reduction.py: Contains functions to reduce the number
 of duplicate circuits present"""
__author__ = "Mohit Bhat, Eli Weissler"
__version__ = "0.1.0"
__status__ = "Development"

# -------------------------------------------------------------------
# Import Statements
# -------------------------------------------------------------------


import numpy as np
import pandas as pd
import networkx as nx

from sircuitenum import utils


def colors_match(n1_attrib, n2_attrib):
    '''returns False if either no color or if the colors do not match'''
    try:
        return n1_attrib['color'] == n2_attrib['color']
    except KeyError:
        return False


def convert_circuit_to_port_graph(circuit: list, edges: list,
                                  comp_map: dict = utils.EDGE_COLOR_DICT):
    """Encodes a circuit as a colored port graph -- see
    Enumeration of Architectures with Perfect Matchings
    Herber, Guo, Allison.

    Assumes that all circuit elements are two port-simple
    devices (i.e. symmetric)

    Assumes port type and component type isomorphism. This
    means that ports within a device and different copies
    of the same component are considered identical.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        comp_map (dict): dictionary that maps components to colors for
                         the colored graph. So it's consistent between
                        different circuits.

    Returns:
        nx.Graph representation of the port graph
    """

    # Count the degree of each vertex to include as a component
    edge_array = np.array(edges)
    vert, counts = np.unique(edge_array, return_counts=True)

    # Max degree is equal to number of vertices - 1 (fully connected)
    # Always have this for consistency of coloring
    max_deg = len(vert)-1

    # Build the graph
    G = nx.Graph()
    for i in range(len(vert)):
        # Add a port for each connection
        for p in range(counts[i]):
            G.add_node(f'v{vert[i]}_p{p}', color=counts[i])

        # Add the internal connections
        edges_to_add = []
        for p0 in range(counts[i]):
            for p1 in range(counts[i]):
                if p0 != p1 and p0 < p1:
                    edges_to_add += [(f'v{vert[i]}_p{p0}',
                                      f'v{vert[i]}_p{p1}')]
        G.add_edges_from(edges_to_add)

    # Keep track of how many ports are taken on each node
    ports_taken = np.zeros(len(vert), dtype=int)

    # Keep track of which copy of each device you're on
    device_counts = {}
    for d in comp_map:
        device_counts[d] = 0

    for i, c in enumerate(circuit):
        # Get the device count
        elem = ''.join(sorted(c))
        copy = device_counts[elem]

        # Add two ports for each device
        G.add_node(f"{elem}{copy}_p0", color=max_deg+1+comp_map[elem])
        G.add_node(f"{elem}{copy}_p1", color=max_deg+1+comp_map[elem])

        # Add edges -- internal connection and external
        # Have first edge be from port 0
        # Have second edge be from port 1
        # internal
        edges_to_add = [(f"{elem}{copy}_p0", f"{elem}{copy}_p1")]
        # external
        ext = edges[i]
        for p in range(len(ext)):
            v = ext[p]
            edges_to_add += [(f"{elem}{copy}_p{p}", f"v{v}_p{ports_taken[v]}")]
            ports_taken[v] += 1
        G.add_edges_from(edges_to_add)

        # Iterate device count
        device_counts[elem] += 1

    return G


def isomorphic_circuit_in_set(circuit: list, edges: list, c_set: list,
                              e_set=None):
    """Helper function to see if a circuit that is isomprphic
    to the given circuit
    (list/tuple of tuples) is in a set of circuits
    (list of list/tuple of tuples)

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [("J"),("L", "J"), ("C")]
        edges (list): a list of edge connections for the circuit
                        (assumed edges for everything in the set
                        if no e_set is given)
                        e.g. [(0,1), (0,2), (1,2)]
        c_set (list of lists): list of circuit-like elements
        e_set (list of lists): list of edges for the circuit list. If none
                               is given then assumes edges argument is the edge

    Returns:
        True if circuit is present in c_set, False if it isn't
    """
    port_graph = convert_circuit_to_port_graph(circuit, edges)
    for i, c2 in enumerate(c_set):
        c2_edges = edges
        if e_set is not None:
            c2_edges = e_set[i]
        port_graph_2 = convert_circuit_to_port_graph(c2, c2_edges)
        if nx.is_isomorphic(port_graph, port_graph_2, node_match=colors_match):
            return True
    return False


def mark_non_isomorphic_set(df: pd.DataFrame, to_consider: np.array):
    """Reduces a set of circuits to contain only those
    whose port graphs are not isomorphic to each other.

    Args:
        df (pd.DataFrame): Dataframe where each row represents a
                           specific circuit. Assumes that every
                           entry has the same number of nodes,
                           and comes from the same basegraph
        to_consider (pd.DataFrame): logical array that marks
                                    rows to consider. For use
                                    when some have already been
                                    eliminated for other reasons.

    Returns:
        Nothing, fills in the 'in_final_set' and 'equivalent_graph'
        columns of df
    """

    # The first graph is always unique
    in_final_set = df['in_final_set'].values
    equivalent_graph = df['equivalent_graph'].values
    unique_graphs = [convert_circuit_to_port_graph(
        df.iloc[0]['circuit'], df.iloc[0]['edges'])]

    # Compare to each previously found unique graph
    # If it's not isomorphic to any of them
    # Then add it to the list
    # If it is, then mark which graph it is isomorphic to
    for i in range(df.shape[0]):
        if to_consider[i]:
            # Compare port graph to all entries in unique set
            row = df.iloc[i]
            g_new = convert_circuit_to_port_graph(
                row['circuit'], row['edges'])
            iso_flag = False
            for (g, uid) in unique_graphs:
                if nx.is_isomorphic(g, g_new, node_match=colors_match):
                    iso_flag = True
                    equivalent_graph[i] = uid
                    break
            # Is unique - add to unique set
            if not iso_flag:
                unique_graphs.append((g_new, row['unique_key']))
                in_final_set[i] = 1
                equivalent_graph[i] = ""
            # Is not unique
            else:
                in_final_set[i] = 0

    df['in_isomorphic_set'] = in_final_set
    df['equivalent_graph'] = equivalent_graph


def remove_series_elems(circuit: list, edges: list,
                        to_reduce: list = ['L', 'C']):
    """
    Reduces the size of the given circuit by eliminating
    linear components that are in series.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        to_reduce (list, optional): circuit elements to reduce.
                                    Defaults to linear elements ['L','C'].

    Returns:
        True if the circuit cannot be reduced
        False if the circuit can be reduced
    """

    num_nodes = utils.get_num_nodes(edges)

    node_representation = utils.circuit_node_representation(
        circuit, edges)

    # List of nodes to eliminate
    to_remove = []

    # Check each node to see if there are only
    # two of the same linear element connect to it
    for node in range(num_nodes):

        # Record how many of each component is at this node
        # and how many components total are there
        n_present = {}
        total_present = 0
        for component, node_repr in node_representation.items():
            n_present[component] = node_repr[node]
            total_present += n_present[component]

        # Can't reduce if we have more than two components
        # connected to the node
        if total_present == 2:
            for component in to_reduce:
                # Reduce if both components connected to
                # a node are the same linear element
                if n_present[component] == 2:
                    to_remove.append((node, component))

    # Remove nodes that were marked
    new_circuit = circuit[:]
    new_edges = edges[:]
    for node, component in to_remove:
        to_connect = []
        i_to_remove = []
        for i in range(len(new_edges)):
            edge = new_edges[i]
            # Mark edge for removal
            # and connecting node
            if node in edge:
                i_to_remove.append(i)
                edge.remove(node)
                to_connect.append(edge[0])
        # Remove marked indices
        # And add an edge to replace it
        for i in i_to_remove:
            new_circuit.pop(i)
            new_edges.pop(i)
        edges.append(tuple(sorted))
        circuit.append((component,))

    return new_circuit, new_edges


def find_equiv_cir_series(db_file: str, circuit: list,
                          edges: list, graph_index: int):
    """
    Searches the database for circuits that are equivalent
    to the one given, up to a reduction of series linear
    circuit elements

    Args:
        db_file (str): sql database file that's already been completed
                       for the previous number of nodes.
        circuit (list): _description_
        edges (list): _description_
        graph_index (int): _description_

    Returns:
        _type_: _description_
    """

    n_nodes = utils.get_num_nodes(edges)

    # What does it look like with series elems removed
    c2, e2 = remove_series_elems(circuit, edges)
    encoding = utils.components_to_encoding(c2)
    filters = f"WHERE circuit LIKE {encoding}\
                AND graph_index = {graph_index}"
    equiv = utils.get_circuit_data_batch(db_file, n_nodes-1,
                                         filter_str=filters)

    # Return the equivalent circuit
    if equiv.iloc[0]['equivalent_circuit'] == "":
        return equiv.iloc[0]['unique_key']
    else:
        return equiv.iloc[0]['equivalent_circuit']


def jj_present(circuit: list):
    """
    Simple function that returns true if there
    is at least one JJ in the circuit and false if there isn't

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
    """

    for edge in circuit:
        for device in edge:
            if device == "J":
                return True
    return False


def full_reduction(df: pd.DataFrame):
    """Performs the full reduction procedure:
    1) Removes circuits that have isolated series linear elements
    2) Removes circuits that have no jj's
    3) Creates a set of circuits whose port-graphs are non-isomorphic


    Args:
        df (pd.Dataframe): dataframe that contains the

    Returns:
        nothing, fills in 'no_series', 'has_jj', 'in_non_isomorphic_set',
        and 'equivalent_circuit' columns of df.
    """

    # Mark series circuits
    eq_circuits = df.apply(lambda row: remove_series_elems(row['circuit'],
                                                           row['edges']),
                           axis=1)
    no_series = np.array([utils.get_num_nodes(eq_circuits[i][1]) ==
                          utils.get_num_nodes(df['edges'].iloc[i])
                          for i in range(df.shape[0])])
    df['no_series'] = no_series

    # Mark no jj circuits
    has_jj = no_series.apply(lambda row: jj_present(row['circuit']), axis=1)
    df['has_jj'] = has_jj

    # Create non-isomorphic set of yes-jj, no-series circuits
    mark_non_isomorphic_set(df, np.logical_and(no_series, has_jj))

    # Create non-isomorphic set of no-jj, no-series circuits
    mark_non_isomorphic_set(df, np.logical_and(no_series,
                                               np.logical_not(has_jj)))


def full_reduction_by_group(df: pd.DataFrame):
    """Performs the full reduction procedure,
    iterating over graph index and edge counts unique
    values for efficiency

    Args:
        df (pd.DataFrame): dataframe that contains the circuits

    Returns:
        dataframe with reduced circuit set
    """

    reduced = []

    # Iterate through graph index and edge_counts
    by_basegraph = df.groupby("graph_index")
    for graph_index in by_basegraph.indices:
        subset1 = by_basegraph.get_group(graph_index)
        by_edge_counts = subset1.groupby("edge_counts")
        for edge_counts in by_edge_counts.indices:
            subset2 = by_edge_counts.get_group(edge_counts)
            reduced.append(full_reduction(subset2))

    return pd.concat(reduced)

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
import functools
import sympy

import networkx as nx
import numpy as np
import pandas as pd

from pathlib import Path
from tqdm import tqdm

from sircuitenum import utils
from sircuitenum import reduction as red
from sircuitenum import qpackage_interface as pi

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


def find_equiv_cir_series(db_file: str, circuit: list, edges: list):
    """
    Searches the database for circuits that are equivalent
    to the one given, up to a reduction of series linear
    circuit elements

    Args:
        db_file (str): sql database file that's already been completed
                       for the previous number of nodes.
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        unique key of the equivalent circuit that is in the
        non isomorphic set
    """

    # What does it look like with series elems removed
    c2, e2 = red.remove_series_elems(circuit, edges)
    equiv = utils.find_circuit_in_db(db_file, c2, e2)
    if equiv.empty:
        return "not found"
    # Return the equivalent circuit
    if equiv.iloc[0]['equiv_circuit'] == "":
        return equiv.iloc[0]['unique_key']
    else:
        return equiv.iloc[0]['equiv_circuit']


def generate_graphs_node(db_file: str, n_nodes: int,
                         base: int, return_vals: bool = False):
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
        if Path(db_file).exists():
            delete_table(db_file, n_nodes)
        table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
        connection_obj = sqlite3.connect(db_file)
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute(
           "CREATE TABLE {table} (circuit, graph_index int, edge_counts, \
            unique_key, n_nodes int, base int, no_series int, \
            has_jj int, in_non_iso_set int, \
            equiv_circuit, PRIMARY KEY(unique_key))".format(table=table_name))
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
            print(n_nodes, edge_counts, graph_index)
            print(utils.get_circuit_data_batch(db_file, n_nodes))
            raise ValueError("Empty Dataframe when there shouldn't be")

        # Mark up the set
        red.full_reduction(df)

        # Find equivalent circuits for the series reduced circuits
        equiv_cir = df['equiv_circuit'].values
        yes_series = np.logical_not(df['no_series'].values)
        for i in range(df.shape[0]):
            if yes_series[i]:
                row = df.iloc[i]
                equiv_cir[i] = find_equiv_cir_series(db_file,
                                                     row['circuit'],
                                                     row['edges']
                                                     )

        # Update the table
        utils.update_db_from_df(db_file, df)


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
    generate_graphs_node(db_file, n_nodes, base)
    print("Circuits Generated for " +
          str(n_nodes) + " node circuits.")
    print("Now Trimming.")
    trim_graph_node(db_file=db_file, n_nodes=n_nodes, base=base)
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


def gen_hamiltonian(circuit: list, edges: list, symmetric: bool = False):
    """
    Generate a Sympy Hamiltonian for the specified circuit

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        symmetric (bool, optional): Whether to set all capacitances equal.
                                    Risks losing terms. Defaults to False.

    Returns:
        Sympy Add: Symbolic Hamiltonian where periodic modes are labeled by n
                   and extended variables are labeled by Q.
    """

    # Make paramater dictionary to load into scQubits
    elems = {
            'C': {'default_unit': 'GHz', 'default_value': 0.2},
            'L': {'default_unit': 'GHz', 'default_value': 1.0},
            'J': {'default_unit': 'GHz', 'default_value': 15.0},
            'CJ': {'default_unit': 'GHz', 'default_value': 500.0}
            }
    params = utils.gen_param_dict(circuit, edges, elems)

    if not symmetric:
        # Set random capacitance value to avoid unintentionally
        # deleting terms
        for edge, comp in params:
            if comp == "C":
                param_range = (0.1, 1)
                params[(edge, comp)] = (np.random.uniform(*param_range), "GHz")

    obj = pi.to_SCqubits(circuit, edges, 10, params=params)

    # Sympy Hamiltonian -- Expand all the trig
    H = obj.sym_hamiltonian(return_expr=True)
    H = sympy.expand_trig(sympy.nsimplify(H))

    # List of variable types
    q_list = [q for q in H.free_symbols
              if "Q" in str(q)]
    n_list = [q for q in H.free_symbols
              if "n" in str(q) and "n_g" not in str(q)]
    theta_list = [q for q in H.free_symbols
                  if "θ" in str(q)]
    ext_list = [q for q in H.free_symbols
                if "_g" in str(q) or "Φ" in str(q)]

    # Set all external parameters to 0
    for ext in ext_list:
        H = H.subs(ext, 0)

    # Terms to group
    # Q and n
    combosQ = {}
    for terms in itertools.product(q_list + n_list, repeat=2):
        combo = functools.reduce(lambda x,y: x*y, terms)
        indices = np.unique([str(x)[-1] for x in terms])
        combosQ[combo] = "E_{C"+''.join(indices)+"}"

    # Phase
    combos = [functools.reduce(lambda x, y: x*y, z)
              for z in itertools.product(theta_list, repeat=2)]
    combos += [sympy.sin(z) for z in theta_list]
    combos += [sympy.cos(z) for z in theta_list]
    combos += [functools.reduce(lambda x, y: sympy.cos(x)*sympy.cos(y), z)
               for z in itertools.product(theta_list, repeat=2)]
    combos += [functools.reduce(lambda x, y: sympy.sin(x)*sympy.sin(y), z)
               for z in itertools.product(theta_list, repeat=2)]

    H = utils.collect_expression(H, combosQ.keys())
    H = utils.collect_expression(H, combos)

    # Replace number coefficients for charge terms
    H = H.replace(lambda x: x.is_Mul,
                  lambda x: sympy.Symbol(combosQ[x.as_coeff_Mul()[1]],
                                         positive=True)*x.as_coeff_Mul()[1]
                  if x.as_coeff_Mul()[1] in combosQ else x)

    # If symmetric set all J's and L's equal to each other
    if symmetric:
        j_list = [j for j in H.free_symbols if "J" in str(j)]
        for j in j_list:
            H = H.subs(j, "J")
        l_list = [L for L in H.free_symbols if "L" in str(L)]
        for L in l_list:
            H = H.subs(L, "L")

    return H


def categorize_hamiltonian(H: sympy.core.Add):
    """
    Categorizes a Hamiltonian according to the nonlinearities
    present

    Args:
        H (sympy.core.Add): sympy Hamiltonian, generated
                            from gen_hamiltonian

    Returns:
        info: Dictionary counting the nonlinearities present.
              Considers every possibility of cos/sin and 
              extended/periodic variables. Should be 4 choices
              with one modes, 10 choices with two modes,
              and 20 with three modes.
    """

    # Expand H to make searching easier
    H_test = sympy.expand(H)

    # List of variable types
    q_list = [q for q in H.free_symbols
                if "Q" in str(q)]
    n_list = [q for q in H.free_symbols
                if "n" in str(q) and "n_g" not in str(q)]
    theta_list = [q for q in H.free_symbols
                    if "θ" in str(q)]

    # Information about the hamiltonian
    n_modes = len(theta_list)
    info = {"n_modes": n_modes,
            "periodic": [],
            "extended": [],
            "harmonic": []}

    # Categorize Modes:
    types = {}
    funcs = set()
    [[funcs.add(f) for f in x.atoms(sympy.Function)]
        for x in H_test.atoms(sympy.Mul)]
    n_str = [str(n) for n in n_list]
    q_str = [str(q) for q in q_list]
    for th in theta_list:
        if f"n{str(th)[-1]}" in n_str:
            info["periodic"].append(str(th)[-1])
            types[str(th)] = "p"
        elif sympy.cos(th) in funcs or sympy.sin(th) in funcs:
            info["extended"].append(str(th)[-1])
            types[str(th)] = "e"
        else:
            info["harmonic"].append(str(th)[-1])
            types[str(th)] = "h"

    # Add counts
    info["n_periodic"] = len(info["periodic"])
    info["n_extended"] = len(info["extended"])
    info["n_harmonic"] = len(info["harmonic"])


    # Products of sin/cos up to n_modes
    for n in range(1, n_modes+1):
        for type_combo in itertools.product(["p", "e"], repeat=n):
            for func_combo in itertools.product(["cos", "sin"], repeat=n):
                # Count the functions present
                counts = {}
                for combo in zip(func_combo, type_combo):
                    if combo in counts:
                        counts[combo] += 1
                    else:
                        counts[combo] = 1
                # Add the field in the dictionary
                combos = []
                for combo in counts:
                    combos += [combo]*counts[combo]
                # Sort alphabetically for consistency
                order = np.sort(["_".join(x) for x in combos])
                info_str = "_".join(order)
                info[info_str] = 0

    # Count the nonlinear terms
    funcs = set(functools.reduce(lambda x, y: x*y, list(x.atoms(sympy.Function)))
                for x in H_test.atoms(sympy.Mul) if len(x.atoms(sympy.Function)) > 0)
    # n = number of nonlinear terms
    for n in range(1, n_modes+1):
        # th_combo = list of variables
        for th_combo in itertools.product(theta_list, repeat=n):
            # Variable types
            th_types = [types[str(th)] for th in th_combo]
            # All different combinations of sin's and cos
            # of the two thetas
            for bar in range(n+1):
                term = 1
                # Cos terms
                for i in range(bar):
                    term *= sympy.cos(th_combo[i])
                # Sin Terms
                for i in range(bar, n):
                    term *= sympy.sin(th_combo[i])
                # Check if term was present
                print(bar, term)
                if term in funcs:
                    info_str = ["_".join(x) for x in zip(["cos"]*bar, th_types[:bar])]
                    info_str += ["_".join(x) for x in zip(["sin"]*(n-bar), th_types[bar:])]
                    info_str = "_".join(np.sort(info_str))
                    info[info_str] += 1
                    funcs.remove(term)

    return info


def refine_latex(latex_str):
    """
    Adds hats to operators, and removes cdots before
    parenthesis

    Args:
        latex_str (str): string of the latex math

    Returns:
        str: copy of the latex_str with the modifications done
    """
    latex_str = latex_str.replace("Q_", r"\hat{Q}_")
    latex_str = latex_str.replace("n_", r"\hat{n}_")
    latex_str = latex_str.replace(r"θ", r"\hat{θ}")
    latex_str = latex_str.replace(r"\cdot \left(", r"\left(")
    return latex_str


if __name__ == "__main__":

    # Simple command line interface
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--db_file", type=str, default="circuits.db",
                        help="Database file to enumeration to")
    parser.add_argument("-b", "--base", type=int, default=7,
                        help="How many different types of edges to allow")
    parser.add_argument("-s", "--start", type=int, default=2,
                        help="Min number of nodes to generate circuits for")
    parser.add_argument("-p", "--stop", type=int, default=4,
                        help="Max number of nodes to generate circuits for")
    args = parser.parse_args()

    generate_all_graphs(args.db_file, args.start, args.stop, args.base)

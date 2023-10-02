#!/usr/bin/env python
from __future__ import print_function
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
import traceback

import sympy as sym

import networkx as nx
import numpy as np
import pandas as pd

from pathlib import Path
from tqdm import tqdm
from func_timeout import func_timeout, FunctionTimedOut

from sircuitenum import utils
from sircuitenum import reduction as red
from sircuitenum import qpackage_interface as pi


import sys
import threading
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread

def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush() # Python 3 stderr is likely buffered.
    thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(s):
    '''
    use as decorator to exit process if 
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer




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
        sql_str = f"CREATE TABLE {table_name} (circuit, graph_index int, edge_counts, \
            unique_key, n_nodes int, base int, no_series int, \
            has_jj int, in_non_iso_set int, \
            equiv_circuit, "
        sql_str += "PRIMARY KEY(unique_key))"
        cursor_obj.execute(sql_str)
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


def reduce_individual_set_(args):

    filter_str = args[0]
    db_file = args[1]
    n_nodes = args[2]
    mapping = args[3]

    df = utils.get_circuit_data_batch(db_file, n_nodes,
                                      elem_mapping=mapping,
                                      filter_str=filter_str)
    if df.empty:
        print('-------------------------------')
        print(utils.get_circuit_data_batch(db_file, n_nodes))
        print("Filter String:", filter_str)
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
    to_update = ["no_series", "has_jj",
                 "in_non_iso_set", "equiv_circuit"]
    str_cols = ["equiv_circuit"]
    utils.update_db_from_df(db_file, df, to_update, str_cols)


def trim_graph_node(db_file: str, n_nodes: int,
                    base: int = len(utils.COMBINATION_DICT),
                    n_workers: int = 1):
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
        n_workers (int): The number of workers to use. Default 1.
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
    args = []
    for edge_counts in counts_to_consider:
        # Start from index 0 instead of the max one
        edge_counts = edge_counts[::-1]

        counts_str = ','.join([str(c) for c in edge_counts])
        for graph_index in range(len(all_graphs)):
            # Skip entries without the right number of edges
            # in edge counts
            if sum(edge_counts) != n_edges_in_graph[graph_index]:
                continue
            else:
                filter_str = f"WHERE edge_counts = '{counts_str}'\
                               AND graph_index = {graph_index}"
                args.append((filter_str, db_file, n_nodes,
                             utils.COMBINATION_DICT))

    # Shuffle to spread out longer cases for more accurate time
    # estimates and better parallel performance
    np.random.shuffle(args)
    if n_workers > 1:
        from multiprocessing import Pool
        pool = Pool(processes=n_workers)
        for _ in tqdm(pool.imap_unordered(reduce_individual_set_, args),
                      total=sum(1 for _ in args)):
            pass
    else:
        for arg_set in tqdm(args):
            reduce_individual_set_(arg_set)


def gen_ham_row_(uid, db_file):

    # uid, db_file = args[0], args[1]

    # Load the graphs with the specified edges counts and graph index
    filter_str = f"WHERE unique_key LIKE '{uid}'"
    n_nodes = int(uid[1])
    mapping = utils.COMBINATION_DICT
    df = utils.get_circuit_data_batch(db_file, n_nodes,
                                      elem_mapping=mapping,
                                      filter_str=filter_str)
    if df.shape[0] > 1:
        raise ValueError("Multiple Circuits on Unique Key")
    entry = df.iloc[0]

    # Generate the Hamiltonian
    try:
        H, trans, H_class = gen_hamiltonian(entry.circuit, entry.edges,
                                            symmetric=False)
        H_str = refine_latex(sym.latex(H))
        info = categorize_hamiltonian(H)
        H_sym, trans, H_class_sym = gen_hamiltonian(entry.circuit,
                                                    entry.edges,
                                                    symmetric=True)
        H_sym_str = refine_latex(sym.latex(H_sym))
        info_sym = categorize_hamiltonian(H_sym)
    except KeyboardInterrupt as kbi:
        raise kbi
    except Exception as exc:
        print("-------------------------------------------")
        print("Unable to Generate Hamiltonian for:", uid)
        print(traceback.format_exc())
        print(exc)
        print("-------------------------------------------")
        return

    # Set values
    to_update = ["H", "H_sym", "coord_transform", "H_class", "H_class_sym",
                 "nonlinearity_counts", "nonlinearity_counts_sym"]
    df.at[uid, "H"] = H_str
    df.at[uid, "H_sym"] = H_sym_str
    df.at[uid, "coord_transform"] = str(trans)
    df.at[uid, "H_class"] = refine_latex(sym.latex(H_class))
    df.at[uid, "H_class_sym"] = refine_latex(sym.latex(H_class_sym))
    for col in info:
        if col in df.columns:
            df.at[uid, col] = info[col]
            to_update.append(col)
    for col in info_sym:
        if col+"_sym" in df.columns:
            df.at[uid, col+"_sym"] = info_sym[col]
            to_update.append(col+"_sym")

    # Add nonlinearity counts
    nonlinearity_cols = [x for x in df.columns if "sin_" in x or "cos_" in x]
    nonlinearity_cols_sym = [x for x in nonlinearity_cols if "_sym" in x]
    nonlinearity_cols = [x for x in nonlinearity_cols if "_sym" not in x]
    nonlinearity_counts = "".join([str(int(x)) for x in
                                   df[nonlinearity_cols].loc[uid].values])
    nonlinearity_counts_sym = "".join([str(int(x)) for x in
                                       df[nonlinearity_cols_sym].loc[uid].values])
    df.at[uid, "nonlinearity_counts"] = nonlinearity_counts
    df.at[uid, "nonlinearity_counts_sym"] = nonlinearity_counts_sym

    # Update value in database
    utils.update_db_from_df(db_file, df, to_update,
                            str_cols=["H", "H_sym", "periodic",
                                      "extended", "harmonic",
                                      "coord_transform",
                                      "periodic_sym", "extended_sym",
                                      "harmonic_sym",
                                      "H_class", "H_class_sym",
                                      "nonlinearity_counts",
                                      "nonlinearity_counts_sym"])


# Sometimes it doesn't work and hangs :(
# 10 Minute Timeout
def timed_out_(args):
    try:
        return func_timeout(10*60, gen_ham_row_, args)
    except FunctionTimedOut:
        print(f"Could not complete {args[0]}")
    except Exception as e:
        raise e


def add_hamiltonians_to_table(db_file: str, n_nodes: int,
                              n_workers: int = 4):
    """
    Adds hamiltonians to the specified db file

    Args:
        db_file (str): database file
        n_nodes (int): number of nodes to add for
        n_workers (int): parallelize the Hamiltonian generation to this many
                         processes.

    Raises:
        ValueError: if multiple circuits with the same unique key exist

    Returns:
        None
    """

    # Add new columns
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        new_cols = ["n_periodic", "n_extended", "n_harmonic",
                    "periodic", "extended", "harmonic"]
        new_cols += gen_func_combos_(n_nodes-1).keys()
        new_cols += [x+"_sym" for x in new_cols]
        new_cols = ["H", "H_sym", "coord_transform",
                    "H_class", "H_class_sym", "nonlinearity_counts",
                    "nonlinearity_counts_sym"] + new_cols
        table_name = 'CIRCUITS_' + str(n_nodes) + '_NODES'
        for col in new_cols:
            sql_str = f"ALTER TABLE {table_name}\n"
            if "n_" in col or "cos" in col or "sin" in col:
                sql_str += f"ADD {col} int DEFAULT 0"
            else:
                sql_str += f"ADD {col}"
            cur.execute(sql_str)
            con.commit()
        unique_keys = [x[0] for x in cur.execute(f"SELECT DISTINCT unique_key\
                                                   FROM {table_name}\
                                                   WHERE in_non_iso_set LIKE 1\
                                                   AND has_jj LIKE 1").fetchall()]

    # Randmize order because difficult ones tend to be near each other
    # This will give more accurate time estimates and spread parallel better
    np.random.shuffle(unique_keys)

    # Go through all the circuits and update rows with info
    args = list(zip(unique_keys, [db_file]*len(unique_keys)))
    if n_workers > 1:
        from multiprocessing import Pool
        pool = Pool(processes=n_workers)
        for stuff in tqdm(pool.imap_unordered(timed_out_, args),
                          total=sum(1 for _ in args)):
            pass
    else:
        for arg_set in tqdm(args):
            gen_ham_row_(arg_set[0], arg_set[1])


# Find the unique set of hamiltonian classes,
# and assign each entry an "H_group"
def find_unique_hams():
    return


def generate_and_trim(n_nodes: int, db_file: str = "circuits.db",
                      base: int = len(utils.COMBINATION_DICT),
                      n_workers: int = 1):
    """ Generates circuits for all graphs for a given number of nodes
        Then trims identical circuits from database.
        Stores circuits in sql database

    Args:
        n_nodes (int): Number of nodes for table
        db_file (str): sql database to store data in
        base (int): The number of possible edges. By default this is 7:
                        (i.e., J, C, I, JI, CI, JC, JCI)
        n_workers (int): The number of workers to use. Default 1.
    """
    print("----------------------------------------")
    print('Starting generating ' + str(n_nodes) + ' node circuits.')
    generate_graphs_node(db_file, n_nodes, base)
    print("Circuits Generated for " +
          str(n_nodes) + " node circuits.")
    print("Now Trimming.")
    trim_graph_node(db_file=db_file, n_nodes=n_nodes, base=base,
                    n_workers=n_workers)
    print("Finished trimming " + str(n_nodes) + " node circuits.")
    print("Appending Hamiltonians to " + str(n_nodes) + " node circuits.")
    add_hamiltonians_to_table(db_file=db_file, n_nodes=n_nodes,
                              n_workers=n_workers)
    return True


def generate_all_graphs(db_file: str = "circuits.db",
                        n_nodes_start: int = 2,
                        n_nodes_stop: int = 4,
                        base: int = len(utils.COMBINATION_DICT),
                        n_workers: int = 1):
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
        n_workers (int): The number of workers to use. Default 1.
    """

    for n in range(n_nodes_start, n_nodes_stop+1):
        generate_and_trim(n, db_file=db_file, base=base, n_workers=n_workers)


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
        (Sympy Add, np.array, Sympy Add):
                   1) Symbolic Hamiltonian where periodic modes are labeled by
                      n and extended variables are labeled by Q.
                   2) Coordinate transformation matrix (new in terms of node
                      variables)
                   3) Hamiltonian "class" that has all constants removed.
    """

    elems = {
            'C': {'default_unit': 'GHz', 'default_value': 0.2},
            'L': {'default_unit': 'GHz', 'default_value': 1.0},
            'J': {'default_unit': 'GHz', 'default_value': 15.0},
            'CJ': {'default_unit': 'GHz', 'default_value': 500.0}
            }
    params = utils.gen_param_dict(circuit, edges, elems)

    if not symmetric:
        # Set random values to avoid unintentionally
        # deleting terms
        for edge, comp in params:
            if comp in ["C", "L"]:
                param_range = (0.1, 1)
            else:
                param_range = (1, 20)
            params[(edge, comp)] = (np.random.uniform(*param_range), "GHz")

    obj = pi.to_SCqubits(circuit, edges, params=params)

    # Sympy Hamiltonian -- Expand all the trig
    H = obj.sym_hamiltonian(return_expr=True)
    H = sym.expand_trig(sym.nsimplify(H))

    # List of variable types
    q_list = [q for q in H.free_symbols
              if "Q" in str(q)]
    n_list = [q for q in H.free_symbols
              if "n" in str(q) and "n_g" not in str(q)]
    theta_list = [q for q in H.free_symbols
                  if "θ" in str(q)]
    ext_list = [q for q in H.free_symbols
                if "_g" in str(q) or "Φ" in str(q)]
    n_modes = len(theta_list)

    # Set all external parameters to 0
    for ext in ext_list:
        H = H.subs(ext, 0)

    # Terms to group
    # Q and n
    combosQ = {}
    for terms in itertools.product(q_list + n_list, repeat=2):
        combo = functools.reduce(lambda x, y: x*y, terms)
        indices = np.unique([str(x)[-1] for x in terms])
        combosQ[combo] = "E_{C"+''.join(indices)+"}"

    # Phase -- TODO: Generalize to more products
    combos = []
    for num_terms in range(1, n_modes + 1):
        # Straight products
        combos += list(set([functools.reduce(lambda x, y: x*y, z)
                            for z in itertools.product(theta_list,
                                                       repeat=num_terms)]))
        # Trig products
        # Encoding signals cos or sin
        for encoding in itertools.product([0, 1], repeat=num_terms):
            # Modes is which num_terms modes are being considered
            for modes in itertools.combinations(range(n_modes), num_terms):
                trig_prod = 1
                for i, term in enumerate(encoding):
                    if term:
                        trig_prod *= sym.cos(theta_list[modes[i]])
                    else:
                        trig_prod *= sym.sin(theta_list[modes[i]])
                combos += [trig_prod]

    # Explicitly add theta squared terms if only one mode
    if n_modes == 1:
        combos += list(set([functools.reduce(lambda x, y: x*y, z)
                            for z in itertools.product(theta_list,
                                                       repeat=2)]))

        # combos += [sym.sin(z) for z in theta_list]
        # combos += [sym.cos(z) for z in theta_list]
        # combos += [functools.reduce(lambda x, y: sym.cos(x)*sym.cos(y), z)
        #         for z in itertools.product(theta_list, repeat=2)]
        # combos += [functools.reduce(lambda x, y: sym.sin(x)*sym.sin(y), z)
        #         for z in itertools.product(theta_list, repeat=2)]

    H = utils.collect_expression(H, combosQ.keys())
    H = utils.collect_expression(H, combos)

    # Replace number coefficients for charge terms
    H_final = H.copy()
    for q in combosQ:
        H_final = H_final.replace(lambda x: x.is_Mul
                                  and all([sym not in q.free_symbols
                                           for sym in (x/q).free_symbols]),
                                  lambda x: sym.Symbol(combosQ[q],
                                                       positive=True)*q)

    # Replace the J, L expressions with E_J, E_L
    j_list = [j for j in H_final.free_symbols if "J" in str(j)]
    l_list = [L for L in H_final.free_symbols if "L" in str(L)]
    # Replace J, L with E_J, E_L
    if not symmetric:
        for j in j_list:
            H_final = H_final.subs(j, sym.Symbol("E_{J"+f"{str(j)[-3:].replace('_','')}"+"}",
                                   positive=True))
        for L in l_list:
            H_final = H_final.subs(L, sym.Symbol("E_{L"+f"{str(L)[-3:].replace('_','')}"+"}",
                                   positive=True))
    # If symmetric set all E_J's and E_L's equal to each other
    if symmetric:
        j_list = [j for j in H_final.free_symbols if "J" in str(j)]
        for j in j_list:
            H_final = H_final.subs(j, sym.Symbol("E_J", positive=True))
        l_list = [L for L in H.free_symbols if "L" in str(L)]
        for L in l_list:
            H_final = H_final.subs(L, sym.Symbol("E_L", positive=True))

    # Generate the H_class which has all coefficients removed
    H_class = sym.expand_trig(sym.simplify(H_final))
    H_class = utils.collect_expression(H_class, combosQ.keys())
    H_class = utils.collect_expression(H_class, combos)
    H_class = H_final.copy()
    all_combos = combos + list(combosQ.keys())
    for combo in all_combos:
        H_class = H_class.replace(lambda x: x.is_Mul
                                  # Dividing removes all the terms in combo
                                  and all([sym not in combo.free_symbols
                                           for sym in (x/combo).free_symbols])
                                  # And all theta/n terms in x are also in
                                  # combo
                                  and all([sym in combo.free_symbols
                                           for sym in x.free_symbols
                                           if sym in all_combos]),
                                  lambda x: -combo if str(x)[0] == "-" else combo)
    # H_class = sym.expand_trig(sym.nsimplify(H_class))

    # Replace theta with \varphi for periodic modes
    for n_term in n_list:
        mode_num = str(n_term)[-1]
        matching_thetas = [th for th in theta_list
                           if f"θ{mode_num}" in str(th)]
        for th in matching_thetas:
            new_var = sym.Symbol(f"𝜑{mode_num}")
            H_final = H_final.replace(th, new_var)
            H_class = H_class.replace(th, new_var)

    return H_final, obj.transformation_matrix, H_class


def gen_func_combos_(n_modes):
    info = {}
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
    return info


def categorize_hamiltonian(H: sym.core.Add):
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
    H_test = sym.expand(H)

    # List of variable types
    n_list = [q for q in H.free_symbols
              if "n" in str(q) and "n_g" not in str(q)]
    theta_list = [q for q in H.free_symbols
                  if "θ" in str(q) or "𝜑" in str(q)]

    # Information about the hamiltonian
    n_modes = len(theta_list)
    info = {"n_modes": n_modes,
            "periodic": [],
            "extended": [],
            "harmonic": []}

    # Categorize Modes:
    types = {}
    funcs = set()
    [[funcs.add(f) for f in x.atoms(sym.Function)]
        for x in H_test.atoms(sym.Mul)]
    n_str = [str(n) for n in n_list]
    for th in theta_list:
        if f"n{str(th)[-1]}" in n_str:
            info["periodic"].append(str(th)[-1])
            types[str(th)] = "p"
        elif sym.cos(th) in funcs or sym.sin(th) in funcs:
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
    info.update(gen_func_combos_(n_modes))

    # Count the nonlinear terms
    funcs = set(functools.reduce(lambda x, y: x*y, list(x.atoms(sym.Function)))
                for x in H_test.atoms(sym.Mul) if len(x.atoms(sym.Function)) > 0)
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
                    term *= sym.cos(th_combo[i])
                # Sin Terms
                for i in range(bar, n):
                    term *= sym.sin(th_combo[i])
                # Check if term was present
                if term in funcs:
                    info_str = ["_".join(x) for x in
                                zip(["cos"]*bar, th_types[:bar])]
                    info_str += ["_".join(x) for x in
                                 zip(["sin"]*(n-bar), th_types[bar:])]
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
    latex_str = latex_str.replace(r"𝜑", r"\hat{𝜑}")
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
    parser.add_argument("-w", "--workers", type=int, default=1,
                        help="Number of workers to use")

    args = parser.parse_args()

    generate_all_graphs(args.db_file, args.start, args.stop, args.base,
                        n_workers=args.workers)

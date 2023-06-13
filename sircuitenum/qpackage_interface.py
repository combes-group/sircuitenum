__author__ = "Mohit Bhat, Eli Weissler"
__version__ = "0.1.0"
__status__ = "Development"
__all__ = ['single_edge_loop_kiting',
           'find_loops',
           'inductive_subgraph',
           'to_SQcircuit',
           'to_SCqubits',
           'to_CircuitQ',
           'to_Qucat']

# -------------------------------------------------------------------
# Import Statements
# -------------------------------------------------------------------

import numpy as np
import networkx as nx

import qucat as qc
import SQcircuit as sq
import circuitq as cq
import scqubits as scq
from typing import Union

import sircuitenum.utils as utils

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------


def single_edge_loop_kiting(circuit, edges):
    """ expands edges which contain loops by splitting inductors and
    adding nodes. Done since networkx doesn't calcuate loops for multigraphs

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        copies of circuit/edges where every edge that contained both a J
        and an L have been expanded into two L's with an intermediate node
    """

    # Make copies
    circuit_out = []
    edges_out = []

    # Highest index node present
    max_node = utils.get_num_nodes(edges)-1

    for element, edge in zip(circuit, edges):

        # If we have a junction and an inductor, then there's a loop
        # Make it understandable by loop finding
        # By streching the inductor into two, adding an extra node
        if "J" in element and "L" in element:

            # Put in the edge without inductors
            circuit_out.append(tuple([x for x in element if x != "L"]))
            edges_out.append(edge)

            # Make the inductors off to the side
            circuit_out.append(("L",))
            edges_out.append((edge[0], max_node + 1))
            circuit_out.append(("L",))
            edges_out.append((max_node + 1, edge[1]))

            # Keep track of how many nodes you've added
            max_node += 1

        # If there's not both a junction and inductor
        # then keep the edge the same
        else:
            circuit_out.append(element)
            edges_out.append(edge)

    return circuit_out, edges_out


def find_loops(circuit, edges, ind_elem=["J", "L"]):
    """ Provides a list of loops

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        ind_elem (list): symbols that define inductive elements.
                        Default is ind_elem = ["J", "L"]

    Returns:
        loop_lst (list): a list of loops in the circuit
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
    """

    # Expand single edge loops
    max_node_og = utils.get_num_nodes(edges)-1
    circuit_temp, edges_temp = single_edge_loop_kiting(circuit, edges)

    # Make a graph that represents only inductive edges
    ind_edges = inductive_subgraph(circuit_temp, edges_temp, ind_elem)
    G = nx.from_edgelist(ind_edges)

    # Find loops in the inductive subgraph
    # And filter out any edges that we added
    loop_lst = [tuple(sorted([x for x in c if x <= max_node_og]))
                for c in nx.cycle_basis(nx.Graph(G))]

    return loop_lst


def inductive_subgraph(circuit, edges, ind_elem=["J", "L"]):
    """Returns a list of edges that contain an inductive element

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        ind_elem (list): symbols that define inductive elements.
                        Default is ind_elem = ["J", "L"]
    """

    return [edges[i] for i in range(len(edges))
            if np.any(np.in1d(circuit[i], ind_elem))]


def to_SQcircuit(circuit: list, edges: list,
                 trunc_num: Union[int, list] = 10, **kwargs):
    """Converts circuit from list of labels and edges to a
    SQcircuit formatted circuit network

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        trunc_num (int or list):
        params (dict): dictionary with entries C, L, J, CJ,
                    which represent the paramaters for the circuit elements.
                    Additionally entries of C_units, L_units, J_units,
                    and CJ_units. Inputting nothing uses the default
                    parameter values/units from utils.ELEM_DICT.

    Returns:
        converted_circuit (SQcircuit.Circuit): returns the input circuit
                                               converted to SQcircuit.

        Charge modes are where cir.omega == 0,
        harmonic modes are when cir.omega != 0
    """

    params = kwargs.get("params", utils.gen_param_dict(circuit, edges,
                                                       utils.ELEM_DICT))

    loops = find_loops(circuit, edges)
    loop_defs = {}

    # Map inductive cycle basis to loops
    for lp in loops:
        loop_defs[lp] = sq.Loop()

    # Build sqcircuit dictionary that maps edges
    # to a list of element objects, which have
    # their loops set
    circuit_dict = {}
    for elems, edge in zip(circuit, edges):

        # Record all the loops for this edge
        loops_pres = []
        for lp in loops:
            if edge[0] in lp and edge[1] in lp:
                loops_pres.append(loop_defs[lp])

        # Add all the elements
        circuit_dict[edge] = []
        for elem in elems:
            val, units = params[(edge, elem)]
            units = "GHz"
            if elem == "C":
                id_str = "C_" + "".join([str(x) for x in edge])
                circuit_dict[edge].append(sq.Capacitor(val, units,
                                                       id_str=id_str))

            elif elem == "L":
                id_str = "L_" + "".join([str(x) for x in edge])
                circuit_dict[edge].append(sq.Inductor(val, units,
                                                      id_str=id_str,
                                                      loops=loops_pres))
            elif elem == "J":
                id_str = "J_" + "".join([str(x) for x in edge])
                if (edge, "CJ") in params:
                    val2, units2 = params[(edge, "CJ")]
                    if val2 > 0:
                        j_c = sq.Capacitor(val2, units2, id_str="C"+id_str)
                        circuit_dict[edge].append(sq.Junction(val, units,
                                                              id_str=id_str,
                                                              loops=loops_pres,
                                                              cap=j_c))
                    else:
                        circuit_dict[edge].append(sq.Junction(val, units,
                                                              id_str=id_str,
                                                              loops=loops_pres)
                                                  )
                else:
                    circuit_dict[edge].append(sq.Junction(val, units,
                                                          id_str=id_str,
                                                          loops=loops_pres))
            else:
                raise ValueError("Unknown circuit compenent present.\
                                  Must be either C, J, or L")

    sqC = sq.Circuit(circuit_dict, flux_dist='junctions')

    # Convert truncation num to list
    if not isinstance(trunc_num, list):
        trunc_num = [trunc_num]*len(sqC.omega)

    sqC.set_trunc_nums(trunc_num)

    return sqC


def to_SCqubits(circuit: list, edges: list,
                trunc_num: Union[int, list] = 10,
                cutoff: Union[int, list] = 101,
                **kwargs):
    """Converts circuit from list of labels and edges to a
    SCqubits formatted circuit network

    ## NOTE: ONLY SUPPORTS VALUES IN GHz

    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
        trunc_num (int or list): Number of eigenstates to consider for each
                                 mode in a composite circuit.
        https://scqubits.readthedocs.io/en/latest/guide/ipynb/custom_circuit_hd.html
        cutoff (int or list): Number of points to use in the underlying
                              position space for each mode.

        params (dict): dictionary with entries C, L, J, CJ,
                    which represent the paramaters for the circuit elements.
                    Additionally entries of C_units, L_units, J_units,
                    and CJ_units. Inputting nothing uses the default
                    parameter values/units from utils.ELEM_DICT.

    Returns:
        converted_circuit (scqubits.Circuit): returns the input circuit
                                               converted to scqubits.
    """
    params = kwargs.get("params", utils.gen_param_dict(circuit, edges,
                                                       utils.ELEM_DICT))

    # Build scqubits circuit yaml string
    circuit_yaml = "branches:"
    for elems, edge in zip(circuit, edges):
        edge_str = "_".join([str(x+1) for x in edge])
        # Add all the elements
        for elem in elems:
            val = f"{elem}_{edge_str} = "
            if elem == "J":
                e_str = "JJ"
                val1, _ = params[(edge), elem]
                if (edge, "CJ") in params:
                    val2, _ = params[(edge), "CJ"]
                    if val2 > 0:
                        val += f"{val1}, {val2}"
                    else:
                        val += f"{val1}, 1000"
                else:
                    val += f"{val1}, 1000"
            else:
                e_str = elem
                val += f"{params[(edge), elem][0]}"

            circuit_yaml += "\n"
            circuit_yaml += f"- ['{e_str}', {edge[0]+1}, {edge[1]+1}, {val}]"

    print(circuit_yaml)
    conv = scq.Circuit(circuit_yaml, from_file=False)

    # Set cutoff
    n_nodes = utils.get_num_nodes(edges)
    if not isinstance(cutoff, list):
        if n_nodes > 2:
            cutoff = [cutoff]*(n_nodes - 1)
        else:
            cutoff = [cutoff]
    for mode_type in ['periodic', 'extended']:
        if mode_type == "periodic":
            mode_str = "n"
        elif mode_type == "extended":
            mode_str = "ext"
        for mode in conv.var_categories[mode_type]:
            exec(f"conv.cutoff_{mode_str}_{mode}={cutoff[mode-1]}")

    # Set truncation
    if n_nodes > 2:
        hier = [[x] for x in np.arange(n_nodes-1) + 1]
        if not isinstance(trunc_num, list):
            if n_nodes > 2:
                trunc_num = [trunc_num]*(n_nodes - 1)
            else:
                hier = conv.system_hierarchy
        conv.configure(system_hierarchy=hier,
                       subsystem_trunc_dims=trunc_num)

    return conv


def to_CircuitQ(circuit: list, edges: list,
                trunc_num: Union[int, list] = 10, **kwargs):
    """Converts circuit from list of labels and edges to a
    SQcircuit formatted circuit network
    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
        trunc_num (int or list):
        params (dict): dictionary with entries C, L, J, CJ,
                    which represent the paramaters for the circuit elements.
                    Additionally entries of C_units, L_units, J_units,
                    and CJ_units. Inputting nothing uses the default
                    parameter values/units from utils.ELEM_DICT.
    Returns:
        circuitQ circuit
    """

    params = kwargs.get("params", utils.gen_param_dict(circuit, edges,
                                                       utils.ELEM_DICT))
    circuit_graph = utils.convert_circuit_to_graph(circuit, edges,
                                                   params=params)
    return cq.CircuitQ(circuit_graph)


def to_Qucat(circuit: list, edges: list,
             trunc_num: Union[int, list] = 10, **kwargs):
    """
    Converts circuit from list of labels and edges to a
    Qucat formatted circuit network
    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
        trunc_num (int or list):
        params (dict): dictionary with entries C, L, J, CJ,
                    which represent the paramaters for the circuit elements.
                    Additionally entries of C_units, L_units, J_units,
                    and CJ_units. Inputting nothing uses the default
                    parameter values/units from utils.ELEM_DICT.
    Returns:
        Qucat circuit
    """
    qc
    raise NotImplementedError("Haven't done Qucat yet")

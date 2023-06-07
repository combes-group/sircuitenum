#!/usr/bin/env python
"package_interface.py: Contains functions to enumerated edges of quantum circuits"
__author__ = "Mohit Bhat, Eli Weissler"
__version__ = "0.1.0"
__status__ = "Development"
__all__ = ['get_circuit', 'get_edges', 'get_circuit_data', 'plot_circuit']

# -------------------------------------------------------------------
# Import Statements
# -------------------------------------------------------------------

import numpy as np
import networkx as nx

import qucat as qc
import SQcircuit as sq
import circuitq as cq
import scqubits as scq
from ast import literal_eval
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
            edges_out.append((edge[0],max_node+1))
            circuit_out.append(("L",))
            edges_out.append((max_node+1,edge[1]))

            # Keep track of how many nodes you've added
            max_node += 1
        
        # If there's not both a junction and inductor
        # then keep the edge the same
        else:
            circuit_out.append(element)
            edges_out.append(edge)

    return circuit_out, edges_out


def find_loops(circuit, edges, ind_elem = ["J", "L"]):
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
    loop_lst = [tuple(sorted([x for x in c if x <= max_node_og])) for c in nx.cycle_basis(nx.Graph(G))]

    return loop_lst

def inductive_subgraph(circuit, edges, ind_elem = ["J", "L"]):
    """Returns a list of edges that contain an inductive element

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        ind_elem (list): symbols that define inductive elements. 
                        Default is ind_elem = ["J", "L"]
    """

    return [edges[i] for i in range(len(edges)) if np.any(np.in1d(circuit[i], ind_elem))]


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
                cutoff: Union[int, list] = 31,
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
        edge_str = "_".join([str(x) for x in edge])
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
            circuit_yaml += f"- ['{e_str}', {edge[0]}, {edge[1]}, {val}]"

    print(circuit_yaml)
    conv = scq.Circuit(circuit_yaml, from_file=False)

    # Set cutoff
    n_nodes = utils.get_num_nodes(edges)
    heir = conv.system_hierarchy
    if not isinstance(cutoff, list):
        if n_nodes > 2:
            n_modes = len(scq.truncation_template(heir))
            cutoff = [cutoff]*n_modes
        else:
            cutoff = [cutoff]
    for mode_type in ['periodic', 'extended']:
        if mode_type == "periodic":
            mode_str = "n"
        elif mode_type == "extended":
            mode_str = "ext"
        for mode in conv.var_categories[mode_type]:
            exec(f"conv.cutoff_{mode_str}_{mode}={cutoff[mode-1]}")

    # Convert truncation num to list
    if not isinstance(trunc_num, list):
        if n_nodes > 2:
            n_modes = len(scq.truncation_template(heir))
            trunc_num = [trunc_num]*n_modes
    conv.configure(system_hierarchy=heir,
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
                    Additionally entries of C_units, L_units, J_units, and CJ_units.
                    Inputting nothing uses the default parameter values/units from
                    utils.ELEM_DICT.
    Returns:
        circuitQ circuit
    """

    params = kwargs.get("params", utils.gen_param_dict(circuit, edges, utils.ELEM_DICT))

    circuit_graph = utils.convert_circuit_to_graph(circuit, edges, params=params)
    return cq.CircuitQ(circuit_graph)


def to_Qucat(circuit: list, edges: list, cap_default: float, jj_default: float, inductor_default: float):
    """Converts circuit from list of labels and edges to a
    qucat formatted circuit network

    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
        cap_default (float): default value for capacitors
        jj_default (float): default value for josephson junctions
        inductor_default (float): default value for inductors

    Returns:
        converted_circuit (Qcircuit): returns the circuit converted
        into a qucat circuit
    """
    i = 0
    num_c = 0
    num_l = 0
    num_j = 0

    network_list = []
    for element in circuit:
        edge = edges[i]
        if(element == '0'):
            network_list.append(
                qc.C(edge[0], edge[1], cap_default, "C_" + str(num_c)))
            num_c = num_c + 1
        elif(element == '1'):
            network_list.append(
                qc.L(edge[0], edge[1], inductor_default, "L_" + str(num_l)))
            num_l = num_l + 1
        elif(element == '2'):
            network_list.append(
                qc.J(edge[0], edge[1], jj_default, "J_" + str(num_j)))
            num_j = num_j + 1
        elif(element == '3'):
            network_list.append(
                qc.C(edge[0], edge[1], cap_default, "C_" + str(num_c)))
            num_c = num_c + 1
            network_list.append(
                qc.L(edge[0], edge[1], inductor_default, "L_" + str(num_l)))
            num_l = num_l + 1
        elif(element == '4'):
            network_list.append(
                qc.C(edge[0], edge[1], cap_default, "C_" + str(num_c)))
            num_c = num_c + 1
            network_list.append(
                qc.J(edge[0], edge[1], jj_default, "J_" + str(num_j)))
            num_j = num_j + 1
        elif(element == '5'):
            network_list.append(
                qc.L(edge[0], edge[1], inductor_default, "L_" + str(num_l)))
            num_l = num_l + 1
            network_list.append(
                qc.J(edge[0], edge[1], jj_default, "J_" + str(num_j)))
            num_j = num_j + 1
        elif(element == '6'):
            network_list.append(
                qc.C(edge[0], edge[1], cap_default, "C_" + str(num_c)))
            num_c = num_c + 1
            network_list.append(
                qc.L(edge[0], edge[1], inductor_default, "L_" + str(num_l)))
            num_l = num_l + 1
            network_list.append(
                qc.J(edge[0], edge[1], jj_default, "J_" + str(num_j)))
            num_j = num_j + 1
        else:
            print("Unrecognized component: " + str(element))
        i = i + 1
    converted_circuit = qc.Network(network_list)
    return converted_circuit


def convert_circuit_to_package_input(circuit: list, edges: list, package_name: str):
    """Converts circuit from list of labels and edges to a
    package formatted circuit network

    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
        package_name (str): name of package to convert to

    Returns:
        converted_circuit: returns the circuit converted
        into a circuit in the desired package
    """
    converted_circuit = []
    if(package_name == "SCqubits"):
        converted_circuit = convert_circuit_to_SCqubits(
            circuit, list(edges), 100e-9, 21e-7, 10e-9)
    elif(package_name == "SQcircuit"):
        converted_circuit = convert_circuit_to_SQcircuit(
            circuit, edges, 100e-15, 21e-7, 10e-9)
    elif(package_name == "CircuitQ"):
        converted_circuit = convert_circuit_to_CircuitQ(circuit, list(edges))
    elif(package_name == "Qucat"):
        converted_circuit = convert_circuit_to_Qucat(
            circuit, edges, 100e-15, 21e-7, 10e-9)
    else:
        print("unknown package")
        converted_circuit = []
    return converted_circuit


def SQCircuit_parameter_space_finding(circuit : list, edges : list):
    """Finds parameter space for given circuit, and checks validity

    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit

    Returns:
        parameter_space (dict): a dictionary describing the parameter
            space of the circuit
    """
    circuit_k = circuit.copy()
    edges_k = edges.copy()
    loop_lst, circuit_k, edges_k = loop_finding(circuit_k, edges_k)

    num_loops = len(loop_lst)
    loop_defs = []

    for j in range(num_loops):
        loop_defs.append(sq.Loop())

    network_dict, num_c, num_j, num_l = convert_to_network_dict(
        circuit, edges, loop_lst, loop_defs, SQCIRCUIT_DEFAULT_PARAMS)
    
    num_charge_modes = 0
    #print(network_dict[(0, 2)][0].energy())
    try:
        converted_circuit = sq.Circuit(network_dict, flux_dist='all')
        i = 0
        for loop in loop_defs:
            loop.set_flux(SQCIRCUIT_DEFAULT_PARAMS['phi_lst'][i])
            i = i + 1

        num_modes = converted_circuit.n
        for k in range(num_modes):
            # TODO successfully check if it is a charge mode
            try:
                converted_circuit.set_charge_offset(k+1, SQCIRCUIT_DEFAULT_PARAMS['ng_lst'][k])
                converted_circuit.set_charge_noise(k+1, SQCIRCUIT_DEFAULT_PARAMS['noise_lst'][k])
                num_charge_modes = num_charge_modes + 1
            except:
                num_charge_modes = num_charge_modes
        converted_circuit.set_trunc_nums([3]*num_modes)
        parameter_space = {
            'valid' : True,
            'ec_len': num_c,
            'ej_len': num_j,
            'el_len': num_l,
            'phi_len': num_loops,
            'charge modes': num_charge_modes,
        }
        return parameter_space
    except Exception as e:
        parameter_space = {
            'valid' : False,
            'reason': e,
            'ec_len': num_c,
            'ej_len': num_j,
            'el_len': num_l,
            'phi_len': num_loops,
            'charge modes': num_charge_modes,
        }
        return parameter_space

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
    max_node = utils.max_node(edges)

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
    n_nodes_og = utils.max_node(edges)
    circuit_temp, edges_temp = single_edge_loop_kiting(circuit, edges)

    # Make a graph that represents only inductive edges
    ind_edges = inductive_subgraph(circuit_temp, edges_temp, ind_elem)
    G = nx.from_edgelist(ind_edges)

    # Find loops in the inductive subgraph
    # And filter out any edges that we added
    loop_lst = [tuple(sorted([x for x in c if x <= n_nodes_og])) for c in nx.cycle_basis(nx.Graph(G))]

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

def gen_param_dict(circuit, edges, params=utils.ELEM_DICT):
    """_summary_

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        params (_type_, optional): _description_. Defaults to SQCIRCUIT_DEFAULT_PARAMS.
    """
    
    counts = utils.count_elems_mapped(circuit)

    param_dict = {}
    # Capacitors
    param_dict['c_list'] = [params['C']['default_value']]*counts["C"]
    param_dict['c_units'] = params['C']['default_unit']
    # Inductors
    param_dict['l_list'] = [params['L']['default_value']]*counts["L"]
    param_dict['l_units'] = params['L']['default_unit']
    # Junctions
    param_dict['j_list'] = [params['J']['default_value']]*counts["J"]
    param_dict['j_units'] = params['J']['default_unit']
    # Junction Capacitances
    param_dict['cj_list'] = [params['CJ']['default_value']]*counts["J"]
    param_dict['cj_units'] = params['CJ']['default_unit']
    
    return param_dict
    
def convert_circuit_to_SQcircuit(circuit: list, edges: list, trunc_num: int = 10, **kwargs):
    """Converts circuit from list of labels and edges to a
    SQcircuit formatted circuit network

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        trunc_num (int): 
        params (dict): dictionary with entries c_lst, l_lst, j_lst, and cj_lst,
                    which represent the paramaters for the circuit elements. 
                    Additionally entries of c_units, l_units, j_units, and cj_units.
                    Inputting nothing uses the default parameter values/units from utils.ELEM_DICT.

    Returns:
        converted_circuit (SQcircuit.Circuit): returns the input circuit converted
        into a SQcircuit circuit.

        Charge modes are where cir.omega == 0, harmonic modes are when cir.omega != 0
    """

    params = kwargs.get("params", gen_param_dict(circuit, edges, utils.ELEM_DICT))


    loops = find_loops(circuit, edges)
    loop_defs = {}

    # Map inductive cycle basis to loops
    for l in loops:
        loop_defs[l] = sq.Loop()


    # Build sqcircuit dictionary that maps edges
    # to a list of element objects, which have 
    # their loops set
    circuit_dict = {}
    elem_counts = {"C":0, "L":0, "J":0}
    for elems, edge in zip(circuit, edges):
        
        # Record all the loops for this edge
        loops_present = []
        for l in loops:
            if edge[0] in l and edge[1] in l:
                loops_present.append(loop_defs[l])

        # Add all the elements
        circuit_dict[edge] = []
        for elem in elems:
            if elem == "C":
                circuit_dict[edge].append(sq.Capacitor(params['c_list'][elem_counts["C"]],
                                 'GHz', id_str=("C_" + str(elem_counts["C"]))))
                
            elif elem == "L":
                circuit_dict[edge].append(sq.Inductor(params['l_list'][elem_counts["L"]],
                                 'GHz', id_str=("L_" + str(elem_counts["L"])),
                                 loops=loops_present))
            elif elem == "J":
                if params['cj_list'][elem_counts["J"]] > 0:
                    j_c = sq.Capacitor(params['cj_list'][elem_counts["J"]],
                                    'GHz', id_str=("J_C_" + str(elem_counts["J"])))
                    circuit_dict[edge].append(sq.Junction(params['j_list'][elem_counts["J"]],
                                 'GHz', id_str=("J_" + str(elem_counts["J"])),
                                 loops=loops_present, cap = j_c))
                else:
                    circuit_dict[edge].append(sq.Junction(params['j_list'][elem_counts["J"]],
                                 'GHz', id_str=("J_" + str(elem_counts["J"])),
                                 loops=loops_present))
            else:
                raise ValueError("Unknown circuit compenent present. Must be either C, J, or L")
            elem_counts[elem] += 1

    breakpoint()
    sqC = sq.Circuit(circuit_dict, flux_dist='junctions')

    return sqC



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


def convert_circuit_to_CircuitQ(circuit: list, edges: list):
    """Converts circuit from list of labels and edges to a
    SQcircuit formatted circuit network
    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
    Returns:
        converted_circuit (SQcircuit.Circuit): returns the input circuit converted
        into a SQcircuit circuit
    """
    # Map the circuit elements
    circuit = [COMBINATION_DICT[e] for e in circuit]
    circuit_graph = convert_circuit_to_graph(circuit, edges)
    converted_circuit = cq.CircuitQ(circuit_graph)
    return converted_circuit


def convert_circuit_to_SCqubits(circuit: list, edges: list, cap_default: float, jj_default: float, inductor_default: float):
    """Converts circuit from list of labels and edges to a
    SCqubits formatted circuit network

    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit
        cap_default (float): default value for capacitors
        jj_default (float): default value for josephson junctions
        inductor_default (float): default value for inductors

    Returns:
        converted_circuit (SCqubits.Circuit): returns the input circuit converted
        into a SCqubits circuit
    """
    circuit_yaml = """branches:"""
    i = 0
    for element in circuit:
        edge = edges[i]
        if(element == '0'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"C\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(cap_default) + "]"
        elif(element == '1'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"L\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(inductor_default) + "]"
        elif(element == '2'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"JJ\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(jj_default) + \
                ", " + str(jj_default / 2) + "]"
        elif(element == '3'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"C\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(cap_default) + "]"
            circuit_yaml = circuit_yaml + \
                "\n- [\"L\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(inductor_default) + "]"
        elif(element == '4'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"C\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(cap_default) + "]"
            circuit_yaml = circuit_yaml + \
                "\n- [\"JJ\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(jj_default) + \
                ", " + str(jj_default / 2) + "]"
        elif(element == '5'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"L\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(inductor_default) + "]"
            circuit_yaml = circuit_yaml + \
                "\n- [\"JJ\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(jj_default) + \
                ", " + str(jj_default / 2) + "]"
        elif(element == '6'):
            circuit_yaml = circuit_yaml + \
                "\n- [\"C\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(cap_default) + "]"
            circuit_yaml = circuit_yaml + \
                "\n- [\"L\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(inductor_default) + "]"
            circuit_yaml = circuit_yaml + \
                "\n- [\"JJ\", " + str(edge[0]) + "," + \
                str(edge[1]) + ", " + str(jj_default) + \
                ", " + str(jj_default / 2) + "]"
        else:
            print("Unrecognized component: " + str(element))
        i = i + 1
    # print(circuit_yaml)
    converted_circuit = scq.Circuit(circuit_yaml, from_file=False)
    return converted_circuit


def convert_circuit_to_Qucat(circuit: list, edges: list, cap_default: float, jj_default: float, inductor_default: float):
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

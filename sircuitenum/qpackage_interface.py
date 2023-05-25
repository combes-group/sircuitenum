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
# defaults
# -------------------------------------------------------------------

EC_DEFAULT = [1]*100
EJ_DEFAULT = [1]*100
EL_DEFAULT = [1]*100
ECJ_DEFAULT = [1]*100
PHI_DEFAULT = [1]*100
NG_DEFAULT = [1]*100
NOISE_DEFAULT = [0]*100

SQCIRCUIT_DEFAULT_PARAMS = {
    'ec_lst': EC_DEFAULT,
    'ej_lst': EJ_DEFAULT,
    'el_lst': EL_DEFAULT,
    'ecj_lst': ECJ_DEFAULT,
    'phi_lst': PHI_DEFAULT,
    'ng_lst': NG_DEFAULT,
    'noise_lst': NOISE_DEFAULT,
}

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
    loop_lst = [sorted([x for x in c if x <= n_nodes_og]) for c in nx.cycle_basis(nx.Graph(G))]

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










def convert_to_network_dict(circuit: list, edges: list, loop_lst: list, loop_defs: list,  params=SQCIRCUIT_DEFAULT_PARAMS):
    num_c = 0
    num_l = 0
    num_j = 0
    network_dict = {}
    i = 0
    for element in circuit:
        edge = edges[i]
        loops = []
        idx = 0
        for loop in loop_lst:
            if(loop.count(edge[0]) > 0 and loop.count(edge[1]) > 0):
                loops.append(loop_defs[idx])
            idx = idx + 1
        #print(element)
        #print(loops)
        if(element == '0'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Capacitor(params['ec_lst'][num_c], 'GHz', id_str=("C_" + str(num_c)))]})
            num_c = num_c + 1
        elif(element == '1'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Junction(params['ej_lst'][num_j], 'GHz', id_str=("J_" + str(num_j)), loops=loops), sq.Capacitor(params['ecj_lst'][num_j], 'GHz', id_str=("CJ_" + str(num_j)))]})
            num_j = num_j + 1
        elif(element == '2'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Inductor(params['el_lst'][num_l], 'GHz', id_str=("L_" + str(num_l)), loops=loops)]})
            num_l = num_l + 1
        elif(element == '3'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Capacitor(params['ec_lst'][num_c], 'GHz', id_str=("C_" + str(num_c))), sq.Capacitor(params['ecj_lst'][num_j], 'GHz', id_str=("CJ_" + str(num_j))), sq.Junction(params['ej_lst'][num_j], 'GHz', id_str=("J_" + str(num_j)), loops=loops)]})
            num_c = num_c + 1
            num_j = num_j + 1
        elif(element == '4'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Capacitor(params['ec_lst'][num_c], 'GHz', id_str=("C_" + str(num_c))), sq.Inductor(params['el_lst'][num_l], 'GHz', id_str=("L_" + str(num_l)), loops=loops)]})
            num_c = num_c + 1
            num_l = num_l + 1
        elif(element == '5'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Inductor(params['el_lst'][num_l], 'GHz', id_str=("L_" + str(num_l)), loops=loops), sq.Capacitor(params['ecj_lst'][num_j], 'GHz', id_str=("CJ_" + str(num_j))), sq.Junction(params['ej_lst'][num_j], 'GHz', id_str=("J_" + str(num_j)), loops=loops)]})
            num_l = num_l + 1
            num_j = num_j + 1
        elif(element == '6'):
            network_dict.update(
                {(edge[0], edge[1]): [sq.Capacitor(params['ec_lst'][num_c], 'GHz', id_str=("C_" + str(num_c))), sq.Inductor(params['el_lst'][num_l], 'GHz', id_str=("L_" + str(num_l)), loops=loops), sq.Capacitor(params['ecj_lst'][num_j], 'GHz', id_str=("CJ_" + str(num_j))), sq.Junction(params['ej_lst'][num_j], 'GHz', id_str=("J_" + str(num_j)), loops=loops)]})
            num_c = num_c + 1
            num_l = num_l + 1
            num_j = num_j + 1
        else:
            print("Unrecognized component: " + str(element))
        i = i + 1
    return network_dict, num_c, num_j, num_l


def convert_circuit_to_SQcircuit(circuit: list, edges: list, params=SQCIRCUIT_DEFAULT_PARAMS, trunc_num: int = 10):
    """Converts circuit from list of labels and edges to a
    SQcircuit formatted circuit network

    Args:
        circuit (list): a list of element labels for the desired circuit
        edges (list): a list of edge connections for the desired circuit

    Returns:
        converted_circuit (SQcircuit.Circuit): returns the input circuit converted
        into a SQcircuit circuit
    """
    circuit_k = circuit.copy()
    edges_k = edges.copy()
    loop_lst, circuit_k, edges_k = loop_finding(circuit_k, edges_k)
    num_loops = len(loop_lst)
    loop_defs = []

    for j in range(num_loops):
        loop_defs.append(sq.Loop())

    network_dict, num_c, num_j, num_l = convert_to_network_dict(
        circuit, edges, loop_lst, loop_defs, params)
    #print("Network dict:")
    #print(network_dict)
    #print(network_dict[(0, 1)][0].energy())
    #print(network_dict[(0, 1)][1].energy())
    #print(network_dict[(0, 1)][2].value())
    try:
        converted_circuit = sq.Circuit(network_dict, flux_dist='all')
        i = 0
        for loop in loop_defs:
            loop.set_flux(params['phi_lst'][i])
            i = i + 1

        num_modes = converted_circuit.n
        #print("There are " + str(num_modes) + " modes")
        for k in range(num_modes):
            # TODO successfully check if it is a charge mode
            try:
                converted_circuit.set_charge_offset(k+1, params['ng_lst'][k])
                converted_circuit.set_charge_noise(k+1, params['noise_lst'][k])
                #print("Mode " + str(k+1) + "is a charge mode")
            except:
                continue
                #print("Mode " + str(k+1) + "is not a charge mode")
        converted_circuit.set_trunc_nums([trunc_num]*num_modes)

        return converted_circuit
    except Exception as e:
        print("Generation of ")
        print(circuit)
        print(edges)
        print("has failed due to")
        print(e)
        return False

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

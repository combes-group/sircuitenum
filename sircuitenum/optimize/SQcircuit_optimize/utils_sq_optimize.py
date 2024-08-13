from sircuitenum import utils
from sircuitenum import visualize as viz
from sircuitenum import qpackage_interface as qpi
import numpy as np
import sircuitenum.optimize.sweep as swp
import sircuitenum.optimize.diff_evol as de
import scipy as sp
from tqdm import tqdm
import SQcircuit as sq
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import warnings



def make_sqc(circuit: list, edges: list, param_sets: list, ground_node:int = 0):
    """
    Constructs an SQcircuit circuit from the given circuit, edges,
    and parameter values

    (ECJ = 3 GHz, ECG = 20 GHz)

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [("J",),("L", "J"), ("C",)]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        param_sets (list): list of parameter values in GHz. Values
                           are given in the order they appear in circuit.
        ground_node (int, optional): Ground node. If None is given, then
                                     adds small capacitive coupling for each
                                     node to gorund. Defaults to 0.

    Returns:
        SQcircuit circuit object
    """

    # Generate the circuit object
    params = gen_param_dict_anyq(circuit, edges, param_sets)
    sqc = qpi.to_SQcircuit(circuit, edges, params=params,
                           ground_node=ground_node)

    # Set the extermal fluxes/charges
    nelems = sum(utils.count_elems_mapped(circuit).values())
    i = nelems
    for loop in sqc.loops:
        loop.set_flux(param_sets[i])
        i += 1
    for mode in range(1, utils.get_num_nodes(edges)):
        if is_charge_mode(sqc, mode):
            sqc.set_charge_offset(mode, param_sets[i])
            i += 1
    
    return sqc

def get_ngate_anyq(param_sets: list, *args):
    """
    Objective function to be minimized for optimization.
    Returns -ngates performed by the circuit

    Args:
        param_sets (list): list of parameter values in GHz. Values
                           are given in the order they appear in circuit.
        args (list): extra arguments 

    Returns:
        float: -ngates performed by the circuit
    """

    try:
        # Generate the sqcircuit object
        [row] = args
        sqc = make_sqc(row["circuit"], row["edges"], param_sets, ground_node=row["ground_node"])
        spec, _ = sqc.diag(3) # Generate first three states used for lots of stuff
        rates = swp.calc_decay_rates(sqc)
        t_1, t_phi, t_2 = swp.decoherence_time(rates)
        gate_time = swp.get_gate_time(spec[1]-spec[0], spec[2]-spec[1])
        ngates = t_2/gate_time
        return -ngates
    except:
        return 0

def get_ngate_anyq_mc(param_sets: list, *args):
    """
    Objective function to be minimized for optimization.
    Returns -ngates performed by the circuit.

    Returns the average (and optionally std) of evaluations
    sampled from a gaussian with std amp, centered on
    the value inside of param_sets
    
    Args:
        param_sets (list): list of parameter values in GHz. Values
                           are given in the order they appear in circuit.
        args (list): extra arguments: [row, nevals, amp, return_std]

    Returns:
        float: -ngates done by the circuit, or -ngates, std of samples
    """

    [row, nevals, amp, return_std] = args
    params = gen_param_dict_anyq(row["circuit"], row["edges"], param_sets)

    nelems = sum(utils.count_elems_mapped(row["circuit"]).values())
    # Run nevals times, going range on either side of params
    ngates = np.zeros(nevals)
    for i in range(nevals):
        # Values
        new_param_set = [x*np.random.normal(1, amp) for x in param_sets[:nelems]]
        # Offsets
        new_param_set += [x*np.random.normal(1, 0) for x in param_sets[nelems:]]
        ngates[i] = -get_ngate_anyq(new_param_set, *args[0:1])
    if return_std:
        return np.mean(ngates), np.std(ngates)
    else:
        return -np.mean(ngates)

def gen_param_dict_anyq(circuit: list, edges: list, param_sets: list):
    """
    Generates a dictionary of parameter values for use in
    qpackage interface.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [("J",),("L", "J"), ("C",)]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        param_sets (list): list of parameter values in GHz. Values
                           are given in the order they appear in circuit.

    Returns:
        dict: parameter values dictionary
    """

    param_dict = {}
    idx = 0
    for elems, edge in zip(circuit, edges):
        for elem in elems:
            key = (edge, elem)
            param_dict[key] = (param_sets[idx],'GHz')
            idx+=1
            # Junction capacitance
            if elem == "J":
                key = (edge, "CJ")
                param_dict[key] = (3.0, 'GHz')
    return param_dict

def gen_param_range_anyq(circuit: list, edges: list, ground_node: int,
                         mapping: dict = {'C': (0.1, 1), 'L': (0.1, 1), 'J': (3, 20)}):
    """
    Generates parameter ranges according to mapping,
    for use in bounded optimizations

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [("J",),("L", "J"), ("C",)]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        ground_node (int): Ground node. If None is given, then
                                     adds small capacitive coupling for each
                                     node to gorund. Defaults to 0.
        mapping (_type_, optional): _description_. Defaults to {'C': (0.1, 1), 'L': (0.1, 1), 'J': (3, 20)}.

    Returns:
        tuple: tuple of parameter ranges, for input to scipy optimization
    """
    # Circuit Elements
    param_range = []
    [[param_range.append(mapping[item]) for item in items] for items in circuit]
    # Offsets
    sqc = qpi.to_SQcircuit(circuit, edges, ground_node=ground_node, rand_amp=1e-05)
    # Flux
    for loop in sqc.loops:
        param_range.append((0, 1))
    # Charge
    for mode in range(1, utils.get_num_nodes(edges)):
        if is_charge_mode(sqc, mode):
            param_range.append((0, 1))
    return tuple(param_range)


def is_charge_mode(sqc: sq.Circuit, mode: int):
    """
    Helper function that returns whether the given mode
    (index from 1) is a charge mode or not

    Args:
        sqc (sq.Circuit): SQcircuit Circuit object
        mode (int): mode number (index from 1)

    Returns:
        Bool: whether the given mode is a charge mode
    """
    return mode - 1 in sqc.charge_islands

def gen_param_anyq(circuit):
    # Define mapping dictionary
    mapping = {'C': 0.1, 'L': 0.2, 'J': 10.}
    param = []
    [[param.append(mapping[item]) for item in items] for items in circuit]
    return param

def print_soln_anyq(optimal_param, convergence, savefile="history.csv"):
    df = pd.DataFrame([optimal_param])
    header = True
    if os.path.exists("history.csv"):
        header = False
    df.to_csv(savefile, mode="a", index=False, header=header)
    # print("best soln:",  np.round(optimal_param,3))
    # print("convergence", np.round(convergence,4))
    # print("----------------------------")

def sav_ngate(num_node, idx, circuit, ngate, param_best):
    with open(f'node{num_node}_ngate.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if idx==0:
            writer.writerow(['index','circuit','ngate', 'param'])
        writer.writerow([idx, circuit, ngate, param_best])


def sav_stability(file, args_sav):
    idx, ngate, mean, mean_ratio, std, std_ratio, max_dev = args_sav 
    with open(file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if idx==0:
            writer.writerow(['index','ngate', 'mean_ngate', 'mean_ratio', 'std_ngate', 'std_ratio', 'max_dev_ngate'])
        writer.writerow(args_sav)

def sav_stability_2(file, idx, std_vec):
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)  
    rows[idx+1].append(std_vec)

    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)



if __name__ == "__main__":

    # circuit = [('L',), ('C', 'L'), ('C', 'J')]
    # edges = [(0, 1), (0, 2), (1, 2)]
    # ground_node = None
    # param_set = [0.8035140053363979, 0.5788066993078237, 0.7213355271998423, 0.8123349536218263, 11.934164145015782, 0.31671821004655193]
    # make_sqc(circuit, edges, param_set, ground_node).description()

    # circuit =  [('L',), ('J', 'L'), ('C', 'J')] 
    # edges =  [(0, 1), (0, 2), (1, 2)] 
    # ground_node =  None
    # param_set = [0.84435117900681, 12.553053207706723, 0.952543957862247, 0.7871929824597942, 4.179673539347094, 0.17673479420537958, 0.6831898706660195]

    import SQcircuit as sq


    ecj = 3
    params = [0.8035140053363979, 0.5788066993078237, 0.7213355271998423, 0.8123349536218263, 11.934164145015782, 0.31671821004655193]
    loop1 = sq.Loop(id_str="loop1")
    circuit_dict = {}
    circuit_dict[(1, 2)] = [sq.Inductor(params[0], "GHz", id_str="L12", loops=[loop1])]
    circuit_dict[(1, 3)] = [sq.Capacitor(params[1], "GHz", id_str="C13"),
                            sq.Inductor(params[2], "GHz", id_str="L13", loops=[loop1]),]
    circuit_dict[(2, 3)] = [sq.Capacitor(params[3], "GHz", id_str="C23"),
                            sq.Junction(params[4], "GHz", id_str="J23", loops=[loop1],
                                    cap = sq.Capacitor(ecj, "GHz", id_str="JC23"))]
    circuit_dict[(0, 1)] = [sq.Capacitor(20, "GHz", id_str="C01")]
    circuit_dict[(0, 2)] = [sq.Capacitor(20, "GHz", id_str="C02")]
    circuit_dict[(0, 3)] = [sq.Capacitor(20, "GHz", id_str="C03")]
    cir = sq.Circuit(circuit_dict, flux_dist="junctions")

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


def get_ngate_anyq(param_sets, *args):
    [row] = args
    params = gen_param_dict_anyq(row["circuit"], row["edges"], param_sets)
    # try:
    sqc = qpi.to_SQcircuit(row.circuit, row.edges, params=params)
    for loop in sqc.loops:
        loop.set_flux(0.25)
    for mode in range(utils.get_num_nodes(row.edges)-1):
        try:
            sqc.set_charge_offset(mode, 0.25)
        except:
            continue
    # sqc.description()
    # spec = sqc.diag(3, tol=1.0e-6) # Generate first three states used for lots of stuff
    spec, _ = sqc.diag(3) # Generate first three states used for lots of stuff
    rates = swp.calc_decay_rates(sqc)
    t_1, t_phi, t_2 = swp.decoherence_time(rates)
    gate_time = swp.get_gate_time(spec[1]-spec[0], spec[2]-spec[1])
    ngates = t_2/gate_time
    # breakpoint()
    # except:
    #     ngates = 0
    #     print('tolerance error happens!!!')
    return -ngates

def get_ngate_anyq_mc(param_sets, *args):
    [row, nevals, amp] = args
    params = gen_param_dict_anyq(row.circuit, row.edges, param_sets)
    # Run nevals times, going range on either side of params
    ngates = np.zeros(nevals)
    for i in range(nevals):
        if i == nevals-1:
            amp = 0
        ngates[i] = -get_ngate_anyq([x*(1-2*(0.5-np.random.random())*amp) for x in param_sets], *args[0:1])
    return np.mean(ngates), np.std(ngates)

def gen_param_dict_anyq(circuit, edges, vals):
    param_dict = {}
    idx = 0
    for elems, edge in zip(circuit, edges):
        for elem in elems:
            key = (edge, elem)
            param_dict[key] = (vals[idx],'GHz')
            idx+=1
            # Junction capacitance
            if elem == "J":
                key = (edge, "CJ")
                param_dict[key] = (3.0, 'GHz')
    return param_dict

def gen_param_range_anyq(circuit):
    # Define mapping dictionary
    mapping = {'C': (0.05, 1), 'L': (0.1, 1), 'J': (3, 20)}
    param_range = []
    [[param_range.append(mapping[item]) for item in items] for items in circuit]
    return tuple(param_range)

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


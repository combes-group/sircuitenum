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
    params = gen_param_dict_anyq(row.circuit, row.edges, param_sets)
    # try:
    sqc = qpi.to_SQcircuit(row.circuit, row.edges, params=params)
    # sqc.description()
    sqc.diag(3, tol=1.0e-6) # Generate first three states used for lots of stuff
    rates = swp.calc_decay_rates(sqc)
    t_1, t_phi, t_2 = swp.decoherence_time(rates)
    alpha = swp.get_anharmonicity(sqc)
    gate_time = swp.get_gate_time(alpha, 1/t_1)
    ngates = t_2/gate_time
    # except:
    #     ngates = 0
    #     print('tolerance error happens!!!')
    return -ngates

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
                param_dict[key] = (20.0, 'GHz')
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


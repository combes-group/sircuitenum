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
import utils_sq_optimize as ut
import itertools
from joblib import Parallel, delayed
import warnings
warnings.filterwarnings("ignore", message="differential_evolution")
warnings.filterwarnings("ignore", message="invalid value encountered in divide")
warnings.filterwarnings("ignore", message="divide by zero")

def get_stability():
    df_ngate = pd.read_csv('node3_ngate.csv')
    db = "circuits_4_nodes_7_elems.db"
    ngate = []
    param_best = []
    circuit_idx = np.arange(80,88)
    for num_node in [3]: # All unique qubits with 2/3/4 nodes    
        df = utils.get_unique_qubits(db, num_node)
        for idx in tqdm(circuit_idx):
            row = df.iloc[idx]
            ngate = df_ngate.iloc[idx]['ngate']
            param_best = np.array( df_ngate.iloc[idx]['param'].strip('[]').split(), dtype=float)

            if len(param_best) in [7, 8] or len(param_best) > 8: # 3**8 = 6561, 4**8 = 65536, 
                n_param = 3
            elif len(param_best) in [5, 6]: # 5**6 = 15625, 6**6 = 46656
                n_param = 5
            else: n_param = 10
            param_vec = [np.linspace(param*0.9, param*1.1, num=n_param) for param in param_best]

            args = [row]
            ngate_vec = Parallel(n_jobs=100, verbose=1)(delayed(ut.get_ngate_anyq)(param, *args)
                                                for param in np.array(list(itertools.product(*param_vec))) )
            ngate_vec = -1* np.array(ngate_vec)
            args_sav = [idx, ngate, 
                        np.mean(ngate_vec), np.mean(ngate_vec)/ngate,
                        np.std(ngate_vec), np.std(ngate_vec)/ngate,
                        np.max(np.abs(ngate_vec - ngate))  ]

            ut.sav_stability(args_sav)


def get_param_std():
    n_grid = 5
    df_ngate = pd.read_csv('node3_ngate.csv')
    db = "circuits_4_nodes_7_elems.db"
    ngate = []
    param_best = []
    circuit_idx = np.arange(0,88)
    # circuit_idx = np.arange(21,22)
    for num_node in [3]: # All unique qubits with 2/3/4 nodes    
        df = utils.get_unique_qubits(db, num_node)
        for idx in circuit_idx:
            row = df.iloc[idx]
            args = [row]

            ngate = df_ngate.iloc[idx]['ngate']
            param_best = list(np.array( df_ngate.iloc[idx]['param'].strip('[]').split(), dtype=float))
            # print(param_best,'\n')

            # Find the two most parameters
            std_vec = []
            for jdx,param in enumerate(param_best):
                param_vec = np.linspace(param*0.9, param*1.1, num=n_grid)

                param_grid = []
                for kdx in range(len(param_vec)):
                    param_grid.append(param_best[:jdx] + [param_vec[kdx]] + param_best[jdx+1:])
                ngate_vec = [-ut.get_ngate_anyq(np.array(params), *args) for params in param_grid]

                # print('\n',param_grid)
                std_vec.append(np.std(ngate_vec)/ngate)
            # print('idx', idx)
            ut.sav_stability_2('node3_ngate.csv', idx, std_vec)
            



if __name__ == "__main__":
    get_param_std()


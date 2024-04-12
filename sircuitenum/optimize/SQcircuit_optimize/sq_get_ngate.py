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
import warnings
warnings.filterwarnings("ignore", message="differential_evolution")
warnings.filterwarnings("ignore", message="invalid value encountered in divide")
warnings.filterwarnings("ignore", message="divide by zero")


if __name__ == "__main__":
    db = "circuits_4_nodes_7_elems.db"
    ngate = []
    param_best = []
    circuit_idx = np.arange(0,1)
    for num_node in [3]:
        # All unique qubits with 2/3/4 nodes
        df = utils.get_unique_qubits(db, num_node)
        for idx in circuit_idx:
            print(f'\n######### Circuit No.{idx}')
            print('######### ngate:',ngate)
            print('######### param:',param_best)
            row = df.iloc[idx]
            # viz.draw_circuit_diagram(row.circuit, row.edges)
            args = [row]
            ranges = ut.gen_param_range_anyq(row.circuit)
            try:
                res = sp.optimize.differential_evolution(ut.get_ngate_anyq, ranges, workers=50, strategy='rand1bin', 
                            # popsize=50, 
                            disp=True,  args=args, updating='immediate',
                            callback=None, 
                            # maxiter=1000,
                            # mutation=(0.1, 1.99), 
                            # recombination=0.7
                            )
                print(f'@@@ Succeed for qubit: NO.{idx} \n', res)
                ngate.append(-res.fun)
                param_best.append(res.x)

            except:
                print(f"@@@ Error occurred for qubit: NO.{idx}")
                ngate.append(0)
                param_best.append(np.array([0]))
            # sav_ngate(num_node, idx, row.circuit, ngate[-1], param_best[-1])
            print(num_node, idx, row.circuit, ngate[-1], param_best[-1])


    idx = np.argmax(ngate)
    row = df.iloc[circuit_idx[idx]]
    print('\n----------------------------------------------------')
    print(f'best {num_node}-node qubit: \nindex={idx},   Ngate=%.3e'%ngate[idx])
    print(f'params: {row.circuit} --- {param_best[idx]}\n')
    # viz.draw_circuit_diagram(row.circuit, row.edges)
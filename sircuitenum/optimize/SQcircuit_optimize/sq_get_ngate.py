import  os
num_cores = "1"
os.environ["OPENBLAS_NUM_THREADS"] = num_cores
os.environ["OMP_NUM_THREADS"] = num_cores
os.environ["MKL_NUM_THREADS"] = num_cores

from sircuitenum import utils
from sircuitenum import visualize as viz
from sircuitenum import qpackage_interface as qpi
import numpy as np
import sircuitenum.optimize.sweep as swp
import sircuitenum.optimize.diff_evol as de
import scipy as sp
from tqdm import tqdm
import SQcircuit as sq
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
    for num_node in [2, 3]:
        # All unique qubits with 2/3/4 nodes
        df = utils.get_unique_qubits(db, num_node).iloc[::-1]
        ngate = [None]*df.shape[0]
        ngate_means = [None]*df.shape[0]
        ngate_stds = [None]*df.shape[0]
        param_best = [None]*df.shape[0]
        circuit_idx = np.arange(0,df.shape[0])
        # circuit_idx = [1]
        for idx in circuit_idx:
            print(f'\n######### Circuit No.{idx}')
            print('######### ngate:',ngate)
            print('######### param:',param_best)
            row = df.iloc[idx]
            # viz.draw_circuit_diagram(row.circuit, row.edges)
            ranges = ut.gen_param_range_anyq(row.circuit)
            try:
                # Initial Result
                res = sp.optimize.differential_evolution(ut.get_ngate_anyq, ranges,strategy='rand1bin', 
                        popsize=50,
                        disp=True,  args=[row],
                        callback=None,
                        polish=False,
                        workers=50,
                        tol=0.05,
                        # maxiter=1000,
                        # mutation=(0.1, 1.99), 
                        # recombination=0.7
                        )
                args2 = [row, 100, 0.05]
                ngate_means[idx], ngate_stds[idx] = ut.get_ngate_anyq_mc(res.x, *args2)
                print(f'@@@ Succeed for qubit: NO.{idx} \n', res)
                ngate[idx] = -res.fun
                param_best[idx] = res.x
                df["ngate"] = ngate
                df["ngate_mean"] = ngate_means
                df["ngate_stds"] = ngate_stds
                df["param_best"] = param_best
                df[["circuit", "edges", "ngate", "ngate_mean", "ngate_stds", "param_best"]].to_csv(f"results_{num_node}_nodes.csv", index=False)
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except:
                print(f"@@@ Error occurred for qubit: NO.{idx}")
                breakpoint()
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
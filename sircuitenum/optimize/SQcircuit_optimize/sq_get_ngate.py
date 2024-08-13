import  os
num_cores = "1"
os.environ["OPENBLAS_NUM_THREADS"] = num_cores
os.environ["OMP_NUM_THREADS"] = num_cores
os.environ["MKL_NUM_THREADS"] = num_cores

from sircuitenum import utils
from sircuitenum import visualize as viz
from sircuitenum import qpackage_interface as qpi
from sircuitenum import enumerate as enum
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
import traceback
warnings.filterwarnings("ignore", message="differential_evolution")
warnings.filterwarnings("ignore", message="invalid value encountered in divide")
warnings.filterwarnings("ignore", message="divide by zero")


def expand_ground_node(df):
    new_df = []
    df["ground_node"] = -1
    for i in tqdm(range(df.shape[0])):
        row = df.iloc[[i]].copy()
        circuit, edges = row["circuit"].iloc[0], row["edges"].iloc[0]
        for gnd in enum.find_unique_ground_placements(circuit, edges):
            new_row = row.copy()
            new_row["ground_node"] = gnd
            new_df.append(new_row)
    return pd.concat(new_df)

def remove_dangling_edges(df):
    ind_to_keep = []
    for i in tqdm(range(df.shape[0])):
        row = df.iloc[i]
        circuit, edges = row["circuit"], row["edges"]
        deg = utils.circuit_degree(circuit, edges)
        if all(d > 1 for d in deg):
            ind_to_keep.append(i)

    return df.iloc[ind_to_keep].copy()

def remove_parallel_elems(df):

    ind_to_keep = []
    for i in tqdm(range(df.shape[0])):
        row = df.iloc[i]
        circuit, edges = row["circuit"], row["edges"]
        if max(len(x) for x in circuit) == 1:
            ind_to_keep.append(i)

    return df.iloc[ind_to_keep].copy()

if __name__ == "__main__":
    db = "circuits_4_nodes_7_elems.db"
    for num_node in [3]:
        # All unique qubits with 2/3/4 nodes
        df = utils.get_unique_qubits(db, num_node)
        df.index = np.arange(df.shape[0])
        df_all = df.copy()

        if num_node > 3:
            df = remove_parallel_elems(df)
        df = remove_dangling_edges(df)
        df = expand_ground_node(df)

        # Add capacitive coupling to ground
        df_all["ground_node"] = None
        df = pd.concat([df_all, df])

        # Sort by Circuit then ground node
        df = df.sort_values(by=["unique_key", "ground_node"])

        print("Num Nodes:", num_node, "Num Circuits:", df.shape[0])

        ngate = [None]*df.shape[0]
        ngate_means = [None]*df.shape[0]
        ngate_stds = [None]*df.shape[0]
        param_best = [None]*df.shape[0]
        circuit_idx = np.arange(0, df.shape[0])
        # circuit_idx = np.arange(0, df.shape[0])[::-1]
        circuit_idx = [181]
        # skip = [126]
        skip = []
        # circuit_idx = [37]*10
        # circuit_idx = [1]
        for idx in circuit_idx:
            if idx in skip:
                continue
            row = df.iloc[idx]
            # if utils.count_elems_mapped(row.circuit)["L"] > 0:
            #     continue
            # for ground_node in range(num_node):
            ground_node = row["ground_node"]
            print(f'\n######### Circuit No.{idx}')
            print("circuit = ", row.circuit, "\nedges = ",row.edges,"\nground_node = ", ground_node)
            # print('######### ngate:',ngate_means)
            # print('######### param:',param_best)
            # viz.draw_circuit_diagram(row.circuit, row.edges)
            try:
                # Initial Result
                ranges = ut.gen_param_range_anyq(row.circuit, row.edges, row.ground_node)
                pop = 20*len(ranges)#50
                args2 = [row, 50, 0.025, False]
                # args2 = [row, 1, 0, False]
                res = sp.optimize.differential_evolution(ut.get_ngate_anyq_mc, ranges,strategy='rand1bin', 
                        popsize=pop,
                        disp=True,  args=args2,
                        callback=None,
                        polish=False,
                        workers=min(200, pop),
                        # workers=1,
                        tol=0.20,
                        init="halton",
                        maxiter=1000,
                        # maxiter=1
                        # mutation=(0.1, 1.99), 
                        # recombination=0.7
                        )

                args2 = [row, 100, 0.025, True]
                ngate_means[idx], ngate_stds[idx] = ut.get_ngate_anyq_mc(res.x, *args2)
                ngate[idx] = -res.fun
                param_best[idx] = res.x
                df["ngate"] = ngate
                df["ngate_mean"] = ngate_means
                df["ngate_stds"] = ngate_stds
                df["param_best"] = param_best
                df[["unique_key", "circuit", "edges", "ground_node", "n_periodic", "ngate", "ngate_mean", "ngate_stds", "param_best"]].to_csv(f"results_{num_node}_nodes.csv", index=False)
                print(f'@@@ Succeed for qubit: NO.{idx} \n', "peak:", round(ngate[idx]), "avg:", round(ngate_means[idx]), "std:",round(ngate_stds[idx]))
                print("circuit:", row.circuit, "edges:", row.edges)
                print("params:", param_best[idx])
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except Exception as exc:
                print(f"@@@ Error occurred for qubit: NO.{idx}")
                traceback.print_exc()
            # sav_ngate(num_node, idx, row.circuit, ngate[-1], param_best[-1])
            print(num_node, idx, row.circuit, ngate[-1], param_best[-1])


    idx = np.argmax(ngate)
    row = df.iloc[circuit_idx[idx]]
    print('\n----------------------------------------------------')
    print(f'best {num_node}-node qubit: \nindex={idx},   Ngate=%.3e'%ngate[idx])
    print(f'params: {row.circuit} --- {param_best[idx]}\n')
    # viz.draw_circuit_diagram(row.circuit, row.edges)
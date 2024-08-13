import os

import pandas as pd
import numpy as np
import scipy as sp

# from noisyopt import minimizeSPSA

import sircuitenum.optimize.sweep as swp



def get_ngates(circuit_func, params):

        cr = circuit_func(params)
        spec = cr.diag(3)

        # Get decoherence time
        rates = swp.calc_decay_rates(cr)
        t_1, t_phi, t_2 = swp.decoherence_time(rates)

        # Calculate anharmonicity/gate time
        gate_time = swp.get_gate_time(spec[1]-spec[0], spec[2]-spec[1])

        return t_2/gate_time


def get_t2(circuit_func, params):

        cr = circuit_func(params)
        cr.diag(3)

        # Get decoherence time
        rates = swp.calc_decay_rates(cr)
        t_1, t_phi, t_2 = swp.decoherence_time(rates)

        return t_2

def transmon_func(x):
    return -get_ngates(swp.make_transmon, x)

def rhombus_func(x):
    return -get_ngates(swp.make_rhombus_full, x)

def ist_func(x):
    return -get_ngates(swp.make_induc_shunt_transmon, x)

def cos_3phi_func(x):
    return -get_t2(swp.make_cos_3phi, x)

def print_soln(xk, convergence, savefile="history.csv"):
# def print_soln(xk, savefile="history.csv"):
    # ej1, ej2, ej3, ej4, phi = xk
    # entry = {"ej1": ej1,
    #         "ej2": ej2,
    #         "ej3": ej3,
    #         "ej4": ej4,
    #         "phi": phi,
    #         "ngates": ist_func(xk)}

    ej, el, ec, phi = xk
    entry = {"ej": ej,
            "el": el,
            "ec": ec,
            "phi": phi,
            "ngates": ist_func(xk)}

    # df = pd.DataFrame([entry])
    # header = True
    # if os.path.exists("history.csv"):
    #     header = False
    # df.to_csv(savefile, mode="a", index=False, header=header)

    print("best soln:", np.round(xk,3))
    # print("ngates:", entry['ngates'])
    print("convergence", np.round(convergence,4))
    print("----------------------------")

if __name__ == "__main__":


    # res = de(transmon_func, ((3,20), (0.1, 1), (0,1)), workers=5, disp=True)
    # if os.path.exists("history.csv"):
    #     raise ValueError("Remove history file or change its name")

    # ranges = ((3,20), (3,20), (3,20),(3,20), (0,1))
    ranges = ((3,20), (0.1,1), (0.1,1.5), (0,1))
    # ranges = ((0.01,0.3), (7.5,8.5), (6.5,7.5), (0,1))
    # x0 = [4.19135625, 0.11972103, 0.99913215, 0.49999335]
    # for lb, up in ranges:
    #     x0.append(np.random.random()*(up-lb)+lb)

    res = sp.optimize.differential_evolution(ist_func, ranges, workers=20, 
                        popsize=50, disp=True, callback=print_soln,
                        mutation=(0.1, 1.99), recombination=0.7)


    
    # res = sp.optimize.differential_evolution(cos_3phi_func, ranges, workers=1, 
    #                     popsize=50, disp=True, callback=print_soln,
    #                     mutation=(0.1, 1.99), recombination=0.7)

    # res = minimizeSPSA(ist_func, x0, bounds = ranges,
    #                     paired=False)

    # res = sp.optimize.dual_annealing(rhombus_func, ranges, workers=5, 
    #                     popsize=15, disp=True, callback=print_soln)
    # print(res.x, ist_func(res.x))
    # print(transmon_func((17, 0.5, 0.25)))
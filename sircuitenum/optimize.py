import warnings
import traceback
import itertools
from typing import Union
import numpy as np
import scipy as sp
from tqdm import tqdm
import SQcircuit as sq
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from multiprocessing import Pool
from skimage import measure
warnings.filterwarnings("ignore", message="differential_evolution")
warnings.filterwarnings("ignore", message="invalid value encountered in divide")
warnings.filterwarnings("ignore", message="divide by zero")

from func_timeout import func_timeout, FunctionTimedOut

from sircuitenum import utils
from sircuitenum import qpackage_interface as qpi
from sircuitenum import enumerate as enum

EPS_C = 1e-4
INT_OFFSETS_CHARGE = {0: 0.0+EPS_C, 1: 0.25+EPS_C, 2: 0.5+EPS_C, 3: 0.75+EPS_C}
# INT_OFFSETS_CHARGE = {1: 0.25+EPS_C}
EPS_F = 1e-6
INT_OFFSETS_FLUX = {0: 0.0+EPS_F, 1: 0.25+EPS_F, 2: 0.5+EPS_F, 3: 0.75+EPS_F}
# INT_OFFSETS_FLUX = {0: 0.0+EPS_F, 1: 0.5+EPS_F}
DECAYS = {  'depolarization':
                    ['capacitive',
                     'inductive',
                     'quasiparticle'],
                'dephasing':
                    ['cc',
                     'flux',
                     'charge']
             }
def get_gate_time(omega0:float, delta_omega:float, max_power:float=0.2*2*np.pi):
    """
    Estimates the gate time for a three level system with specified
    parameters, according to appendix A.

    Args:
        omega0 (float): qubit frequency E1 - E0 in GHz
        delta_omega (float): frequency of the E2 - E1 transition in GHz
        max_power (float, optional): Maximum drive strength in GHz.
                                     Defaults to 0.200.
    
    Returns:
        gate time estimate as half width of Gaussian pulse in s
    """

    # Turn into angular units
    omega0 = omega0*2*np.pi
    delta_omega = delta_omega*2*np.pi

    # Direct transitions
    delta = min(abs(omega0-delta_omega), abs(delta_omega))
    Vmax = min(max_power, omega0/10)
    if delta/2 <= Vmax:
        tau_direct = np.sqrt(np.pi/2)/(delta/2)
    else:
        tau_direct = np.sqrt(np.pi/2)/Vmax
    
    # Raman transition
    tau_raman = 60*np.sqrt(np.pi/2)/max_power

    return 5*min(tau_direct, tau_raman)*1e-09


def make_decay_plots(i_vec, j_vec, t_1, t_phi, labels, savename=""):
    """Makes a plot of decay times

    Args:
        i_vec (np.array): Row (Y) axis in t_1, t_phi
        j_vec (np.array): Col (X) axis in t_1, t_phi
        t_1 (np.array): array of t1 values in s
        t_phi (np.array): array of t_phi values in s
        labels (tuple): (Row (Y), Col (X)) axis labels for the plots
        savename (str, optional): Place to save the figure if desired. Defaults to "".

    Returns:
        figure, axis
    """

    Y, X = np.meshgrid(i_vec, j_vec, indexing='ij')
    f, ax = plt.subplots(ncols=3)
    f.set_size_inches((22,5))
    im = ax[0].pcolormesh(X,Y,t_1, cmap='rainbow',norm=matplotlib.colors.LogNorm())
    ax[0].set_xlabel(labels[1], fontsize=16)
    ax[0].set_ylabel(labels[0], fontsize=16)
    ax[0].set_title(r"$t_1$ (s)", fontsize=16)
    ax[0].tick_params(labelsize=14)

    f.colorbar(im, ax=ax[0])
    im = ax[1].pcolormesh(X,Y,t_phi, cmap='rainbow', norm=matplotlib.colors.LogNorm())
    ax[1].set_xlabel(labels[1], fontsize=16)
    ax[1].set_ylabel(labels[0], fontsize=16)
    ax[1].set_title(r"$t_{\phi}$ (s)", fontsize=16)
    ax[1].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[1])

    t_2 = 1/(1/(2*t_1)+1/t_phi)
    im = ax[2].pcolormesh(X,Y,t_2, cmap='rainbow', norm=matplotlib.colors.LogNorm())
    ax[2].set_xlabel(labels[1], fontsize=16)
    ax[2].set_ylabel(labels[0], fontsize=16)
    ax[2].set_title(r"$t_2 (s)$", fontsize=16)
    ax[2].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[2])

    if savename != "":
        plt.savefig(savename)

    return f, ax


def make_gate_plots(i_vec: np.array, j_vec: np.array, t_2: np.array,
                    alpha: np.array, g_times: np.array, labels: tuple,
                    thresh: float = 0.5, savename=""):
    """Make plots of gate times, anharmonicity, and number of gates
    Args:
        i_vec (np.array): Row (Y) axis in t_1, t_phi
        j_vec (np.array): Col (X) axis in t_1, t_phi
        t_2 (np.array): array of t2 values in s
        alpha (np.array): array of anharmonicities in 2pi*GHz
        g_times (np.array): array of gate times in s
        labels (tuple): (Row (Y), Col (X)) axis labels for the plots
        thresh (float): threshold for plotting the level set on the n gates plot
        savename (str, optional): Place to save the figure if desired. Defaults to "".

    Returns:
        figure, axis
    """

    Y, X = np.meshgrid(i_vec, j_vec, indexing='ij')
    f, ax = plt.subplots(ncols=3)
    f.set_size_inches((22,5))

    im = ax[0].pcolormesh(X,Y,alpha, cmap='rainbow')
    ax[0].set_xlabel(labels[1], fontsize=16)
    ax[0].set_ylabel(labels[0], fontsize=16)
    ax[0].set_title(r"Anharmonicity $\alpha$ (GHz)", fontsize=16)
    ax[0].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[0])

    im = ax[1].pcolormesh(X,Y,g_times*1e09, cmap='rainbow', norm=matplotlib.colors.LogNorm())
    ax[1].set_xlabel(labels[1], fontsize=16)
    ax[1].set_ylabel(labels[0], fontsize=16)
    ax[1].set_title(r"Predicted Gate Time (ns)", fontsize=16)
    ax[1].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[1])
    n_gates = t_2/g_times

    
    im = ax[2].pcolormesh(X,Y,n_gates, cmap='rainbow', norm=matplotlib.colors.LogNorm())
    ax[2].set_xlabel(labels[1], fontsize=16)
    ax[2].set_ylabel(labels[0], fontsize=16)
    ax[2].set_title(r"Predicted Number of Gates (t2/gate time)", fontsize=16)
    ax[2].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[2])

    # Find contours at specified frac of max value
    if thresh > 0:
        contours = measure.find_contours(n_gates, thresh*n_gates.max())
        Ec_interp = sp.interpolate.interp1d(np.arange(j_vec.size), j_vec)
        Ej_interp = sp.interpolate.interp1d(np.arange(i_vec.size), i_vec)

        for contour in contours:
            ax[2].plot(Ec_interp(contour[:, 1]), Ej_interp(contour[:, 0]), linewidth=2, color='k')

    i, j = np.where(n_gates == n_gates.max())
    plt.scatter(Ec_interp(j), Ej_interp(i), c = 'w', marker=(5, 1), s=80)



    if savename != "":
        plt.savefig(savename)

    return f, ax


def calc_decay_rates(cr, decay_types = DECAYS):
    """Uses sqcircuit to calculate the decay rates for the indicated decay types

    Args:
        cr (sqcircuit circuit): circuit you are interested in
        decay_types (dict, optional): dictionary like DECAYS at the top fo the file. Defaults to DECAYS.

    Returns:
        All rates are in units of 1/s
        dictionary {'depolarization':
                    {'capacitive': rate,
                     'inductive': rate,
                     'quasiparticle'}: rate
                    'dephasing':
                    {'cc': rate,
                     'flux': rate,
                     'charge'}
                     }
    """
    
    # Get raw rates
    decay_rates = {}
    for dec in decay_types:
        decay_rates[dec] = {}
        for dec_type in decay_types[dec]:
            decay_rates[dec][dec_type] = cr.dec_rate(dec_type=dec_type, states=(1,0))

    return decay_rates


def decoherence_time(decay_rates, t_1_channels = ["capacitive", "inductive", "quasiparticle"],
                                  t_phi_channels = ["flux", "charge", "cc"]):
    """Turns the dictionary of decay rates into a t1, t_phi, and t2
    given a list of channels for each error type.

    Args:
        decay_rates (dict): Dictionary of decay rates in 1/s, returned by calc_decay_rates.
        t_1_channels (list, optional): list of 'deplarization' channels to consider.
                                             Defaults to ["capacitive", "inductive"].
        t_phi_channels (list, optional): list of 'dephasing' channels to consider.
                                             Defaults to ["flux", "charge"].

    Returns:
        t_1, t_phi, t_2 in units of s
    """

    # Calculate t1, tphi
    t_1_rate = 0
    for dec_type in t_1_channels:
        rate = decay_rates['depolarization'][dec_type]
        if np.isfinite(rate):
            t_1_rate += rate
    t_1 = 1/t_1_rate
    
    t_phi_rate = 0
    for dec_type in t_phi_channels:
        rate = decay_rates['dephasing'][dec_type]
        if np.isfinite(rate):
            t_phi_rate += rate

    t_phi = 1/t_phi_rate    

    t_2 = 1/(1/(2*t_1)+1/t_phi)

    return t_1, t_phi, t_2


def get_anharmonicity(spec):
    """
    Returns the anharmonicity in units of 2*pi*hbar GHz
    E_12 - E_10 = E_2 - 2*E_1 + E_0

    Args:
        spec (np.array): energy spectrum in GHz

    Returns:
        Anharmonicity in units of GHz
    """
    return spec[2] - 2*spec[1] + spec[0]


def make_sqc(circuit: list, edges: list, param_sets: list, ground_node: int = 0,
             offset_integer: bool = False, trunc_num: Union[int, list] = 50,
             cj: float = 3.0):
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
        offset_integer (bool, optional): whether to restrict the offsets,
                                         values according to dict INT_OFFSETS
        trunc_num (int or list, optional): truncation number for each mode
        cj (float): junction capacitance in GHz. Pass 0 to ignore it.

    Returns:
        SQcircuit circuit object
    """

    # Generate the circuit object
    params = gen_param_dict_anyq(circuit, edges, param_sets, cj=cj)
    sqc = qpi.to_SQcircuit(circuit, edges, params=params,
                           ground_node=ground_node,
                           trunc_num=trunc_num)

    # Set the extermal fluxes/charges
    nelems = sum(utils.count_elems_mapped(circuit).values())
    i = nelems
    for loop in sqc.loops:
        if offset_integer:
            loop.set_flux(INT_OFFSETS_FLUX[int(param_sets[i])])
        else:
            loop.set_flux(param_sets[i])
        i += 1
    for mode in range(1, utils.get_num_nodes(edges)):
        if is_charge_mode(sqc, mode):
            if offset_integer:
                sqc.set_charge_offset(mode, INT_OFFSETS_CHARGE[int(param_sets[i])])
            else:
                sqc.set_charge_offset(mode, param_sets[i])
            i += 1
    return sqc


def get_ngate_mc(param_set: list, *args):
    """
    Objective function to be minimized for optimization.
    Returns -ngates performed by the circuit.

    Returns the average (and optionally std) of evaluations
    sampled from a gaussian with std amp, centered on
    the value inside of param_sets
    
    Args:
        param_set (list): list of parameter values in GHz. Values
                           are given in the order they appear in circuit.
        args (list): extra arguments [circuit, edges, ground_node, trunc_num,
                                      offset_integer, ntrial, amp, return_std]

    Returns:
        float: -ngates done by the circuit, or -ngates, std of samples
    """
    [ntrial, amp_elem, amp_off, return_std, workers] = args[-5:]

    # Run ntrial times, going amp on either side of params
    nelems = sum(utils.count_elems_mapped(args[0]).values())
    ngates = []
    swp_args = []
    for i in range(ntrial):
        # Generate random values and evaluate
        new_param_set = [x*np.random.normal(1, amp_elem) for x in param_set[:nelems]]
        new_param_set += [x*np.random.normal(1, amp_off) for x in param_set[nelems:]]
        swp_args.append((tuple(enumerate(new_param_set)),) + (3,) + args[:-5] + ({},) + (False,))
    if workers == 1:
        for i in range(ntrial):
            ngates.append(_sweep_helper(swp_args[i])[1]["ngate"])
    else:
        pool = Pool(processes=workers)
        for res in pool.imap_unordered(_sweep_helper, swp_args):
            ngates.append(res[1]["ngate"])

    if return_std:
        return np.mean(ngates), np.std(ngates)
    else:
        return -np.mean(ngates)


def gen_param_dict_anyq(circuit: list, edges: list, param_sets: list,
                        cj: float = 3.0):
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
        cj (float): junction capacitance in GHz. Pass 0 to ignore it.

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
            if elem == "J" and cj > 0:
                key = (edge, "CJ")
                param_dict[key] = (cj, 'GHz')
    return param_dict


def gen_param_range_anyq(circuit: list, edges: list, ground_node: int, offset_integer: bool = False,
                         mapping: dict = {'C': (0.05, 10.0), 'L': (0.05, 5.0), 'J': (1, 30)}):
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
        mapping (dict, optional): Ranges for the different components.
                                  Defaults to {'C': (0.1, 1), 'L': (0.1, 1), 'J': (3, 20)}.

    Returns:
        tuple: tuple of parameter ranges, for input to scipy optimization
    """
    # Circuit Elements
    param_range = []
    [[param_range.append(mapping[item]) for item in items] for items in circuit]
    # Offsets
    sqc = qpi.to_SQcircuit(circuit, edges, ground_node=ground_node, rand_amp=0.25)
    # Flux
    for loop in sqc.loops:
        if offset_integer:
            param_range.append((min(INT_OFFSETS_FLUX.keys()), max(INT_OFFSETS_FLUX.keys())))
        else:
            param_range.append((0, 1))
    # Charge
    for mode in range(1, utils.get_num_nodes(edges)):
        if is_charge_mode(sqc, mode):
            if offset_integer:
                param_range.append((min(INT_OFFSETS_CHARGE.keys()), max(INT_OFFSETS_CHARGE.keys())))
            else:
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


def pick_truncation(cir: sq.Circuit, thresh: float = 1e-06, neig: int = 5,
                    default_flux: int = 30, default_charge: int = 10,
                    increment_flux: int = 5, increment_charge: int = 5):
    """
    Picks a truncation number for analyzing the SQcircuit circuit
    by finding a number where adding the specified increment doesn't
    change the first neig eigenvalues by more than the specified threshold
    (defined relative to the original eigenvalues)

    Args:
        cir (sq.Circuit or tuple): circuit to get truncation number for, or
                                  (circuit, edges, params, ground_node, offset_integer)
        thresh (float, optional): relative threshold for changing eigenvalues.
                                  Defaults to 1e-06.
        neig (int, optional): number of eigenvalues to compute. Defaults to 5.
        default_flux (int, optional): default truncation for flux modes. Defaults to 50.
        default_charge (int, optional): default truncation for charge modes. Defaults to 20.
        increment_flux (int, optional): increment for flux mode. Defaults to 5.
        increment_charge (int, optional): increment for charge mode. Defaults to 5.

    Returns:
        list: truncation numbers for each mode
    """
    if isinstance(cir, tuple):
        params = cir[2]
        cir = make_sqc(*cir)
    else:
        params = None
    
    nmodes = cir.n
    truncs = [default_charge if is_charge_mode(cir, i) else
              default_flux for i in range(1, nmodes+1)]
    increments = [increment_charge if is_charge_mode(cir, i) else
                  increment_flux for i in range(1, nmodes+1)]
    cir.set_trunc_nums(truncs)
    cir.diag(5)
    diff = np.inf*np.ones(nmodes)
    def update_diff(cir, truncs, diff, i):
        old = cir.efreqs.copy()
        cir.set_trunc_nums(truncs)
        cir.diag(neig)
        diff[i] = np.max(np.abs(cir.efreqs-old)/np.abs(cir.efreqs))

    incremented = np.ones(nmodes, dtype=bool)
    while np.any(incremented):
        for i in range(nmodes):
            incremented[i] = False
            truncs[i] += increments[i]
            update_diff(cir, truncs, diff, i)
            while(diff[i] > thresh):
                truncs[i] += increments[i]
                update_diff(cir, truncs, diff, i)
                incremented[i] = True
            truncs[i] -= increments[i]
    
    if params is None:
        return truncs
    else:
        return params, truncs

# 5 min timeout to help speed things up
def _timed_out(*args, **kwargs):
    timeout_min = 60
    try:
        return func_timeout(60*timeout_min, get_ngate_mc, args, kwargs)
    except FunctionTimedOut:
        print(f"Could not complete {args[0]} ({timeout_min} min timout)")
        return 0
    except KeyboardInterrupt as KI:
        raise KI
    except Exception as e:
        print(e)
        return 0

def _sweep_helper(args, **kwargs):
    [vals, n_eig, circuit, edges, ground_node, trunc_num, offset_integer, cj, extras, just_spec] = args

    idx = tuple([x[0] for x in vals])
    param_set = tuple([x[1] for x in vals])

    cir = make_sqc(circuit, edges, param_set, ground_node, offset_integer,
                   trunc_num=trunc_num, cj=cj)
    
    cir.diag(n_eig)
    spec = cir.efreqs
    to_return = {}
    to_return["spec"] = spec
    if just_spec:
        return idx, to_return

    # Calculate anharmonicity/rates
    alpha = get_anharmonicity(spec)
    rates = calc_decay_rates(cir)
    t1, tphi, t2 = decoherence_time(rates)

    # Save anharmoniciry and gate times
    gate_time = get_gate_time(spec[1]-spec[0], spec[2]-spec[1])

    to_return["alpha"] = alpha
    to_return["rates"] = rates
    to_return["t1"] = t1
    to_return["t2"] = t2
    to_return["tphi"] = tphi
    to_return["tg"] = gate_time
    to_return["ngate"] = t2/gate_time

    # Extras
    for field in extras:
        to_return[field] = extras[field](cir)

    return idx, to_return


def sweep_params(circuit: list, edges: list, params: list, 
                 ground_node: int = 0, workers: int = 4, n_eig: int = 5,
                 extras: dict = {}, trunc_num: Union[int, list] = -1,
                 cj: float = 3.0, just_spec: bool = False, quiet: bool = False):
    """General function to perform paramater sweeps on quantum circuits
    using SQcircuit.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [("J",),("L", "J"), ("C",)]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        params (list): list of parameter values in GHz. Float entries are fixed,
                       while iterable fields are swept over.
        ground_node (int, optional): Ground node. If None is given, then
                                     adds small capacitive coupling for each
                                     node to gorund. Defaults to 0.
        workers (int, optional): Number of workers to use in parallel evalutation.
        n_eig (int, optional): Number of eigenvalues to compute and save.
        extras: (dict, optional): Optional fields to compute, providing a function
                                  that takes in an SQcircuit circuit objects.
                                  extras[str] = func for scalar
                                  extras[str] = (dims, func) for non-scalar
        trunc_num (int or list, optional): truncation number for each mode
        cj (float): junction capacitance in GHz. Pass 0 to ignore it.
        just_spec (bool): Only calculate the energy spectrum to save time.
        quiet (bool): whether to print out messages or not


    Returns:
        Many arrays that have shapes to match the dimensions of params:
        - eigenvalues (last dimension is n_eig),
        - decays (dictionary that maps to arrays), 
        - gate_time, 
        - anharmonicity
    """

    # Calculate the return array size
    # From parameter inputs
    arr_size = []
    ranges = []
    for p in params:
        if isinstance(p, float) or isinstance(p, int):
            arr_size.append(1)
            ranges.append(np.array([p]))
        else:
            ranges.append(p)
            arr_size.append(len(p))

    # Construct results dictionary
    results = {}
    results["rates"] = {  'depolarization':
                            {'capacitive':np.zeros(arr_size),
                            'inductive':np.zeros(arr_size),
                            'quasiparticle':np.zeros(arr_size)},
                          'dephasing':
                            {'cc':np.zeros(arr_size),
                            'flux':np.zeros(arr_size),
                            'charge':np.zeros(arr_size)}
                     }
    results["spec"] = np.zeros(arr_size + [n_eig])
    fields = ["spec", "alpha", "t1", "t2", "tphi", "tg", "ngate"]
    for field in fields[1:]:
        results[field] = np.zeros(arr_size)
    for field in extras:
        if isinstance(extras[field], tuple):
            results[field] = np.zeros(arr_size + extras[field][0])
            extras[field] = extras[field][1]
        else:
            results[field] = np.zeros(arr_size)
    if just_spec:
        fields = ["spec"]
    fields = fields + list(extras.keys())


    # Estimate truncation number
    if trunc_num == -1:
        mean_params = [np.mean(x) for x in ranges]
        cir = make_sqc(circuit, edges, mean_params, ground_node=ground_node)
        trunc_num = pick_truncation(cir)

    if not quiet:
        print("----------------------------")
        print("Sweeping Circuit", circuit, edges, f"({workers} workers)")
        print("Ground Node:", ground_node)
        print("Truncation Numbers:", trunc_num)
        print("Ranges:")
        count = 0
        for i in range(len(circuit)):
            print(" edge:", edges[i])
            for j, elem in enumerate(circuit[i]):
                if ranges[count].size > 1:
                    print(" ", elem, (ranges[count][0], ranges[count][-1], ranges[count].size))
                else:
                    print(" ", elem, ranges[count][0])
                count += 1
        print(" offsets:")
        for i in range(count, len(ranges)):
            if ranges[i].size > 1:
                print(" ", (ranges[i][0], ranges[i][-1], ranges[i].size))
            else:
                print(" ", ranges[i][0])
        print("----------------------------")               
    

    # Parameter values to iterate over
    vals = itertools.product(*[enumerate(x) for x in ranges])
    vals = [(v,) + (n_eig, circuit, edges, ground_node,
                    trunc_num, False, cj, extras, just_spec) for v in vals]
    if workers > 1:
        pool = Pool(processes=workers)
        for idx, res in tqdm(pool.imap_unordered(_sweep_helper, vals),
                        total=sum(1 for _ in vals)):
            # Save values
            for field in fields:
                results[field][idx] = res[field]
            if "rates" in res:
                for dec in res["rates"]:
                    for dec_type in results["rates"][dec]:
                        results["rates"][dec][dec_type][idx] = res["rates"][dec][dec_type]
    else:
        for v in tqdm(vals):
            idx, res = _sweep_helper(v)
            # Save value
            for field in fields:
                results[field][idx] = res[field]
            if "rates" in res:
                for dec in res["rates"]:
                    for dec_type in results["rates"][dec]:
                        results["rates"][dec][dec_type][idx] = res["rates"][dec][dec_type]

    # Squeeze 1 length dimensions
    for field in fields:
        results[field] = np.squeeze(results[field])
    if "rates" in res:
        for dec in results["rates"]:
            for dec_type in results["rates"][dec]:
                results["rates"][dec][dec_type] = np.squeeze(results["rates"][dec][dec_type])

    return results


def optimize_diff_evol(circuit: list, edges: list, ground_node: int,
                       ranges: list = None, offset_integer: bool = False,
                       trials: list = [1, 100],
                       amps: dict = {"elem": [0, 0.025], "offset": [0, 1e-06]},
                       trunc_num: Union[int, list] = -1,
                       cj: float = 3.0, quiet: bool = False,
                       **kwargs):
    
    kwargs = dict({'disp': 'True', 'popsize': 20,
                   "callback": None, "polish": False,
                   "workers": 1, "tol": 0.1, "init": "halton",
                   "maxiter": 1000}, **kwargs)

    # Auto make ranges if none is given
    if ranges is None:
        ranges = gen_param_range_anyq(circuit, edges, ground_node, offset_integer)
    kwargs["bounds"] = ranges

    # Determine integrality of variables
    integrality = np.zeros(len(ranges), dtype=bool)
    if offset_integer:
        nelems = sum(utils.count_elems_mapped(circuit).values())
        for i in range(nelems, integrality.size):
            integrality[i] = True
    kwargs["integrality"] = integrality

    # Dictionary with results
    to_return = {}
    
    # Estimate truncation number if none is given
    if trunc_num == -1:
        if kwargs["workers"] > 1:
            random_params = [[np.exp(np.random.random()*(np.log(ranges[i][1])-np.log(ranges[i][0]))+np.log(ranges[i][0])) 
                              if not integrality[i] else np.random.randint(*ranges[i]) for i in range(len(ranges))]
                              for i in range(kwargs["workers"])]
            args = [(circuit, edges, p, ground_node, offset_integer) for p in random_params]
            pool = Pool(processes=kwargs["workers"])
            trunc_vals = []
            param_vals = []
            if not quiet:
                print("Picking Truncation Number with", kwargs["workers"], "randomly chosen points")
            
            for p, res in tqdm(pool.imap_unordered(pick_truncation, args)):
                trunc_vals.append(res)
                param_vals.append(p)
            
            trunc_vals = np.array(trunc_vals)
            param_vals = np.array(param_vals)
            to_return["max_trunc"] = list(np.max(trunc_vals, axis=0))
            trunc_num = np.round(np.percentile(trunc_vals, 90, axis=0)).astype(int)
            to_return["trunc_num"] = list(trunc_num)
            if not quiet:
                print("Maximum Cutoffs:", to_return["max_trunc"])
                print("Chosen Values (90th Percentile)", trunc_num)
        else:
            random_params = [np.random.random()*(x[1]-x[0])+x[0] for x in ranges]
            cir = make_sqc(circuit, edges, random_params, ground_node=ground_node)
            trunc_num = pick_truncation(cir)
            to_return["trunc_num"] = list(trunc_num)
            if not quiet:
                print("Picking Truncation Number with Avg Parameter Value")
                print("Chosen Values", trunc_num)

    if not quiet:
        print("----------------------------")
        print("Optimizing", circuit, edges, "using differential evolution", f"({kwargs['workers']} workers)")
        print("Ground node:", ground_node)
        print("Truncation numbers:", trunc_num)
        print("Offset integer:", offset_integer)
        print("Ranges:")
        count = 0
        for i in range(len(circuit)):
            print(" edge:", edges[i])
            for j, elem in enumerate(circuit[i]):
                if len(ranges[count]) > 1:
                    print(" ", elem, (ranges[count][0], ranges[count][-1]))
                else:
                    print(" ", elem, ranges[count][0])
                count += 1
        print(" offsets (charge then flux):", ranges[count:])
        print("MC Settings: (Optimize, Eval)", "trials -", trials, "amps -", amps)
        print("DE args:", kwargs)
        print("----------------------------")               

    # Run differential evolution
    # [circuit, edges, ground_node, trunc_num, offset_integer, cj,
    #  ntrial, amp_elem, amp_off, return_std]
    args = [circuit, edges, ground_node, trunc_num, offset_integer, cj,
            trials[0], amps["elem"][0], amps["offset"][0], False, 1]
    res = sp.optimize.differential_evolution(_timed_out, args=args, **kwargs)
    # res = sp.optimize.differential_evolution(get_ngate_mc, args=args, **kwargs)

    if not quiet:
        print("Finished optimization\n", res)
        print("----------------------------")      

    to_return["ngate"] = -res.fun
    cir = make_sqc(circuit, edges, res.x, ground_node=ground_node)
    # if offset_integer:
    #     ii = 0
    #     for i in range(len(res.x)):
    #         if integrality[i]:
    #             if is_charge_mode(cir, ii):
    #                 res.x[i] = INT_OFFSETS_CHARGE[res.x[i]]
    #             else:
    #                 res.x[i] = INT_OFFSETS_FLUX[res.x[i]]
    #             ii += 1
    to_return["param_best"] = res.x

    # Run final evaluation
    args2 = [circuit, edges, ground_node, trunc_num, False, cj,
             trials[1], amps["elem"][1], amps["offset"][1], True,
             kwargs["workers"]]
    to_return["ngate_mean"] , to_return["ngate_std"] = get_ngate_mc(res.x, *args2)

    if not quiet:
        print("Finished evaluation")
        print("mean (+/- std):", int(to_return["ngate_mean"]),
              "+/-", int(to_return["ngate_std"]))
        print("----------------------------")

    return to_return
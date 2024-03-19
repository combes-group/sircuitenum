import itertools
import matplotlib

import SQcircuit as sq
import numpy as np
import matplotlib.pyplot as plt
# Set matplotlib font to match a powerpoint font
# plt.rcParams['font.family'] = "Arial"
from tqdm import tqdm
from scipy.optimize import minimize
from skimage import measure
from pathlib import Path

import scipy as sp

#################
## NOTE: For the circuit making functions, tried to standardize the order 
##       to be ec, ej, el, ng, phi with any multiples grouped together
#################

# https://arxiv.org/pdf/2206.08319.pdf
#
# Section 5.3 Estimating decay and dephasing rates
#
# Depolarization:
#   - Capacative
#   - Inductive
#   - Quasiparticle
# Dephasing:
#   - Critical Current
#   - Charge Noise (can set)
#   - Flux Noise (can set)
#
# Questions:
#   - Setting t experiment 10 microseconds by default
#   - Setting omega low and omega hi
#   - Default value for charge/flux bias?
#
DECAYS = {  'depolarization':
                    ['capacitive',
                     'inductive',
                     'quasiparticle'],
                'dephasing':
                    ['cc',
                     'flux',
                     'charge']
             }


def func_min(t, alpha, t1):
    """
    Function to minimize for calculating gate time. 
    Represents the negative of the population that ends in the first excited state.
    Derived from assuming that the incoming control pulse is Gaussian
    in time only considering the first three states.

    From Andras homework.

    Args:
        t (float): time to run the gate (units of ns) (independent variable)
        alpha (flaot): anharmonicity (units of 2pi*GHz)
        t1 (float): t1 decay time (units of ns)
        max_power (float): maximum power (units of 2pi*Ghz)

    Returns:
        negative of fraction of population that could end in the first excited state
    """
    
    return -np.exp(-t / t1) / (1 + np.exp(- (alpha* t)**2))


def guess_fn(alpha, t1, tmin=-2, tmax=5, numz=100000, max_power=None):
    """Initial guess function for gate time minimization

    Args:
        alpha (flaot): anharmonicity (units of 2pi*GHz)
        t1 (float): t1 decay time (units of ns)
        tmin (int, optional): Power of 10 to start the sweep at
        tmax (int, optional): Power of 10 to end the sweep at
        numz (int, optional): Number of samples. Defaults to 100000.
        max_power (float, optional): Max drive amplitude (units of GHz)

    Returns:
        The gate length that minimizes func_min over the specified range
    """
    tgrid = np.logspace(tmin, tmax, num=numz)
    
    if not max_power is None:
        # Get a minimum gate 
        # time based on maximum power output
        lam = np.exp(-(tgrid**2)*(alpha**2)/2)
        t_min = np.pi/(2*np.pi*max_power*np.sqrt(lam**2 + 1))

        # breakpoint()
        
        # Remove from consideration all gates that would be
        # faster than the minimum time
        tgrid = tgrid[tgrid > t_min]


    tidx = np.argmin(func_min(tgrid, alpha, t1))
    return tgrid[tidx]  

def get_gate_time(alpha, t1, max_power=1):
    """Optimized gate time for a given anharmonicity/t1

    Args:
        alpha (flaot): anharmonicity (units of 2pi*GHz)
        t1 (float): t1 decay time (units of s)
        max_power (float): Max drive power (units of GHz)
    Returns:
        The gate length that maximizes the population in the first excited state
    """
    # Scale to ns
    t1 = 1e09*t1



    x0 = guess_fn(alpha, t1, max_power=max_power)
    # bnds = sp.optimize.Bounds(lb=0, ub=float('inf'))
    # result = minimize(func_min, x0 = guess_fn(alpha,t1), args = (alpha, t1), tol = 1e-19)
    # Scale to s to return
    # return result.x[0]*1e-09
    return x0*1e-09

def sweep_params(circuit_func, params, n_eig=5):
    """General function to perform paramater sweeps on quantum circuits

    Args:
        circuit_func (function): function that creates your desired circuit. 
                                 Assumes the input is a tuple of length params.
        params (tuple): Tuple of paramaters to sweep through. 
                        Each entry is a vector of values to sweep through
        n_eig (int, optional): Number of eigenvalues to calculate. Defaults to 5.

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
    total_iters = 1
    for p in params:
        n = len(p)
        arr_size.append(n)
        total_iters*=n

    decays = {  'depolarization':
                    {'capacitive':np.zeros(arr_size),
                     'inductive':np.zeros(arr_size),
                     'quasiparticle':np.zeros(arr_size)},
                'dephasing':
                    {'cc':np.zeros(arr_size),
                     'flux':np.zeros(arr_size),
                     'charge':np.zeros(arr_size)}
             }

    spec = np.zeros(arr_size + [n_eig])
    gate_time = np.zeros(arr_size)
    alpha_mat = np.zeros(arr_size)

    # Iterate through all combinations of paramaters
    for vals in tqdm(itertools.product(*[enumerate(p) for p in params]),
                                     total=total_iters):    
        
        # Extract the index and parameter set
        idx = tuple([x[0] for x in vals])
        param_set = tuple([x[1] for x in vals])

        cr = circuit_func(param_set)

        spec[idx], _ = cr.diag(n_eig)

        # Calculate anharmonicity/rates
        alpha = get_anharmonicity(cr)
        rates = calc_decay_rates(cr)

        # Save decay rates
        for dec in decays:
            for dec_type in decays[dec]:
                decays[dec][dec_type][idx]= rates[dec][dec_type]

        # Save anharmoniciry and gate times
        alpha_mat[idx] = alpha
        gate_time[idx] = get_gate_time(alpha,1/(rates['depolarization']['capacitive']+rates['depolarization']['inductive']))


        # print(idx, param_set, alpha, gate_time[idx])

    return spec, decays, gate_time, alpha_mat


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


def decoherence_time(decay_rates, t_1_channels = ["capacitive", "inductive"],
                                  t_phi_channels = ["flux", "charge"]):
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
    
    t_phi_rate = 1
    for dec_type in t_phi_channels:
        rate = decay_rates['dephasing'][dec_type]
        if np.isfinite(rate):
            t_phi_rate += rate

    t_phi = 1/t_phi_rate    

    t_2 = 1/(1/(2*t_1)+1/t_phi)

    return t_1, t_phi, t_2


def get_anharmonicity(cr):
    """
    Returns the anharmonicity in units of 2*pi*hbar GHz
    E_12 - E_10 = E_2 - 2*E_1 + E_0

    Args:
        cr (sqcircuit): circuit

    Returns:
        Anharmonicity in units of 2pi*GHz
    """
    return (cr._efreqs[2] - 2*cr._efreqs[1] + cr._efreqs[0])*1e-9


def make_transmon(params, trunc_num=60):
    """Function to make a transmon circuit using sqcircuit

    Args:
        params (tuple): (ec, ej, ng)
        trunc_num (int, optional): Truncation for linear algebra.
                                    Defaults to 60.

    Returns:
        sqcircuit circuit
    """

    ec, ej, ng = params 


    C = sq.Capacitor(ec, 'GHz',Q=1e6 ,error=10)
    # CJ = sq.Capacitor(3.6, 'GHz',Q=1e6 ,error=10)
    JJ = sq.Junction(ej,'GHz', A=1e-7, x=3e-06)
    
    # define the circuit
    elements = {
        (0, 1): [JJ, C]
    }

    cr = sq.Circuit(elements, flux_dist='all')
    cr.set_charge_offset(1,ng)
    cr.set_trunc_nums([trunc_num])

    # Generate first three states used for lots of stuff
    cr.diag(3)
    

    return cr

def make_fluxonium(params, trunc_num=40):
    """Function to make a fluxonium circuit using sqcircuit

    Args:
        params (tuple): (ej, el, phi)
        trunc_num (int, optional): Truncation for linear algebra.
                                    Defaults to 40.

    Returns:
        sqcircuit circuit
    """

    ej, el, phi = params 

    loop1 = sq.Loop()
    CJ = sq.Capacitor(2.6, 'GHz',Q=1e6 ,error=10)
    C = sq.Capacitor(1, 'GHz',Q=1e6 ,error=10)
    L = sq.Inductor(el,'GHz',Q=500e6 ,loops=[loop1])
    JJ = sq.Junction(ej,'GHz',cap =CJ , A=1e-7, x=3e-06, loops=[loop1])
    # JJ = sq.Junction(ej,'GHz', A=1e-7, x=3e-06, loops=[loop1])

    # define the circuit
    elements = {
        (0, 1): [JJ, L]
    }

    cr = sq.Circuit(elements, flux_dist='all')
    loop1.set_flux(phi)
    cr.set_trunc_nums([trunc_num])

    # Generate first three states used for lots of stuff
    cr.diag(3)
    

    return cr

def make_zero_pi(params, trunc_num=60):
    """Function to make a 0-pi circuit using sqcircuit

    Args:
        params (tuple): (ec, ej, ng)
        trunc_num (int, optional): Truncation for linear algebra.
                                    Defaults to 20.

    Returns:
        sqcircuit circuit
    """

    ec, ej, el, phi = params 

    loop1 = sq.Loop()
    C = sq.Capacitor(ec, 'GHz',Q=1e6 ,error=10)
    CJ = sq.Capacitor(10, 'GHz',Q=1e6 ,error=10)
    L = sq.Inductor(el,'GHz',Q=500e6 ,loops=[loop1])
    JJ = sq.Junction(ej,'GHz',cap =CJ , A=1e-7, x=3e-06, loops=[loop1])

    # define the circuit
    elements = {(0, 1): [CJ, JJ],
                (0, 2): [L],
                (0, 3): [C],
                (1, 2): [C],
                (1, 3): [L],
                (2, 3): [CJ, JJ]}

    cr = sq.Circuit(elements, flux_dist='all')
    loop1.set_flux(phi)
    #cr.set_charge_offset(1,ng)
    cr.set_trunc_nums([trunc_num,trunc_num])

    # Generate first three states used for lots of stuff
    cr.diag(3)
    
    return cr    


def make_cos_3phi(params, trunc_num=2):
    """Function to make a 0-pi circuit using sqcircuit

    Args:
        params (tuple): (ec, ej, ng)
        trunc_num (int, optional): Truncation for linear algebra.
                                    Defaults to 20.

    Returns:
        sqcircuit circuit
    """

    ec, ej, el = params
    phi1, phi2 = 0,0
    ng = 0

    loop1 = sq.Loop()
    loop2 = sq.Loop()
    C = sq.Capacitor(ec, 'GHz',Q=1e6 ,error=10)
    CJ = sq.Capacitor(10, 'GHz',Q=1e6 ,error=10)
    L1 = sq.Inductor(el,'GHz',Q=500e6 ,loops=[loop1])
    JJ1 = sq.Junction(ej,'GHz',cap =CJ , A=1e-7, x=3e-06, loops=[loop1])
    JJ12 = sq.Junction(ej,'GHz',cap =CJ , A=1e-7, x=3e-06, loops=[loop1,loop2])
    L2 = sq.Inductor(el,'GHz',Q=500e6 ,loops=[loop2])
    JJ2 = sq.Junction(ej,'GHz',cap =CJ , A=1e-7, x=3e-06, loops=[loop2])
    

    # define the circuit
    elements = {(0, 1): [CJ, JJ1],
                (0, 2): [L1],
                (0, 3): [C],
                (1, 2): [C],
                (1, 3): [L1],
                (2, 3): [CJ, JJ12],
                (3, 4): [C],
                (3, 5): [L2],
                (4, 5): [CJ, JJ2],
                (2, 5): [C],
                (2, 4): [L2]
    }

    cr = sq.Circuit(elements, flux_dist='all')
    loop1.set_flux(phi1)
    loop2.set_flux(phi2)
    for i in range(6):
        try:
            cr.set_charge_offset(i,ng)
        except:
            print(i, "is not a charge mode")

    cr.set_trunc_nums([trunc_num, trunc_num, trunc_num, trunc_num, trunc_num])

    # Generate first three states used for lots of stuff
    cr.diag(3)
    
    return cr 

def make_induc_shunt_transmon(params, trunc_num=30):
    """Function to make an inductively shunted transmon using sqcircuit

    Args:
        params (tuple): (ec, ej, ng)
        trunc_num (int, optional): Truncation for linear algebra.
                                    Defaults to 30.

    Returns:
        sqcircuit circuit
    """

    ec, ej, el, phi = params
    
    loop1 = sq.Loop()
    
    C = sq.Capacitor(ec, 'GHz',Q=1e6 ,error=10)
    CJ = sq.Capacitor(2.5, 'GHz',Q=1e6 ,error=10)
    L = sq.Inductor(el,'GHz',Q=500e6 ,loops=[loop1])
    # JJ = sq.Junction(ej,'GHz', A=1e-7, cap=CJ, x=3e-06, loops=[loop1])
    JJ = sq.Junction(ej,'GHz', A=1e-7, x=3e-06, loops=[loop1])
    # define the circuit
    elements = {
        (0, 1): [JJ, L, C]
    }

    cr = sq.Circuit(elements, flux_dist='all')
    loop1.set_flux(phi)
    cr.set_trunc_nums([trunc_num])

    # Generate first three states used for lots of stuff
    cr.diag(3)
    

    return cr


def make_rhombus_full(params, trunc_num=10):

    ej1, ej2, ej3, ej4, phi = params 

    loop1 = sq.Loop()
    C = sq.Capacitor(0.2, 'GHz',Q=1e6 ,error=10)
    JJ1 = sq.Junction(ej1,'GHz',A=1e-7, x=3e-06, loops=[loop1])
    JJ2 = sq.Junction(ej2,'GHz',A=1e-7, x=3e-06, loops=[loop1])
    JJ3 = sq.Junction(ej3,'GHz',A=1e-7, x=3e-06, loops=[loop1])
    JJ4 = sq.Junction(ej4,'GHz',A=1e-7, x=3e-06, loops=[loop1])

    # define the circuit
    # define the circuit
    elements = {
        (0, 1): [JJ1, C],
        (1, 2): [JJ2, C],
        (2, 3): [JJ3, C],
        (3, 0): [JJ4, C]
    }

    cr = sq.Circuit(elements, flux_dist='all')
    loop1.set_flux(phi)

    for i in range(3):
        cr.set_charge_offset(i+1,0.25)

    cr.set_trunc_nums([trunc_num, trunc_num, trunc_num])

    # Generate first three states used for lots of stuff
    # cr.diag(3)
    

    return cr

def make_rhombus(params, trunc_num=10):

    ej1, ej2, ng, phi,  = params 

    loop1 = sq.Loop()
    C = sq.Capacitor(0.2, 'GHz',Q=1e6 ,error=10)
    JJ1 = sq.Junction(ej1,'GHz',A=1e-7, x=3e-06, loops=[loop1])
    JJ2 = sq.Junction(ej2,'GHz',A=1e-7, x=3e-06, loops=[loop1])

    # define the circuit
    # define the circuit
    elements = {
        (0, 1): [JJ1, C],
        (1, 2): [JJ1, C],
        (2, 3): [JJ1, C],
        (3, 0): [JJ2, C]
    }

    cr = sq.Circuit(elements, flux_dist='all')
    loop1.set_flux(phi)
    for i in range(3):
        cr.set_charge_offset(i+1,ng)
    cr.set_trunc_nums([trunc_num, trunc_num, trunc_num])

    # Generate first three states used for lots of stuff
    # cr.diag(3)
    

    return cr

##
## TODO: Generalize:
##          1) Automate sweep by generating __vecs at "coarse", "fine", "single point", etc.
##          2) Seperate image/plot function to allow loading in saved arrays
##

def induc_shunt_transmon_sweep(img_dir = "/home/eweissler/img/ist_sweep/test"):

    ej_vec = np.linspace(17,20, 100)
    el_vec = np.linspace(0.1,0.15, 100)
    ec_vec = [1]

    # ej_vec = np.linspace(22,29, 50)
    # el_vec = np.linspace(22,28, 50)
    # ej_vec = np.linspace(25,35, 50)
    # el_vec = np.linspace(15,25, 50)
    # ec_vec = [0.29]

    # ec_vec = np.linspace(0.01,1, 25) 
    # phi_vec = np.linspace(0,1, 11)
    # phi_vec = np.linspace(0.48, 0.52, 41)
    phi_vec = [0.5]
    # ng_vec = [0.25]

    spec, decays, times, alpha = sweep_params(make_induc_shunt_transmon,
                             (ec_vec, ej_vec, el_vec, phi_vec))

   

    # breakpoint()

    np.save("decays_ist.npy", decays)
    np.save("spec_ist.npy", spec)
    np.save("times_ist.npy", times)
    np.save("alpha_ist.npy", alpha)

    decays = np.load("decays_ist.npy", allow_pickle=True).flatten()[0]
    times = np.load("times_ist.npy", allow_pickle=True)
    spec = np.load("spec_ist.npy", allow_pickle=True)
    alpha = np.load("alpha_ist.npy", allow_pickle=True)

    # ec = ec_vec[indx[0]]

    img_dir = Path(img_dir)
    img_dir.mkdir(exist_ok=True,parents=True)
    for i, phi in enumerate(phi_vec):
        
        indx = (0,i)

        t_1_rate = 0
        for dec_type in ["capacitive", "inductive"]:
            # t_1_rate += np.min(decays['depolarization'][dec_type], axis=(2,3))
            t_1_rate += decays['depolarization'][dec_type][indx[0],:,:, indx[1]]
        t_1 = 1/t_1_rate
        
    
        t_phi_rate = 1
        for dec_type in ["flux", "charge"]:
            # t_phi_rate += np.min(decays['dephasing'][dec_type], axis=(2,3))
            t_phi_rate += decays['dephasing'][dec_type][indx[0],:,:, indx[1]]

        t_phi = 1/t_phi_rate
        
        t_2 = 1/(1/(2*t_1)+1/t_phi)

        # Standardize length of file names
        phi_label = str(np.round(phi,3))
        if len(phi_label) < 5:
            phi_label = phi_label+'0'*(5-len(phi_label))

        make_decay_plots(ej_vec, el_vec, t_1, t_phi, 
        (r"$E_{J}$", r"$E_{L}$"), Path(img_dir,f"ist_decay_phi_{phi_label}.png"))
        make_gate_plots(ej_vec, el_vec, t_2, alpha[indx[0],:,:, indx[1]],
         times[indx[0],:,:, indx[1]],
         (r"$E_{J}$", r"$E_{L}$"), Path(img_dir,f"ist_gates_phi_{phi_label}.png"))


def rhombus_sweep():

    ej1_vec = np.linspace(3,20, 20)
    ej2_vec = np.linspace(3,20, 20)  
    # phi_vec = np.linspace(0,0.5, 10)
    phi_vec = [0.4999]
    ng_vec = [0.25]

    spec, decays, times, alpha = sweep_params(make_rhombus, (ej1_vec, ej2_vec, ng_vec, phi_vec))

    t_1_rate = 0
    for dec_type in ["capacitive"]:#, "inductive"]:
        # t_1_rate += np.min(decays['depolarization'][dec_type], axis=(2,3))
        t_1_rate += decays['depolarization'][dec_type][:,:,-1,-1]
    t_1 = 1/t_1_rate
    


    t_phi_rate = 1
    for dec_type in ["flux", "charge"]:
        # t_phi_rate += np.min(decays['dephasing'][dec_type], axis=(2,3))
        t_phi_rate += decays['dephasing'][dec_type][:,:,-1,-1]

    t_phi = 1/t_phi_rate
    
    t_2 = 1/(1/(2*t_1)+1/t_phi)

    # breakpoint()

    # np.save("decays.npy", decays)
    # np.save("spec.npy", spec)
    # np.save("times.npy", times)
    # np.save("alpha.npy", alpha)
    # decays = np.load("decays.npy", allow_pickle=True).flatten()[0]
    # times = np.load("times.npy", allow_pickle=True)
    # spec = np.load("spec.npy", allow_pickle=True)
    # alpha = np.load("alpha.npy", allow_pickle=True)

    make_decay_plots(ej1_vec, ej2_vec, t_1, t_phi, (r"$E_{J1}$", r"$E_{J2}$"), "rhombus_decay.png")
    make_gate_plots(ej1_vec, ej2_vec, t_2, alpha[:,:,-1,-1], times[:,:,-1,-1],(r"$E_{J1}$", r"$E_{J2}$"), "rhombus_gates.png")


def fluxonium_sweep():

    el_vec = np.linspace(0.1, 1, 100)
    ej_vec = np.linspace(3,20, 100)  
    # phi_vec = np.linspace(0,0.5, 5)
    phi_vec = [0.25]

    spec, decays, times, alpha = sweep_params(make_fluxonium, (ej_vec, el_vec, phi_vec))

    
    t_1_rate = 0
    for dec_type in ["capacitive", "inductive"]:
        # t_1_rate += np.min(decays['depolarization'][dec_type], axis=(2,3))
        t_1_rate += decays['depolarization'][dec_type][:,:,-1]
    t_1 = 1/t_1_rate
    
    t_phi_rate = 1
    for dec_type in ["flux"]:
        # t_phi_rate += np.min(decays['dephasing'][dec_type], axis=(2,3))
        t_phi_rate += decays['dephasing'][dec_type][:,:,-1]

    t_phi = 1/t_phi_rate

    t_2 = 1/(1/(2*t_1)+1/t_phi)
    
    # breakpoint()

    # make_decay_plots(ej_vec, el_vec, t_1, t_phi, (r"$E_j$", r"$E_l$"))
    make_decay_plots(ej_vec, el_vec, t_1, t_phi, (r"$E_J$", r"$E_l$"), "fluxonium_decay.svg")
    make_gate_plots(ej_vec, el_vec, t_2, alpha[:,:,-1], times[:, :, -1],(r"$E_J$", r"$E_l$"), "fluxonium_gates.svg" )



def transmon_sweep():

    # EC is 0.1 -> 1

    Ej_vec = np.linspace(3,20,100)
    Ec_vec = np.linspace(0.1,1,100)  
    ng_vec = [0.25]

    spec, decays, times, alpha = sweep_params(make_transmon, (Ec_vec, Ej_vec, ng_vec))
    t_1 = 1/decays['depolarization']['capacitive'][:,:,0]
    t_phi = 1/decays['dephasing']['charge'][:,:,0]
    t_2 = 1/(1/(2*t_1)+1/t_phi)

    make_decay_plots(Ec_vec, Ej_vec, t_1, t_phi, (r"$E_C$", r"$E_J$"), f"transmon_decay_{ng_vec[0]}.svg")
    make_gate_plots(Ec_vec, Ej_vec, t_2, alpha[:,:,-1], times[:, :, -1],(r"$E_C$", r"$E_J$"), f"transmon_gates_{ng_vec[0]}.svg" )

    
    
    

def zero_pi_sweep(#img_dir = "/home/eweissler/img/ist_sweep/test"
img_dir = "/Users/jlac/img"): 

    ej_vec = np.linspace(3,20, 8)
    #ec_vec = np.linspace(0.01,1, 8) 
    ec_vec = [0.15] 
    el_vec = np.linspace(0.1,1, 8)
    # phi_vec = np.linspace(0,1, 11)
    # phi_vec = np.linspace(0.48, 0.52, 41)
    phi_vec = [0.0]
    # ng_vec = [0.25]

    spec, decays, times, alpha = sweep_params(make_zero_pi,
                             (ec_vec, ej_vec, el_vec, phi_vec))

    # breakpoint()

    np.save("decays_ist.npy", decays)
    np.save("spec_ist.npy", spec)
    np.save("times_ist.npy", times)
    np.save("alpha_ist.npy", alpha)

    decays = np.load("decays_ist.npy", allow_pickle=True).flatten()[0]
    times = np.load("times_ist.npy", allow_pickle=True)
    spec = np.load("spec_ist.npy", allow_pickle=True)
    alpha = np.load("alpha_ist.npy", allow_pickle=True)

    # ec = ec_vec[indx[0]]

    img_dir = Path(img_dir)
    img_dir.mkdir(exist_ok=True,parents=True)
    for i, phi in enumerate(phi_vec):
        
        indx = (0,i)

        t_1_rate = 0
        for dec_type in ["capacitive", "inductive"]:
            # t_1_rate += np.min(decays['depolarization'][dec_type], axis=(2,3))
            t_1_rate += decays['depolarization'][dec_type][indx[0],:,:, indx[1]]
        t_1 = 1/t_1_rate
        
    
        t_phi_rate = 1
        for dec_type in ["flux", "charge"]:
            # t_phi_rate += np.min(decays['dephasing'][dec_type], axis=(2,3))
            t_phi_rate += decays['dephasing'][dec_type][indx[0],:,:, indx[1]]

        t_phi = 1/t_phi_rate
        
        t_2 = 1/(1/(2*t_1)+1/t_phi)

        # Standardize length of file names
        phi_label = str(np.round(phi,3))
        if len(phi_label) < 5:
            phi_label = phi_label+'0'*(5-len(phi_label))

        make_decay_plots(ej_vec, el_vec, t_1, t_phi, 
        (r"$E_{J}$", r"$E_{L}$"), Path(img_dir,f"ist_decay_phi_{phi_label}.png"))
        make_gate_plots(ej_vec, el_vec, t_2, alpha[indx[0],:,:, indx[1]],
         times[indx[0],:,:, indx[1]],
         (r"$E_{J}$", r"$E_{L}$"), Path(img_dir,f"ist_gates_phi_{phi_label}.png"))
    

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

def make_gate_plots(i_vec, j_vec, t_2, alpha, g_times, labels, savename=""):
    """Make plots of gate times, anharmonicity, and number of gates

    Args:
        i_vec (np.array): Row (Y) axis in t_1, t_phi
        j_vec (np.array): Col (X) axis in t_1, t_phi
        t_2 (np.array): array of t2 values in s
        alpha (np.array): array of anharmonicities in 2pi*GHz
        g_times (np.array): array of gate times in s
        labels (tuple): (Row (Y), Col (X)) axis labels for the plots
        savename (str, optional): Place to save the figure if desired. Defaults to "".

    Returns:
        figure, axis
    """



    Y, X = np.meshgrid(i_vec, j_vec, indexing='ij')
    f, ax = plt.subplots(ncols=3)
    f.set_size_inches((25*2,5*2))

    im = ax[0].pcolormesh(X,Y,alpha, cmap='rainbow')
    ax[0].set_xlabel(labels[1], fontsize=16)
    ax[0].set_ylabel(labels[0], fontsize=16)
    ax[0].set_title(r"Anharmonicity $\alpha$ (GHz)", fontsize=16)
    ax[0].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[0])

    im = ax[1].pcolormesh(X,Y,g_times, cmap='rainbow', norm=matplotlib.colors.LogNorm())
    ax[1].set_xlabel(labels[1], fontsize=16)
    ax[1].set_ylabel(labels[0], fontsize=16)
    ax[1].set_title(r"Predicted Gate Time (s)", fontsize=16)
    ax[1].tick_params(labelsize=14)
    f.colorbar(im, ax=ax[1])
    n_gates = t_2/g_times


    im = ax[2].pcolormesh(X,Y,n_gates, cmap='rainbow', norm=matplotlib.colors.LogNorm())
    ax[2].set_xlabel(labels[1], fontsize=16*2)
    ax[2].set_ylabel(labels[0], fontsize=16*2)
    ax[2].set_title(r"Predicted Number of Gates (t2/gate time)", fontsize=16*2)
    ax[2].tick_params(labelsize=14*2)
    f.colorbar(im, ax=ax[2])

    # Find contours at 80% max value
    contours = measure.find_contours(n_gates, 0.5*n_gates.max())
    Ec_interp = sp.interpolate.interp1d(np.arange(j_vec.size), j_vec)
    Ej_interp = sp.interpolate.interp1d(np.arange(i_vec.size), i_vec)

    for contour in contours:
        ax[2].plot(Ec_interp(contour[:, 1]), Ej_interp(contour[:, 0]), linewidth=2, color='k')

    i, j = np.where(n_gates == n_gates.max())
    plt.scatter(Ec_interp(j), Ej_interp(i), c = 'w', marker=(5, 1), s=80)



    if savename != "":
        plt.savefig(savename)

    return f, ax


if __name__ == "__main__":
    transmon_sweep()
    # fluxonium_sweep()
    # rhombus_sweep()
    # induc_shunt_transmon_sweep()
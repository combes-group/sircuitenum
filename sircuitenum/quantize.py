from sircuitenum import utils

import sympy as sym
import numpy as np

PERIODIC_CHARGE = "n"
PERIODIC_PHASE = "θ"
EXTENDED_CHARGE = "q"
EXTENDED_PHASE = "φ"
NODE_CHARGE = "q"
NODE_PHASE = "ϕ"
EXT_CHARGE = "n_g"
EXT_PHASE = "_{ext}"


def gen_cap_mat(circuit, edges):
    """
    Generates a capacitance matrix using Sympy for the given circuit.
    Energy C = Q_vec @ ind_mat @ Q_vec

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        sym.Matrix of the capacitance matrix
    """

    # Generate a blank matrix
    n_nodes = utils.get_num_nodes(edges)
    cap_mat = sym.Matrix(np.zeros((n_nodes, n_nodes)))

    C = {}
    CJ = {}
    for elems in circuit:
        for elem in elems:
            if elem in C or elem in CJ:
                continue
            if "C" in elem:
                C[elem] = sym.Symbol(elem, positive=True, real=True)
            elif "J" in elem:
                suffix = elem.replace("J", "")
                CJ[elem] = sym.Symbol("C_{J" + suffix + "}", positive=True, real=True)

    # Fill in capacitance values
    for edge, elems in zip(edges, circuit):
        i, j = edge
        val = 0
        for elem in elems:
            if "C" in elem:
                val += C[elem]
            elif "J" in elem:
                val += CJ[elem]

        cap_mat[i, i] += val
        cap_mat[j, j] += val
        cap_mat[i, j] += -val
        cap_mat[j, i] += -val

    return cap_mat


def gen_ind_mat(circuit, edges):
    """
    Generates an inductor matrix using Sympy for the given circuit. 
    Defined so Energy L = Phi_vec @ ind_mat @ Phi_vec

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]

    Returns:
        sym.Matrix of the capacitance matrix
    """

    # Generate a blank matrix
    n_nodes = utils.get_num_nodes(edges)
    ind_mat = sym.Matrix(np.zeros((n_nodes, n_nodes)))

    L = {}
    for elems in circuit:
        for elem in elems:
            if elem in L:
                continue
            if "L" in elem:
                L[elem] = sym.Symbol(elem, positive=True, real=True)

    # Fill in inductance values
    for edge, elems in zip(edges, circuit):
        i, j = edge
        val = 0
        for elem in elems:
            if "L" in elem:
                val += 1/L[elem]
        ind_mat[i, i] += val
        ind_mat[j, j] += val
        ind_mat[i, j] += -val
        ind_mat[j, i] += -val

    return ind_mat


def gen_junc_pot(circuit, edges, flux_vars, cob=None):
    """
    Generates the junction potential terms, optionally doing a change of
    basis.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        flux_vars (sym.matrix): a vector of flux variables.
        cob (sym.Matrix): a change of basis matrix to transform the node flux
                          variables.

    Returns:
        sym.Matrix of the capacitance matrix
    """

    n_nodes = utils.get_num_nodes(edges)

    EJ = {}
    for elems in circuit:
        for elem in elems:
            if elem in EJ:
                continue
            elif "J" in elem:
                EJ[elem] = sym.Symbol("E_{"+str(elem)+"}", positive=True,
                                      real=True)

    # Add all the junction terms
    j_terms = 0
    for edge, elems in zip(edges, circuit):
        i, j = edge
        val = 0
        for elem in elems:
            if "J" in elem:
                val += -EJ[elem]

        node_vec = np.zeros(n_nodes, dtype=int)
        node_vec[i] = -1
        node_vec[j] = 1
        node_vec = sym.Matrix(node_vec)
        if cob is not None:
            node_vec = sym.transpose(cob)*node_vec

        j_terms += val*sym.cos((sym.transpose(flux_vars)*node_vec)[0])

    return j_terms


def gen_variables(n_nodes, cob, periodic):

    Q_str = ""
    th_str = ""
    for n in range(1, n_nodes+1):
        if cob is None:
            th_str += "\hat{" + NODE_PHASE + "}_{"+str(n)+"}, "
            Q_str += "\hat{" + NODE_CHARGE + "}_{"+str(n)+"}, "
        elif n in periodic:
            th_str += "\hat{" + PERIODIC_PHASE + "}_{"+str(n)+"}, "
            Q_str += "\hat{" + PERIODIC_CHARGE + "}_{"+str(n)+"}, "
        else:
            th_str += "\hat{" + EXTENDED_PHASE + "}_{"+str(n)+"}, "
            Q_str += "\hat{" + EXTENDED_CHARGE + "}_{"+str(n)+"}, "

    Q_vec = sym.Matrix(sym.symbols(Q_str[:-1]))
    th_vec = sym.Matrix(sym.symbols(th_str[:-1]))

    return Q_vec, th_vec


def quantize_circuit(circuit, edges, Cv=None, V=None, cob=None,
                     periodic=[], extended=[], free=[], frozen=[],
                     sigma = [], return_mats=False, return_vars=False,
                     return_H_class: bool = False,
                     return_combos: bool = False,
                     collect_phase: bool = True):
    """
    Performs a symbolic circuit quantization for the given circuit.

    - Periodic variables are represented using \hat{n}/\hat{θ}
    - Extended variables are represented using \hat{q}/\hat{ϕ}
    - Node variables are represented using \hat{q}/\hat{φ}

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        Cv (sym.Matrix, optional): Coupling of nodes in the circuit to
                                   fixed voltage nodes.
        V (sym.Matrix, optional): Fixed voltages.
        cob (sym.Matrix, optional): Change of basis from node variables
                                    to new variables. This is Z of scqubits.
                                    NOTE: if you have new written in terms
                                    of old, this is the inverse of that.
        periodic (list[int], optional): list of mode numbers (indexed from 1)
                                        transformed coord that are periodic.
        extended (list[int], optional): list of mode numbers (indexed from 1)
                                        transformed coord that are extended.
        free (list[int], optional): list of mode numbers (indexed from 1)
                                        transformed coord that are free.
        frozen (list[int], optional): list of mode numbers (indexed from 1)
                                        transformed coord that are frozen.
        return_mats (bool, optional): optionally return the capacitance and
                                        inductance matrices
        return_vars (bool, optional): optionally return the sympy variables
                                      used to construct H
        return_H_class(bool, optional): optionally return the Hamiltonian with
                                        all coefficients removed
        return_combos(bool, optional): optionally return the combination of
                                       variables present
        collect_phase (bool, optional): for speed, don't collect the phase terms.
                                        slightly messier, but faster.

    Returns:
        Hamiltonian or Hamiltonian, Capacitance Matrix, Inductance Matrix
    """
    edges = utils.zero_start_edges(edges)

    n_nodes = utils.get_num_nodes(edges)

    Q_vec, th_vec = gen_variables(n_nodes, cob, periodic)
    

    C_mat = gen_cap_mat(circuit, edges)
    L_mat = gen_ind_mat(circuit, edges)

    # Set zero applied voltage
    if Cv is None:
        Qv = sym.zeros(rows=n_nodes, cols=1)

    if cob is not None:
        C_mat = sym.transpose(cob)*C_mat*cob
        L_mat = sym.transpose(cob)*L_mat*cob
        if Cv is not None:
            if V is None:
                raise ValueError("Provide Voltages for Coupling Cbapacitors")
            Qv = sym.transpose(cob)*Cv*V
    elif Cv is not None:
        Qv = Cv*V

    # J terms shouldn't contain anything from free modes or frozen modes
    J_terms = gen_junc_pot(circuit, edges, th_vec, cob=cob)

    # Remove any marked modes
    C_mat_full = C_mat.copy()
    L_mat_full = L_mat.copy()
    # All modes to remove
    remove_modes = free + frozen + sigma
    if remove_modes:
        # Go in order to make the indexing
        # post deletion straightforward
        n_deleted = 0
        for n in range(n_nodes):
            if n+1 in remove_modes:
                Qv.row_del(n-n_deleted)
                Q_vec.row_del(n-n_deleted)
                th_vec.row_del(n-n_deleted)
                C_mat.row_del(n-n_deleted)
                C_mat.col_del(n-n_deleted)
                L_mat.row_del(n-n_deleted)
                L_mat.col_del(n-n_deleted)
                n_deleted += 1
    try:
        if C_mat.shape[0] == 1:
            C_inv = C_mat.inv()
        else:
            # Check for the weird all 0 issue
            C_inv = sym.inv_quick(C_mat)
            if C_inv == sym.zeros(rows=C_inv.shape[0],
                                  cols=C_inv.shape[1]):
                C_inv = C_mat.inv()
    except Exception as exc:
        print(exc)
        print("circuit:", circuit)
        print("edges:", edges)
        print("C_mat_full:", C_mat_full)
        print("C_mat:", C_mat)
        return C_mat_full, L_mat_full

    # Explicitly subtract out constant terms from coupling
    C_terms = sym.Rational(1, 2)*sym.transpose(Q_vec - Qv)*C_inv*(Q_vec - Qv)
    C_terms += -sym.Rational(1, 2)*sym.transpose(Qv)*C_inv*Qv
    L_terms = sym.Rational(1, 2)*sym.transpose(th_vec)*L_mat*th_vec

    # Combine terms and group terms in H
    H = C_terms[0] + L_terms[0] + J_terms
    H = sym.expand_trig(sym.expand(sym.nsimplify(H)))
    if cob is None:
        H, combos, combosQ = utils.collect_H_terms(H, zero_ext=False,
                                  periodic_charge="n", periodic_phase="θ",
                                  extended_charge="q", extended_phase="ϕ",
                                  collect_phase = collect_phase)
    else:
        H, combos, combosQ = utils.collect_H_terms(H, zero_ext=False,
                                  periodic_charge="n", periodic_phase="θ",
                                  extended_charge="q", extended_phase="φ",
                                  collect_phase = collect_phase)

    to_return = (H,)

    if return_H_class:
        to_return = to_return + (utils.remove_coeff_(H, list(combosQ)+combos),)
    if return_combos:
        to_return = to_return + (list(combosQ)+combos,)
    if return_mats:
        to_return = to_return + (C_mat, L_mat)
    if return_vars:
        to_return = to_return + (Q_vec, th_vec)
    if len(to_return) == 1:
        to_return = to_return[0]

    return to_return
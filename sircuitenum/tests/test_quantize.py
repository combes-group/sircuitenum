import sympy as sym

from sircuitenum import quantize
from sircuitenum import qpackage_interface as pi


def test_gen_cap_mat():

    # Transmon
    edges = [(0, 1)]
    circuit = [("J", "C")]
    obj = pi.to_SCqubits(circuit, edges)
    Z = sym.Matrix(obj.transformation_matrix)

    C = quantize.gen_cap_mat(circuit, edges)
    ans = '\left[\begin{matrix}C + C_{J} & - C - C_{J}\\- C - C_{J} & C + C_{J}\end{matrix}\right]'
    assert sym.latex(C, order="grlex") == ans

    return


def test_gen_junc_pot():

    # Transmon
    edges = [(0, 1)]
    circuit = [("J", "C")]
    obj = pi.to_SCqubits(circuit, edges)
    Z = sym.Matrix(obj.transformation_matrix)

    th_vec = sym.Matrix(sym.symbols("p1, p2"))
    J = quantize.gen_junc_pot(circuit, edges, th_vec)
    ans = '-E_{J}*cos(p1 - p2)'
    assert sym.latex(C, order="grlex") == ans

    J = quantize.gen_junc_pot(circuit, edges, th_vec, cob="Z")
    ans = '-E_{J}*cos(p1)'
    assert sym.latex(C, order="grlex") == ans

    return


def gen_ind_mat():

    # Transmon
    edges = [(0, 1)]
    circuit = [("J", "C")]
    obj = pi.to_SCqubits(circuit, edges)
    Z = sym.Matrix(obj.transformation_matrix)

    L = quantize.gen_ind_mat(circuit, edges)
    ans = '\left[\begin{matrix}0 & 0\\0 & 0\end{matrix}\right]'
    assert sym.latex(L, order="grlex") == ans


    return


def quantize_circuit():
    return
from sircuitenum import optimize as optim


def test_pick_truncation():

    circuit = [('J',), ('J', 'L')]
    edges = [(0, 2), (1, 2)]
    params = [7.412802517160099, 4.879383407260387, 0.6606415539313616, 20.74202294168071, 21.613559736082763, 23.132434123842902, 0.2092362500235012, 0.7460265564772862]
    cir = optim.make_sqc(circuit, edges, params, ground_node=None)

    assert optim.pick_truncation(cir, thresh=1e-06, neig=5, default_flux=50,
                                 default_charge=20, increment_flux=5,
                                 increment_charge=5) == [50, 30]

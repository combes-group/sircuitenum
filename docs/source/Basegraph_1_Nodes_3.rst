3 Nodes, Basegraph 1
====================

.. image:: img/basegraph_3_nodes_i_001.svg

All unique qubits derived from the above base graph are shown below.
Circuits with series linear elements or no no Josephson Junctions are
excluded.

n3_g1_c8
--------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c8
      - 3
      - 1
      - [(‘C’,), (‘J’,), (‘J’,)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c8.svg

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.05 n_{2}^{2} + 80.05 n_{g2}^{2} + 80.0 n_{1} n_{2} + 80.0 n_{1} n_{g2} + 80.0 n_{2} n_{g1} + 80.0 n_{g1} n_{g2} + 160.09 n_{2} n_{g2} + 160.026 n_{1} n_{g1} + \frac{3201.92 n_{2} n_{g2}}{C_{1 2}} + \frac{3200.525 n_{1} n_{g1}}{C_{1 2}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)}\right)

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1)~-~E_{J_{2}}\cos(\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~40.199~~~~~~~~~~~E_{C_{12}}~=~-79.602~~~~~~~~~~~E_{C_{22}}~=~40.199~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c9
--------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c9
      - 3
      - 1
      - [(‘C’,), (‘J’,), (‘L’,)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c9.svg

.. _circuit-hamiltonian-1:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-1:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(20.0 Q_{2}^{2} + 80.0 n_{1}^{2} + 80.0 n_{g1}^{2} + 1.0 C_{1 2} Q_{2}^{2} + 160.0 n_{1} n_{g1} - 80.0 Q_{2} n_{1} - 80.0 Q_{2} n_{g1}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} - 2.0 L_{2 3} θ_{2}^{2}\right)

.. _sqcircuit-1:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~12.71214~~~~~~~~~~~\varphi_{zp_{1}}~=~2.50e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.792~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

.. _circuitq-1:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}} + \frac{0.5 Cp_{12}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}} + \frac{0.5 Cp_{12}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}}\right) + \frac{\left(\Phi_{2} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 Cp_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}}

n3_g1_c10
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c10
      - 3
      - 1
      - [(‘C’,), (‘J’,), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c10.svg

.. _circuit-hamiltonian-2:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-2:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 n_{1}^{2} + 80.0129 n_{g1}^{2} + 160.026 n_{1} n_{g1} + \frac{4.0 C_{2 3} n_{2}^{2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{4.0 C_{2 3} n_{g2}^{2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{3200.525 n_{1} n_{g1}}{C_{1 2}} + \frac{3200.525 n_{1} n_{g1}}{C_{2 3}} + \frac{4.0 C_{2 3} n_{1} n_{2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{4.0 C_{2 3} n_{1} n_{g2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{4.0 C_{2 3} n_{2} n_{g1}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{4.0 C_{2 3} n_{g1} n_{g2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{8.0 C_{2 3} n_{2} n_{g2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{0.2 C_{1 2} C_{2 3} n_{2}^{2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{0.2 C_{1 2} C_{2 3} n_{g2}^{2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}} + \frac{0.4 C_{1 2} C_{2 3} n_{2} n_{g2}}{1.0 + 0.05 C_{1 2} + 0.1 C_{2 3}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)}\right)

.. _sqcircuit-2:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1)~-~E_{J_{2}}\cos(\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~1.561~~~~~~~~~~~E_{C_{12}}~=~-1.553~~~~~~~~~~~E_{C_{22}}~=~0.784~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

.. _circuitq-2:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c11
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c11
      - 3
      - 1
      - [(‘C’,), (‘J’,), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c11.svg

.. _circuit-hamiltonian-3:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-3:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{1.0 C_{2 3} Q_{2}^{2}}{1.0 + 0.05 C_{1 2} + 0.05 C_{2 3}} + \tilde{\infty} C_{1 2} n_{1} n_{g1} + \tilde{\infty} C_{2 3} Q_{2} n_{1} + \tilde{\infty} C_{2 3} Q_{2} n_{g1} + \tilde{\infty} C_{2 3} n_{1} n_{g1} + \frac{0.05 C_{1 2} C_{2 3} Q_{2}^{2}}{1.0 + 0.05 C_{1 2} + 0.05 C_{2 3}} - \frac{2.0 C_{2 3} Q_{2} n_{1}}{1.0 + 0.05 C_{1 2} + 0.05 C_{2 3}} - \frac{2.0 C_{2 3} Q_{2} n_{g1}}{1.0 + 0.05 C_{1 2} + 0.05 C_{2 3}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} - 2.0 L_{2 3} θ_{2}^{2}\right)

.. _sqcircuit-3:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.2587~~~~~~~~~~~\varphi_{zp_{1}}~=~7.85e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.792~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

.. _circuitq-3:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c12
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c12
      - 3
      - 1
      - [(‘C’,), (‘J’,), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c12.svg

.. _circuit-hamiltonian-4:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-4:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 71.11 n_{1}^{2} + 71.11 n_{g1}^{2} + 0.44 C_{1 2} n_{1}^{2} + 0.44 C_{1 2} n_{g1}^{2} + \frac{1537.5 Q_{2}^{2}}{C_{1 2}} + 142.22 n_{1} n_{g1} + \frac{4622.22 n_{1}^{2}}{C_{1 2}} + \frac{4622.22 n_{g1}^{2}}{C_{1 2}} + \frac{156444.44 n_{1}^{2}}{C_{1 2}^{2}} + \frac{156444.44 n_{g1}^{2}}{C_{1 2}^{2}} + \frac{2915555.56 n_{1}^{2}}{C_{1 2}^{3}} + \frac{2915555.56 n_{g1}^{2}}{C_{1 2}^{3}} + \frac{28444444.44 n_{1}^{2}}{C_{1 2}^{4}} + \frac{28444444.44 n_{g1}^{2}}{C_{1 2}^{4}} + \frac{113888888.89 n_{1}^{2}}{C_{1 2}^{5}} + \frac{113888888.89 n_{g1}^{2}}{C_{1 2}^{5}} + 0.89 C_{1 2} n_{1} n_{g1} + \frac{3215.966796875 Q_{2} n_{1}}{C_{1 2}} + \frac{3215.966796875 Q_{2} n_{g1}}{C_{1 2}} + \frac{9244.44 n_{1} n_{g1}}{C_{1 2}} + \frac{312888.89 n_{1} n_{g1}}{C_{1 2}^{2}} + \frac{5831111.11 n_{1} n_{g1}}{C_{1 2}^{3}} + \frac{56888888.89 n_{1} n_{g1}}{C_{1 2}^{4}} + \frac{227555555.56 n_{1} n_{g1}}{C_{1 2}^{5}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-4:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(0.990099\hat{\varphi}_1+\hat{\varphi}_2)~-~E_{J_{2}}\cos(-\hat{\varphi}_1+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~8.96647~~~~~~~~~~~\varphi_{zp_{1}}~=~2.12e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.792~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-4:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c13
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c13
      - 3
      - 1
      - [(‘C’,), (‘J’,), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c13.svg

.. _circuit-hamiltonian-5:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-5:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 n_{1}^{2} + 80.0129 n_{g1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 3.0 C_{2 3} Q_{2} n_{1} + 3.0 C_{2 3} Q_{2} n_{g1} + 0.15625 C_{1 2} C_{2 3} Q_{2}^{2}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-5:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(0.990099\hat{\varphi}_1+\hat{\varphi}_2)~-~E_{J_{2}}\cos(-\hat{\varphi}_1+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.25251~~~~~~~~~~~\varphi_{zp_{1}}~=~7.91e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.792~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-5:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c17
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c17
      - 3
      - 1
      - [(‘C’,), (‘L’,), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c17.svg

.. _circuit-hamiltonian-6:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-6:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(4.0 C_{2 3} n_{1}^{2} + 4.0 C_{2 3} n_{g1}^{2} + \frac{1.0 C_{1 2} Q_{2}^{2}}{1.0 + 0.05 C_{2 3}} + \frac{1.0 C_{2 3} Q_{2}^{2}}{1.0 + 0.05 C_{2 3}} + 8.0 C_{2 3} n_{1} n_{g1} - \frac{0.5 Q_{2} n_{1}}{0.01 + \frac{1}{4 C_{2 3}}} - \frac{0.5 Q_{2} n_{g1}}{0.01 + \frac{1}{4 C_{2 3}}} - 2.0 C_{2 3} Q_{2} n_{1} - 2.0 C_{2 3} Q_{2} n_{g1} + \frac{0.05 C_{1 2} C_{2 3} Q_{2}^{2}}{1.0 + 0.05 C_{2 3}}\right) - \left(J_{2 3} \cos{\left(θ_{1} \right)} - 2.0 L_{1 3} θ_{2}^{2}\right)

.. _sqcircuit-6:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.78442~~~~~~~~~~~\varphi_{zp_{1}}~=~4.70e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.398~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

.. _circuitq-6:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c19
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c19
      - 3
      - 1
      - [(‘C’,), (‘L’,), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c19.svg

.. _circuit-hamiltonian-7:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-7:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(20.0 Q_{1}^{2} + 80.0 Q_{2}^{2} + 1.0 C_{1 2} Q_{1}^{2} - 80.0 Q_{1} Q_{2}\right) + \left(- J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 3} θ_{1}^{2} - 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-7:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~17.91077~~~~~~~~~~~\varphi_{zp_{1}}~=~2.11e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.89331~~~~~~~~~~~\varphi_{zp_{2}}~=~4.74e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-7:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c20
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c20
      - 3
      - 1
      - [(‘C’,), (‘L’,), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c20.svg

.. _circuit-hamiltonian-8:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-8:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(1.0 C_{1 2} Q_{1}^{2} + 1.0 C_{2 3} Q_{1}^{2} + 4.0 C_{2 3} Q_{2}^{2} - 4.0 C_{2 3} Q_{1} Q_{2}\right) + \left(- J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 3} θ_{1}^{2} - 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-8:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~2.03933~~~~~~~~~~~\varphi_{zp_{1}}~=~5.29e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.78068~~~~~~~~~~~\varphi_{zp_{2}}~=~5.32e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-8:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c24
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c24
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘J’), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c24.svg

.. _circuit-hamiltonian-9:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-9:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 n_{1}^{2} + 80.0129 n_{g1}^{2} + 160.026 n_{1} n_{g1} + \frac{3200.525 n_{1} n_{g1}}{C_{1 2}} + \frac{3200.525 n_{1} n_{g1}}{C_{2 3}} + \frac{4.0 C_{1 2} C_{2 3} n_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 2} C_{2 3} n_{g2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{g2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{1} n_{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{1} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{2} n_{g1}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{g1} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{8.0 C_{1 2} C_{2 3} n_{2} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{8.0 C_{1 3} C_{2 3} n_{2} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{0.2 C_{1 2} C_{1 3} C_{2 3} n_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{0.2 C_{1 2} C_{1 3} C_{2 3} n_{g2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}} + \frac{0.4 C_{1 2} C_{1 3} C_{2 3} n_{2} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)}\right)

.. _sqcircuit-9:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1)~-~E_{J_{2}}\cos(\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~0.529~~~~~~~~~~~E_{C_{12}}~=~-0.526~~~~~~~~~~~E_{C_{22}}~=~0.529~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

.. _circuitq-9:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c25
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c25
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘J’), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c25.svg

.. _circuit-hamiltonian-10:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-10:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{1.0 C_{1 2} C_{2 3} Q_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 3} C_{2 3}} + \frac{1.0 C_{1 3} C_{2 3} Q_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 3} C_{2 3}} + \tilde{\infty} C_{1 2} C_{1 3} n_{1} n_{g1} + \tilde{\infty} C_{1 3} C_{2 3} Q_{2} n_{1} + \tilde{\infty} C_{1 3} C_{2 3} Q_{2} n_{g1} + \tilde{\infty} C_{1 3} C_{2 3} n_{1} n_{g1} + \frac{0.05 C_{1 2} C_{1 3} C_{2 3} Q_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 3} C_{2 3}} - \frac{2.0 C_{1 3} C_{2 3} Q_{2} n_{1}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 3} C_{2 3}} - \frac{2.0 C_{1 3} C_{2 3} Q_{2} n_{g1}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.05 C_{1 2} C_{1 3} + 0.05 C_{1 3} C_{2 3}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} - 2.0 L_{2 3} θ_{2}^{2}\right)

.. _sqcircuit-10:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2)  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.03194~~~~~~~~~~~\varphi_{zp_{1}}~=~3.57e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.398~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\end{align*}

.. _circuitq-10:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c26
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c26
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘J’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c26.svg

.. _circuit-hamiltonian-11:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-11:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 n_{1}^{2} + 80.0129 n_{g1}^{2} + 3.0 C_{1 2} Q_{2}^{2} + 3.0 C_{1 3} Q_{2}^{2} + 3.0 C_{1 3} Q_{2} n_{1} + 3.0 C_{1 3} Q_{2} n_{g1} + 0.15625 C_{1 2} C_{1 3} Q_{2}^{2}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-11:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(0.497512\hat{\varphi}_1+\hat{\varphi}_2)~-~E_{J_{2}}\cos(-\hat{\varphi}_1+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.76693~~~~~~~~~~~\varphi_{zp_{1}}~=~9.40e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.398~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-11:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c27
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c27
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘J’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c27.svg

.. _circuit-hamiltonian-12:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-12:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 n_{1}^{2} + 80.0129 n_{g1}^{2} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2} n_{1}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2} n_{g1}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) - \left(J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left(θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-12:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(0.497512\hat{\varphi}_1+\hat{\varphi}_2)~-~E_{J_{2}}\cos(-\hat{\varphi}_1+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.02852~~~~~~~~~~~\varphi_{zp_{1}}~=~7.17e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.398~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-12:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c33
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c33
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c33.svg

.. _circuit-hamiltonian-13:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-13:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(1.0 C_{1 3} Q_{1}^{2} + 4.1875 C_{1 2} Q_{2}^{2} + 4.1875 C_{1 3} Q_{2}^{2} - 4.1875 C_{1 3} Q_{1} Q_{2}\right) + \left(- J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 3} θ_{1}^{2} - 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-13:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~2.02758~~~~~~~~~~~\varphi_{zp_{1}}~=~8.55e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.78134~~~~~~~~~~~\varphi_{zp_{2}}~=~3.30e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-13:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c34
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c34
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c34.svg

.. _circuit-hamiltonian-14:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-14:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.25 C_{1 2} C_{2 3} Q_{2}^{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}} + \frac{0.25 C_{1 3} C_{2 3} Q_{2}^{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}} + \frac{0.03 C_{1 2} C_{1 3} Q_{1}^{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} + \frac{0.03 C_{1 3} C_{2 3} Q_{1}^{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} - \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} - \frac{0.12 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}}\right) + \left(- J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 3} θ_{1}^{2} - 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-14:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.26177~~~~~~~~~~~\varphi_{zp_{1}}~=~5.60e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.72969~~~~~~~~~~~\varphi_{zp_{2}}~=~4.28e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-14:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c40
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c40
      - 3
      - 1
      - [(‘C’,), (‘J’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c40.svg

.. _circuit-hamiltonian-15:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-15:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 71.11 Q_{1}^{2} + 0.44 C_{1 2} Q_{1}^{2} + \frac{1537.5 Q_{2}^{2}}{C_{1 2}} + \frac{4622.22 Q_{1}^{2}}{C_{1 2}} + \frac{156444.44 Q_{1}^{2}}{C_{1 2}^{2}} + \frac{2915555.56 Q_{1}^{2}}{C_{1 2}^{3}} + \frac{28444444.44 Q_{1}^{2}}{C_{1 2}^{4}} + \frac{113888888.89 Q_{1}^{2}}{C_{1 2}^{5}} + \frac{3215.966796875 Q_{1} Q_{2}}{C_{1 2}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-15:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{2}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~12.64905~~~~~~~~~~~\varphi_{zp_{1}}~=~1.78e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.8922~~~~~~~~~~~\varphi_{zp_{2}}~=~4.72e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\varphi_{\text{ext}_{2}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-15:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c41
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c41
      - 3
      - 1
      - [(‘C’,), (‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c41.svg

.. _circuit-hamiltonian-16:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-16:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 Q_{1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 3.0 C_{2 3} Q_{1} Q_{2} + 0.15625 C_{1 2} C_{2 3} Q_{2}^{2}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-16:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+0.618034\hat{\varphi}_2+\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(-0.618034\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{2}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~2.02039~~~~~~~~~~~\varphi_{zp_{1}}~=~8.55e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.78027~~~~~~~~~~~\varphi_{zp_{2}}~=~5.31e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\varphi_{\text{ext}_{2}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-16:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c48
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c48
      - 3
      - 1
      - [(‘C’,), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c48.svg

.. _circuit-hamiltonian-17:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-17:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 Q_{1}^{2} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left(θ_{2} \right)} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-17:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+\varphi_{\text{ext}_{2}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.25863~~~~~~~~~~~\varphi_{zp_{1}}~=~5.61e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.72908~~~~~~~~~~~\varphi_{zp_{2}}~=~4.27e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\varphi_{\text{ext}_{2}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-17:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c57
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c57
      - 3
      - 1
      - [(‘J’,), (‘J’,), (‘J’,)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c57.svg

.. _circuit-hamiltonian-18:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-18:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.33 n_{1}^{2} + 53.33 n_{2}^{2} + 53.33 n_{g1}^{2} + 53.33 n_{g2}^{2} + 53.33 n_{1} n_{2} + 53.33 n_{1} n_{g2} + 53.33 n_{2} n_{g1} + 53.33 n_{g1} n_{g2} + 106.67 n_{1} n_{g1} + 106.67 n_{2} n_{g2}\right) - \left(J_{1 2} \cos{\left(θ_{1} - θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - θ_{2} \right)}\right)

.. _sqcircuit-18:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+0.33\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})~-~E_{J_{3}}\cos(\hat{\varphi}_1-\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~53.333~~~~~~~~~~~E_{C_{12}}~=~53.333~~~~~~~~~~~E_{C_{22}}~=~53.333~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~E_{J_{3}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-18:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c58
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c58
      - 3
      - 1
      - [(‘J’,), (‘J’,), (‘L’,)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c58.svg

.. _circuit-hamiltonian-19:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-19:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 n_{1}^{2} + 80.0 n_{g1}^{2} + 160.0 Q_{2}^{2} + 160.0 Q_{2} n_{1} + 160.0 Q_{2} n_{g1} + 160.0 n_{1} n_{g1}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-19:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+0.5\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_1+\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~17.88837~~~~~~~~~~~\varphi_{zp_{1}}~=~1.50e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~40.0~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-19:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}} + \frac{0.5 Cp_{12}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}} + \frac{0.5 Cp_{12}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 Cp_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} Cp_{12} + C_{02} Cp_{12}}

n3_g1_c59
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c59
      - 3
      - 1
      - [(‘J’,), (‘J’,), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c59.svg

.. _circuit-hamiltonian-20:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-20:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 n_{1}^{2} + 53.3349 n_{g1}^{2} + 6.40625 C_{2 3} n_{2}^{2} + 6.40625 C_{2 3} n_{g2}^{2} + 26.6675 n_{1} n_{2} + 26.6675 n_{1} n_{g2} + 26.6675 n_{2} n_{g1} + 26.6675 n_{g1} n_{g2} + 106.6698 n_{1} n_{g1} + 2.0 C_{2 3} n_{1} n_{2} + 2.0 C_{2 3} n_{1} n_{g2} + 2.0 C_{2 3} n_{2} n_{g1} + 2.0 C_{2 3} n_{g1} n_{g2} + 8.0 C_{2 3} n_{2} n_{g2} + \frac{1066.6984 n_{1} n_{g1}}{C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - θ_{2} \right)}\right)

.. _sqcircuit-20:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+0.33\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})~-~E_{J_{3}}\cos(\hat{\varphi}_1-\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~40.197~~~~~~~~~~~E_{C_{12}}~=~79.606~~~~~~~~~~~E_{C_{22}}~=~40.197~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~E_{J_{3}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-20:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c60
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c60
      - 3
      - 1
      - [(‘J’,), (‘J’,), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c60.svg

.. _circuit-hamiltonian-21:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-21:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(79.9975 n_{1}^{2} + 79.9975 n_{g1}^{2} + 6.40625 C_{2 3} Q_{2}^{2} + 79.9975 Q_{2} n_{1} + 79.9975 Q_{2} n_{g1} + 159.995 n_{1} n_{g1} + 2.0 C_{2 3} Q_{2} n_{1} + 2.0 C_{2 3} Q_{2} n_{g1} + \frac{3199.9 n_{1} n_{g1}}{C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-21:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+0.5\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_1+\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.26176~~~~~~~~~~~\varphi_{zp_{1}}~=~3.97e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~40.0~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-21:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c61
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c61
      - 3
      - 1
      - [(‘J’,), (‘J’,), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c61.svg

.. _circuit-hamiltonian-22:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-22:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.33 Q_{2}^{2} + 53.33 n_{1}^{2} + 53.33 n_{g1}^{2} + 53.33 Q_{2} n_{1} + 53.33 Q_{2} n_{g1} + 106.67 n_{1} n_{g1}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{2})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-22:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-22:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c62
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c62
      - 3
      - 1
      - [(‘J’,), (‘J’,), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c62.svg

.. _circuit-hamiltonian-23:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-23:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 n_{1}^{2} + 53.3349 n_{g1}^{2} + 6.40625 C_{2 3} Q_{2}^{2} + 26.6675 Q_{2} n_{1} + 26.6675 Q_{2} n_{g1} + 106.6698 n_{1} n_{g1} + 2.0 C_{2 3} Q_{2} n_{1} + 2.0 C_{2 3} Q_{2} n_{g1} + \frac{1066.6984 n_{1} n_{g1}}{C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{2})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-23:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-23:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c66
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c66
      - 3
      - 1
      - [(‘J’,), (‘L’,), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c66.svg

.. _circuit-hamiltonian-24:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-24:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(160.0 Q_{2}^{2} + 80.0 Q_{2} n_{1} + 80.0 Q_{2} n_{g1} + \frac{1537.5 Q_{2}^{2}}{C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{1} \right)} - 0.5 L_{1 3} θ_{2}^{2}\right)

.. _sqcircuit-24:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+0.5\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(0.009901\hat{\varphi}_1+\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~12.71151~~~~~~~~~~~\varphi_{zp_{1}}~=~2.50e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.784~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-24:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c67
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c67
      - 3
      - 1
      - [(‘J’,), (‘L’,), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c67.svg

.. _circuit-hamiltonian-25:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-25:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 1.0 C_{2 3} Q_{1}^{2}\right) + \left(- J_{1 2} \cos{\left(θ_{2} \right)} + 0.5 L_{1 3} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{2 3} θ_{1}^{2} + 2.0 L_{1 3} θ_{1} θ_{2} - 2.0 (2πΦ_{1}) L_{2 3} θ_{1}\right)

.. _sqcircuit-25:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1-\hat{\varphi}_2+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~12.71277~~~~~~~~~~~\varphi_{zp_{1}}~=~2.50e+00 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~1.25857~~~~~~~~~~~\varphi_{zp_{2}}~=~8.01e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-25:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c68
---------

.. list-table::
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c68
      - 3
      - 1
      - [(‘J’,), (‘L’,), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c68.svg

.. _circuit-hamiltonian-26:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-26:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 160.0 Q_{1}^{2} + 160.0 Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-26:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-26:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c69
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c69
      - 3
      - 1
      - [(‘J’,), (‘L’,), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c69.svg

.. _circuit-hamiltonian-27:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-27:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(160.026 Q_{1}^{2} + 80.0129 Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-27:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-27:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 Cp_{02}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}} + \frac{0.5 C_{12}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{12} + C_{01} Cp_{02} + C_{12} Cp_{02}}

n3_g1_c73
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c73
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘J’), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c73.svg

.. _circuit-hamiltonian-28:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-28:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.335 n_{1}^{2} + 53.335 n_{g1}^{2} + 26.6674 n_{1} n_{2} + 26.6674 n_{1} n_{g2} + 26.6674 n_{2} n_{g1} + 26.6674 n_{g1} n_{g2} + 106.67 n_{1} n_{g1} + \frac{4.0 C_{2 3} n_{2}^{2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{4.0 C_{2 3} n_{g2}^{2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{1066.7 n_{1} n_{g1}}{C_{2 3}} + \frac{8.0 C_{2 3} n_{2} n_{g2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.4 C_{1 3} C_{2 3} n_{2}^{2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.4 C_{1 3} C_{2 3} n_{g2}^{2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.2 C_{1 3} C_{2 3} n_{1} n_{2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.2 C_{1 3} C_{2 3} n_{1} n_{g2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.2 C_{1 3} C_{2 3} n_{2} n_{g1}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.2 C_{1 3} C_{2 3} n_{g1} n_{g2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}} + \frac{0.8 C_{1 3} C_{2 3} n_{2} n_{g2}}{1.0 + 0.1 C_{1 3} + 0.1 C_{2 3} + 0.01 C_{1 3} C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - θ_{2} \right)}\right)

.. _sqcircuit-28:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+0.33\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})~-~E_{J_{3}}\cos(\hat{\varphi}_1-\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~1.553~~~~~~~~~~~E_{C_{12}}~=~1.553~~~~~~~~~~~E_{C_{22}}~=~0.784~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~E_{J_{3}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-28:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c74
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c74
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘J’), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c74.svg

.. _circuit-hamiltonian-29:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-29:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 n_{1}^{2} + 80.0129 n_{g1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 80.0129 Q_{2} n_{1} + 80.0129 Q_{2} n_{g1} + 0.3125 C_{1 3} C_{2 3} Q_{2}^{2} + 0.15625 C_{1 3} C_{2 3} Q_{2} n_{1} + 0.15625 C_{1 3} C_{2 3} Q_{2} n_{g1}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-29:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+0.5\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(0.009901\hat{\varphi}_1+\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.2587~~~~~~~~~~~\varphi_{zp_{1}}~=~7.86e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.784~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-29:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c75
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c75
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘J’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c75.svg

.. _circuit-hamiltonian-30:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-30:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.333334 Q_{2}^{2} + \frac{512.5 Q_{2}^{2}}{C_{1 3}} + 26.666667 Q_{2} n_{1} + 26.666667 Q_{2} n_{g1} + 8.00002 C_{1 3} n_{1} n_{g1} + 2.0 C_{1 3} Q_{2} n_{1} + 2.0 C_{1 3} Q_{2} n_{g1}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{2})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-30:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-30:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c76
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c76
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘J’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c76.svg

.. _circuit-hamiltonian-31:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-31:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.335 n_{1}^{2} + 53.335 n_{g1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 26.6674 Q_{2} n_{1} + 26.6674 Q_{2} n_{g1} + 106.67 n_{1} n_{g1} + 0.3125 C_{1 3} C_{2 3} Q_{2}^{2} + \frac{1066.7 n_{1} n_{g1}}{C_{2 3}} + 0.15625 C_{1 3} C_{2 3} Q_{2} n_{1} + 0.15625 C_{1 3} C_{2 3} Q_{2} n_{g1}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{2})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-31:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-31:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c81
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c81
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘L’), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c81.svg

.. _circuit-hamiltonian-32:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-32:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(1.0 C_{2 3} Q_{1}^{2} + 4.1875 C_{1 3} Q_{2}^{2} + 4.1875 C_{2 3} Q_{2}^{2} - 4.1875 C_{2 3} Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{2} \right)} + 0.5 L_{1 3} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{2 3} θ_{1}^{2} + 2.0 L_{1 3} θ_{1} θ_{2} - 2.0 (2πΦ_{1}) L_{2 3} θ_{1}\right)

.. _sqcircuit-32:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.25245~~~~~~~~~~~\varphi_{zp_{1}}~=~1.12e+00  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-32:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c82
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c82
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c82.svg

.. _circuit-hamiltonian-33:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-33:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 80.0 Q_{1} Q_{2} + \frac{1537.5 Q_{2}^{2}}{C_{1 3}} + 2.0 C_{1 3} Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-33:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-33:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c83
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c83
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c83.svg

.. _circuit-hamiltonian-34:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-34:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(3.0 C_{2 3} Q_{2}^{2} + 80.0129 Q_{1} Q_{2} + 0.15625 C_{1 3} C_{2 3} Q_{2}^{2} + 0.15625 C_{1 3} C_{2 3} Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-34:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-34:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c89
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c89
      - 3
      - 1
      - [(‘J’,), (‘J’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c89.svg

.. _circuit-hamiltonian-35:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-35:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.33 Q_{1}^{2} + 53.33 Q_{2}^{2} + 53.33 Q_{1} Q_{2}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} - 0.5 L_{1 3} (2πΦ_{1})^{2} - 0.5 L_{1 3} θ_{1}^{2} - 0.5 L_{2 3} (2πΦ_{3})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 3} θ_{1} + 1.0 (2πΦ_{3}) L_{2 3} θ_{2}\right)

.. _sqcircuit-35:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-35:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c90
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c90
      - 3
      - 1
      - [(‘J’,), (‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c90.svg

.. _circuit-hamiltonian-36:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-36:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 Q_{1}^{2} + 6.40625 C_{2 3} Q_{2}^{2} + 26.6675 Q_{1} Q_{2} + 2.0 C_{2 3} Q_{1} Q_{2}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} - 0.5 L_{1 3} (2πΦ_{1})^{2} - 0.5 L_{1 3} θ_{1}^{2} - 0.5 L_{2 3} (2πΦ_{3})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 3} θ_{1} + 1.0 (2πΦ_{3}) L_{2 3} θ_{2}\right)

.. _sqcircuit-36:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-36:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c97
---------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c97
      - 3
      - 1
      - [(‘J’,), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c97.svg

.. _circuit-hamiltonian-37:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-37:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.335 Q_{1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 26.6674 Q_{1} Q_{2} + 0.3125 C_{1 3} C_{2 3} Q_{2}^{2} + 0.15625 C_{1 3} C_{2 3} Q_{1} Q_{2}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} - 0.5 L_{1 3} (2πΦ_{1})^{2} - 0.5 L_{1 3} θ_{1}^{2} - 0.5 L_{2 3} (2πΦ_{3})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 3} θ_{1} + 1.0 (2πΦ_{3}) L_{2 3} θ_{2}\right)

.. _sqcircuit-37:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-37:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c122
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c122
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘J’), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c122.svg

.. _circuit-hamiltonian-38:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-38:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(3.0 C_{1 3} Q_{2}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 80.0 Q_{2} n_{1} + 80.0 Q_{2} n_{g1} + 159.995 n_{1} n_{g1} + 0.3125 C_{1 3} C_{2 3} Q_{2}^{2}\right) - \left(J_{1 3} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) + θ_{1} \right)} - 0.5 L_{1 2} θ_{2}^{2}\right)

.. _sqcircuit-38:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_1-\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.77998~~~~~~~~~~~\varphi_{zp_{1}}~=~4.72e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.396~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-38:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c123
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c123
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘J’), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c123.svg

.. _circuit-hamiltonian-39:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-39:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.5 Q_{2}^{2}}{0.01 + \frac{0.12}{C_{1 3}}} + 1.0 C_{2 3} Q_{1}^{2}\right) + \left(- J_{1 3} \cos{\left(θ_{2} \right)} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 2.0 L_{1 2} θ_{1}^{2} + 2.0 L_{2 3} θ_{1}^{2} + 2.0 (2πΦ_{1}) L_{2 3} θ_{1} + 2.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-39:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~\omega_2\hat a^\dagger_2\hat a_2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2-\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~2.04387~~~~~~~~~~~\varphi_{zp_{1}}~=~3.26e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_2~=~\varphi_{zp_{2}}(\hat a_2+\hat a^\dagger_2)~~~~~~~~~~~\omega_2/2\pi~=~0.77894~~~~~~~~~~~\varphi_{zp_{2}}~=~8.59e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-39:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c124
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c124
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘J’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c124.svg

.. _circuit-hamiltonian-40:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-40:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + \frac{0.5 Q_{1}^{2}}{0.01 + \frac{0.12}{C_{1 3}}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-40:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-40:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c125
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c125
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘J’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c125.svg

.. _circuit-hamiltonian-41:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-41:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.5 Q_{1}^{2}}{0.01 + \frac{0.12}{C_{1 3}}} + \frac{0.5 Q_{2}^{2}}{0.01 + \frac{0.12}{C_{2 3}}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-41:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-41:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c131
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c131
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c131.svg

.. _circuit-hamiltonian-42:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-42:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 1.0 C_{1 3} Q_{1}^{2}\right) + \left(- J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 2} θ_{1}^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{1 2} θ_{1} θ_{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-42:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-42:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c132
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c132
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c132.svg

.. _circuit-hamiltonian-43:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-43:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.5 Q_{2}^{2}}{0.01 + \frac{0.12}{C_{2 3}}} + 1.0 C_{1 3} Q_{1}^{2}\right) + \left(- J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 2} θ_{1}^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{1 2} θ_{1} θ_{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-43:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-43:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c138
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c138
      - 3
      - 1
      - [(‘L’,), (‘J’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c138.svg

.. _circuit-hamiltonian-44:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-44:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{1}^{2} + 80.0 Q_{2}^{2}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{3})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{3}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-44:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-44:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c139
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c139
      - 3
      - 1
      - [(‘L’,), (‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c139.svg

.. _circuit-hamiltonian-45:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-45:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{1}^{2} + \frac{0.5 Q_{2}^{2}}{0.01 + \frac{0.12}{C_{2 3}}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{3})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{3}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-45:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-45:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c146
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c146
      - 3
      - 1
      - [(‘L’,), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c146.svg

.. _circuit-hamiltonian-46:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-46:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.5 Q_{1}^{2}}{0.01 + \frac{0.12}{C_{1 3}}} + \frac{0.5 Q_{2}^{2}}{0.01 + \frac{0.12}{C_{2 3}}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{3})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{3}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-46:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-46:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{12}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}} + \frac{0.5 Cp_{01}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{02} C_{12} + C_{02} Cp_{01} + C_{12} Cp_{01}}

n3_g1_c171
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c171
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘J’), (‘C’, ‘J’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c171.svg

.. _circuit-hamiltonian-47:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-47:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 n_{1}^{2} + 53.3349 n_{g1}^{2} + 26.6675 n_{1} n_{2} + 26.6675 n_{1} n_{g2} + 26.6675 n_{2} n_{g1} + 26.6675 n_{g1} n_{g2} + 106.6698 n_{1} n_{g1} + \frac{1066.6984 n_{1} n_{g1}}{C_{1 2}} + \frac{1066.6984 n_{1} n_{g1}}{C_{2 3}} + \frac{4.0 C_{1 2} C_{2 3} n_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 2} C_{2 3} n_{g2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{g2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{1} n_{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{1} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{2} n_{g1}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{4.0 C_{1 3} C_{2 3} n_{g1} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{8.0 C_{1 2} C_{2 3} n_{2} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{8.0 C_{1 3} C_{2 3} n_{2} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.4 C_{1 2} C_{1 3} C_{2 3} n_{2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.4 C_{1 2} C_{1 3} C_{2 3} n_{g2}^{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.2 C_{1 2} C_{1 3} C_{2 3} n_{1} n_{2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.2 C_{1 2} C_{1 3} C_{2 3} n_{1} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.2 C_{1 2} C_{1 3} C_{2 3} n_{2} n_{g1}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.2 C_{1 2} C_{1 3} C_{2 3} n_{g1} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}} + \frac{0.8 C_{1 2} C_{1 3} C_{2 3} n_{2} n_{g2}}{1.0 C_{1 2} + 1.0 C_{1 3} + 1.0 C_{2 3} + 0.1 C_{1 2} C_{1 3} + 0.1 C_{1 2} C_{2 3} + 0.1 C_{1 3} C_{2 3} + 0.01 C_{1 2} C_{1 3} C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - θ_{2} \right)}\right)

.. _sqcircuit-47:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~+~E_{C_{12}}(\hat{n}_1-n_{g_{1}})(\hat{n}_2-n_{g_{2}})~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1+0.33\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})~-~E_{J_{3}}\cos(\hat{\varphi}_1-\hat{\varphi}_2-0.33\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{1}}~=~0 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{11}}~=~0.528~~~~~~~~~~~E_{C_{12}}~=~0.528~~~~~~~~~~~E_{C_{22}}~=~0.528~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~E_{J_{3}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-47:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c172
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c172
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘J’), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c172.svg

.. _circuit-hamiltonian-48:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-48:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(159.995 n_{1} n_{g1} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.01 C_{1 2} C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2} n_{1}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2} n_{g1}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} - 0.5 L_{2 3} (2πΦ_{1})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{2 3} θ_{2}\right)

.. _sqcircuit-48:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~+~E_{C_{22}}(\hat{n}_2-n_{g_{2}})^2~~-~E_{J_{1}}\cos(-\hat{\varphi}_1+\hat{\varphi}_2+0.5\varphi_{\text{ext}_{1}})~-~E_{J_{2}}\cos(\hat{\varphi}_1+\hat{\varphi}_2-0.5\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~1.03108~~~~~~~~~~~\varphi_{zp_{1}}~=~3.59e-01 \\ &\text{mode}~2:~~~~~~~~~~~\text{charge}~~~~~~~~~~~~~~~~n_{g_{2}}~=~0  \\ &\text{parameters}:~~~~~~~~~~~E_{C_{22}}~=~0.396~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~E_{J_{2}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-48:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c173
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c173
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘J’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c173.svg

.. _circuit-hamiltonian-49:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-49:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 n_{1}^{2} + 53.3349 n_{g1}^{2} + 3.0 C_{1 2} Q_{2}^{2} + 3.0 C_{1 3} Q_{2}^{2} + 26.6675 Q_{2} n_{1} + 26.6675 Q_{2} n_{g1} + 106.6698 n_{1} n_{g1} + 3.0 C_{1 3} Q_{2} n_{1} + 3.0 C_{1 3} Q_{2} n_{g1} + 0.3125 C_{1 2} C_{1 3} Q_{2}^{2} + 0.15625 C_{1 2} C_{1 3} Q_{2} n_{1} + 0.15625 C_{1 2} C_{1 3} Q_{2} n_{g1}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{2})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-49:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-49:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c174
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c174
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘J’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c174.svg

.. _circuit-hamiltonian-50:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-50:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 n_{1}^{2} + 53.3349 n_{g1}^{2} + 26.6675 Q_{2} n_{1} + 26.6675 Q_{2} n_{g1} + 106.6698 n_{1} n_{g1} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.01 C_{1 2} C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2} n_{1}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2} n_{g1}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} - 0.5 L_{2 3} (2πΦ_{2})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-50:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-50:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c179
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c179
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘L’), (‘C’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c179.svg

.. _circuit-hamiltonian-51:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-51:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.25 C_{1 2} C_{1 3} Q_{2}^{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}} + \frac{0.25 C_{1 2} C_{2 3} Q_{2}^{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}} + \frac{0.03 C_{1 2} C_{2 3} Q_{1}^{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} + \frac{0.03 C_{1 3} C_{2 3} Q_{1}^{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} - \frac{0.06 C_{1 2} C_{2 3} Q_{1} Q_{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} - \frac{0.12 C_{1 2} C_{2 3} Q_{1} Q_{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}}\right) + \left(- J_{1 2} \cos{\left(θ_{2} \right)} + 0.5 L_{1 3} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{1})^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{2 3} θ_{1}^{2} + 2.0 L_{1 3} θ_{1} θ_{2} - 2.0 (2πΦ_{1}) L_{2 3} θ_{1}\right)

.. _sqcircuit-51:

SQcircuit:
^^^^^^^^^^

.. math:: \begin{align*} &\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\varphi_{\text{ext}_{1}})  \\ &\text{mode}~1:~~~~~~~~~~~\text{harmonic}~~~~~~~~~~~\hat{\varphi}_1~=~\varphi_{zp_{1}}(\hat a_1+\hat a^\dagger_1)~~~~~~~~~~~\omega_1/2\pi~=~0.72787~~~~~~~~~~~\varphi_{zp_{1}}~=~8.53e-01  \\ &\text{parameters}:~~~~~~~~~~~E_{J_{1}}~=~5.0~~~~~~~~~~~ \\ &\text{loops}:~~~~~~~~~~~~~~~~~~~~\varphi_{\text{ext}_{1}}/2\pi~=~0.0~~~~~~~~~~~\end{align*}

.. _circuitq-51:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c180
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c180
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c180.svg

.. _circuit-hamiltonian-52:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-52:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(3.0 C_{1 2} Q_{2}^{2} + 3.0 C_{1 3} Q_{2}^{2} + 80.0129 Q_{1} Q_{2} + 3.0 C_{1 3} Q_{1} Q_{2} + 0.15625 C_{1 2} C_{1 3} Q_{2}^{2} + 0.15625 C_{1 2} C_{1 3} Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-52:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-52:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c181
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c181
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c181.svg

.. _circuit-hamiltonian-53:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-53:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 Q_{1} Q_{2} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-53:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-53:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c187
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c187
      - 3
      - 1
      - [(‘C’, ‘J’), (‘J’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c187.svg

.. _circuit-hamiltonian-54:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-54:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(50.79 Q_{1}^{2} + 53.333334 Q_{2}^{2} + 0.76 C_{1 2} Q_{1}^{2} + \frac{512.5 Q_{2}^{2}}{C_{1 2}} + \frac{1405.29 Q_{1}^{2}}{C_{1 2}} + \frac{20656.08 Q_{1}^{2}}{C_{1 2}^{2}} + \frac{170158.73 Q_{1}^{2}}{C_{1 2}^{3}} + \frac{744973.54 Q_{1}^{2}}{C_{1 2}^{4}} + \frac{1355820.11 Q_{1}^{2}}{C_{1 2}^{5}} + 55.8730159822911 Q_{1} Q_{2} + 0.38 C_{1 2} Q_{1} Q_{2} + \frac{15195.77 Q_{1} Q_{2}}{C_{1 2}^{2}} + \frac{677248.68 Q_{1} Q_{2}}{C_{1 2}^{4}} + \frac{139682.54 Q_{1} Q_{2}}{C_{1 2}^{3}} + \frac{1355820.11 Q_{1} Q_{2}}{C_{1 2}^{5}} + \frac{1431.01851851852 Q_{1} Q_{2}}{C_{1 2}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} - 0.5 L_{1 3} (2πΦ_{1})^{2} - 0.5 L_{1 3} θ_{1}^{2} - 0.5 L_{2 3} (2πΦ_{3})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 3} θ_{1} + 1.0 (2πΦ_{3}) L_{2 3} θ_{2}\right)

.. _sqcircuit-54:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-54:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c188
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c188
      - 3
      - 1
      - [(‘C’, ‘J’), (‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c188.svg

.. _circuit-hamiltonian-55:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-55:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 Q_{1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 26.6675 Q_{1} Q_{2} + 3.0 C_{2 3} Q_{1} Q_{2} + 0.3125 C_{1 2} C_{2 3} Q_{2}^{2} + 0.15625 C_{1 2} C_{2 3} Q_{1} Q_{2}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} - 0.5 L_{1 3} (2πΦ_{1})^{2} - 0.5 L_{1 3} θ_{1}^{2} - 0.5 L_{2 3} (2πΦ_{3})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 3} θ_{1} + 1.0 (2πΦ_{3}) L_{2 3} θ_{2}\right)

.. _sqcircuit-55:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-55:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c195
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c195
      - 3
      - 1
      - [(‘C’, ‘J’), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c195.svg

.. _circuit-hamiltonian-56:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-56:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 Q_{1}^{2} + 26.6675 Q_{1} Q_{2} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.01 C_{1 2} C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) - \left(J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} + J_{1 3} \cos{\left(θ_{1} \right)} + J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} - 0.5 L_{1 3} (2πΦ_{1})^{2} - 0.5 L_{1 3} θ_{1}^{2} - 0.5 L_{2 3} (2πΦ_{3})^{2} - 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 3} θ_{1} + 1.0 (2πΦ_{3}) L_{2 3} θ_{2}\right)

.. _sqcircuit-56:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-56:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c229
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c229
      - 3
      - 1
      - [(‘C’, ‘L’), (‘C’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c229.svg

.. _circuit-hamiltonian-57:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-57:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(1.0 C_{1 3} Q_{1}^{2} + 4.1875 C_{1 2} Q_{2}^{2} + 4.1875 C_{1 3} Q_{2}^{2} - 4.1875 C_{1 3} Q_{1} Q_{2}\right) + \left(- J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 2} θ_{1}^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{1 2} θ_{1} θ_{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-57:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-57:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c230
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c230
      - 3
      - 1
      - [(‘C’, ‘L’), (‘C’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c230.svg

.. _circuit-hamiltonian-58:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-58:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(\frac{0.25 C_{1 2} C_{2 3} Q_{2}^{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}} + \frac{0.25 C_{1 3} C_{2 3} Q_{2}^{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}} + \frac{0.03 C_{1 2} C_{1 3} Q_{1}^{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} + \frac{0.03 C_{1 3} C_{2 3} Q_{1}^{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} - \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.03 C_{1 2} + 0.03 C_{1 3} + 0.03 C_{2 3}} - \frac{0.12 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.06 C_{1 2} + 0.06 C_{1 3} + 0.06 C_{2 3}}\right) + \left(- J_{2 3} \cos{\left((2πΦ_{1}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{2 3} (2πΦ_{2})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 2.0 L_{1 2} θ_{1}^{2} + 2.0 L_{1 3} θ_{1}^{2} + 2.0 L_{1 2} θ_{1} θ_{2} - 1.0 (2πΦ_{2}) L_{2 3} θ_{2}\right)

.. _sqcircuit-58:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-58:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\Phi_{2}^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c236
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c236
      - 3
      - 1
      - [(‘C’, ‘L’), (‘J’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c236.svg

.. _circuit-hamiltonian-59:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-59:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0 Q_{2}^{2} + 71.11 Q_{1}^{2} + 0.44 C_{1 2} Q_{1}^{2} + \frac{1537.5 Q_{2}^{2}}{C_{1 2}} + \frac{4622.22 Q_{1}^{2}}{C_{1 2}} + \frac{156444.44 Q_{1}^{2}}{C_{1 2}^{2}} + \frac{2915555.56 Q_{1}^{2}}{C_{1 2}^{3}} + \frac{28444444.44 Q_{1}^{2}}{C_{1 2}^{4}} + \frac{113888888.89 Q_{1}^{2}}{C_{1 2}^{5}} + \frac{3215.966796875 Q_{1} Q_{2}}{C_{1 2}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{3})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{3}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-59:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-59:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c237
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c237
      - 3
      - 1
      - [(‘C’, ‘L’), (‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c237.svg

.. _circuit-hamiltonian-60:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-60:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 Q_{1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 3.0 C_{2 3} Q_{1} Q_{2} + 0.15625 C_{1 2} C_{2 3} Q_{2}^{2}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{3})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{3}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-60:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-60:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c244
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c244
      - 3
      - 1
      - [(‘C’, ‘L’), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c244.svg

.. _circuit-hamiltonian-61:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-61:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(80.0129 Q_{1}^{2} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) + \left(- J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{2}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{1})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{3})^{2} + 0.5 L_{2 3} θ_{2}^{2} - 1.0 (2πΦ_{1}) L_{1 3} θ_{1} - 1.0 (2πΦ_{3}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-61:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-61:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\Phi_{1}^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c285
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c285
      - 3
      - 1
      - [(‘J’, ‘L’), (‘J’, ‘L’), (‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c285.svg

.. _circuit-hamiltonian-62:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-62:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.33 Q_{1}^{2} + 53.33 Q_{2}^{2} + 53.33 Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{3}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} (2πΦ_{1})^{2} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{2})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{4})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 2} θ_{2} - 1.0 (2πΦ_{1}) L_{1 2} θ_{1} - 1.0 (2πΦ_{2}) L_{1 3} θ_{1} - 1.0 (2πΦ_{4}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-62:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-62:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{1} + \tilde{\Phi}_{010}\right)^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c286
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c286
      - 3
      - 1
      - [(‘J’, ‘L’), (‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c286.svg

.. _circuit-hamiltonian-63:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-63:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 Q_{1}^{2} + 6.40625 C_{2 3} Q_{2}^{2} + 26.6675 Q_{1} Q_{2} + 2.0 C_{2 3} Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{3}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} (2πΦ_{1})^{2} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{2})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{4})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 2} θ_{2} - 1.0 (2πΦ_{1}) L_{1 2} θ_{1} - 1.0 (2πΦ_{2}) L_{1 3} θ_{1} - 1.0 (2πΦ_{4}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-63:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-63:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{1} + \tilde{\Phi}_{010}\right)^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c293
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c293
      - 3
      - 1
      - [(‘J’, ‘L’), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c293.svg

.. _circuit-hamiltonian-64:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-64:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.335 Q_{1}^{2} + 3.0 C_{2 3} Q_{2}^{2} + 26.6674 Q_{1} Q_{2} + 0.3125 C_{1 3} C_{2 3} Q_{2}^{2} + 0.15625 C_{1 3} C_{2 3} Q_{1} Q_{2}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{3}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} (2πΦ_{1})^{2} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{2})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{4})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 2} θ_{2} - 1.0 (2πΦ_{1}) L_{1 2} θ_{1} - 1.0 (2πΦ_{2}) L_{1 3} θ_{1} - 1.0 (2πΦ_{4}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-64:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-64:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{1} + \tilde{\Phi}_{010}\right)^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

n3_g1_c342
----------

.. list-table::
   :widths: 18 13 20 13 9
   :header-rows: 1

   - 

      - unique_key
      - n_nodes
      - graph_index
      - circuit
      - edges
   - 

      - n3_g1_c342
      - 3
      - 1
      - [(‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’), (‘C’, ‘J’, ‘L’)]
      - [(0, 1), (0, 2), (1, 2)]

Notes:

.. image:: img/n3_g1_c342.svg

.. _circuit-hamiltonian-65:

Circuit Hamiltonian
~~~~~~~~~~~~~~~~~~~

For scQubits and SQcircuit, default numerical values are given as
:math:`E_C = 0.2` GHz, :math:`E_L = 1` GHz, :math:`E_J = 5` GHz, and
:math:`E_{CJ} = 20` GHz.

.. _scqubits-65:

scQubits:
^^^^^^^^^

Nodes index from 1, and are assumed to be connected to a voltage source
via a coupling capacitor.

.. math:: \left(53.3349 Q_{1}^{2} + 26.6675 Q_{1} Q_{2} + \frac{0.06 C_{1 2} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.01 C_{1 2} C_{1 3} C_{2 3} Q_{2}^{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}} + \frac{0.06 C_{1 3} C_{2 3} Q_{1} Q_{2}}{0.02 C_{1 2} + 0.02 C_{1 3} + 0.02 C_{2 3}}\right) + \left(- J_{1 2} \cos{\left(θ_{1} - 1.0 θ_{2} \right)} - J_{1 3} \cos{\left(θ_{1} \right)} - J_{2 3} \cos{\left((2πΦ_{3}) - 1.0 θ_{2} \right)} + 0.5 L_{1 2} (2πΦ_{1})^{2} + 0.5 L_{1 2} θ_{1}^{2} + 0.5 L_{1 2} θ_{2}^{2} + 0.5 L_{1 3} (2πΦ_{2})^{2} + 0.5 L_{1 3} θ_{1}^{2} + 0.5 L_{2 3} (2πΦ_{4})^{2} + 0.5 L_{2 3} θ_{2}^{2} + 1.0 (2πΦ_{1}) L_{1 2} θ_{2} - 1.0 (2πΦ_{1}) L_{1 2} θ_{1} - 1.0 (2πΦ_{2}) L_{1 3} θ_{1} - 1.0 (2πΦ_{4}) L_{2 3} θ_{2} - 1.0 L_{1 2} θ_{1} θ_{2}\right)

.. _sqcircuit-65:

SQcircuit:
^^^^^^^^^^

N/A

.. _circuitq-65:

CircuitQ:
^^^^^^^^^

Nodes index from 0, with node 0 assigned to be ground. Flux biases are
included, but offset charges are ignored.

.. math:: q_{1}^{2} \cdot \left(\frac{0.5 C_{02}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + q_{2}^{2} \cdot \left(\frac{0.5 C_{01}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}} + \frac{0.5 C_{12}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}\right) + \frac{\left(\Phi_{1} + \tilde{\Phi}_{010}\right)^{2}}{2 L_{010}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{020}\right)^{2}}{2 L_{020}} + \frac{\left(\Phi_{2} + \tilde{\Phi}_{120} + \tilde{\Phi}_{121} - \Phi_{1}\right)^{2}}{2 L_{120}} - E_{J010} \cos{\left(\frac{\Phi_{1}}{\Phi_{o}} \right)} - E_{J020} \cos{\left(\frac{\Phi_{2}}{\Phi_{o}} \right)} - E_{J120} \cos{\left(\frac{\Phi_{2} + \tilde{\Phi}_{120} - \Phi_{1}}{\Phi_{o}} \right)} + \frac{1.0 C_{12} q_{1} q_{2}}{C_{01} C_{02} + C_{01} C_{12} + C_{02} C_{12}}

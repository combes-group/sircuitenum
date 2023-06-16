2 Node Circuits
===============

.. list-table::
   :widths: 17 20 22 12
   :header-rows: 1

   - 

      - Circuit
      - SCqubits
      - SQcircuit
      - Notes
   - 

      - |image1|
      - :math:`\left(\frac{0.5 n_{1}^{2}}{0.000125 + \frac{1}{8 C_{1 2}}} + \frac{0.5 n_{g1}^{2}}{0.000125 + \frac{1}{8 C_{1 2}}} + \frac{1.0 n_{1} n_{g1}}{0.000125 + \frac{1}{8 C_{1 2}}}\right) - J_{1 2} \cos{\left(θ_{1} \right)}`
      - :math:`\hat{H} =~E_{C_{11}}(\hat{n}_1-n_{g_{1}})^2~~-~E_{J_{1}}\cos(\hat{\varphi}_1)`
      - Transmon
   - 

      - |image2|
      - :math:`4000.0 Q_{1}^{2} + \left(- J_{1 2} \cos{\left(θ_{1} \right)} + 0.5 L_{1 2} (2πΦ_{1})^{2} + 0.5 L_{1 2} θ_{1}^{2} - 1.0 (2πΦ_{1}) L_{1 2} θ_{1}\right)`
      - :math:`\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\varphi_{\text{ext}_{1}})`
      - 
   - 

      - |image3|
      - :math:`\frac{0.5 Q_{1}^{2}}{0.000125 + \frac{0.125}{C_{1 2}}} + \left(- J_{1 2} \cos{\left(θ_{1} \right)} + 0.5 L_{1 2} (2πΦ_{1})^{2} + 0.5 L_{1 2} θ_{1}^{2} - 1.0 (2πΦ_{1}) L_{1 2} θ_{1}\right)`
      - :math:`\hat{H} =~\omega_1\hat a^\dagger_1\hat a_1~~-~E_{J_{1}}\cos(\hat{\varphi}_1+\varphi_{\text{ext}_{1}})`
      - Fluxonium

.. |image1| image:: img/2_node_circuits/n2_g0_c3.svg
.. |image2| image:: img/2_node_circuits/n2_g0_c5.svg
.. |image3| image:: img/2_node_circuits/n2_g0_c6.svg

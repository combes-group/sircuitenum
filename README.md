[![Documentation Status](https://readthedocs.org/projects/sircuitenum/badge/?version=latest)](https://sircuitenum.readthedocs.io/en/latest/?badge=latest)
Superconducting cIRCUIT-ENUMeration
======================================

A library for enumerating superconducting circuits.

Installation
------------

`sircuitenum` can be installed from source or via the Python package manager PyPI.

 

### Source

```bash
git clone https://github.com/combes-group/sircuitenum.git
cd sircuitenum/
pip install -e .
```

### PyPI

```bash
pip install sircuitenum
```

Library Philosophy
------------------

The core philosophy of `sircuitenum` is to be:

* Interoperable with different circuit quantization packages
* Separate data generation, data analysis, data visualisation

 

Testing
-------

The unit tests can be run locally using `pytest`. Testing dependency is installed automatically
with the package.


Disclaimer
----------

This package is currently in alpha (v0.x), and therefore you should not expect that APIs
will necessarily be stable between releases. Code that depends on this package in its current
state is very likely to break when the package version changes, so we encourage you to pin
the version you use, and update it consciously when necessary.

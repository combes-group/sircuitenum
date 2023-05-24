import os
import re
from pathlib import Path

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with open(os.path.join(HERE, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


 

setup(
    name='Superconducting Circuit Enumeration',
    version='0.1', #find_version('asdf', '__init__.py'),
    description='asdf',
    url=' ',
    author='asdf',
    author_email='asdf',
    license='GNU GPL-3.0',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=['numpy',
                    'networkx',
                    'scipy',
                    'sympy',
                    'python-rapidjson',
                    'seaborn',
                    'tqdm',
                    'matplotlib',
                    'pandas',
                    'qucat',
                    'SQcircuit',
                    'circuitq',
                    'scqubits',
                    'schemdraw',
                    'scikit-image',

                    # test dependencies
                    'flake8',
                    'pytest',
                    'pytest-cov',
                    'coverage',

                    # doc dependencies
                    'sphinx',
                    'sphinx-autodoc-typehints',
                    'sphinx_rtd_theme',
                    'nbsphinx',

                    # for testing examples
                    'nbval'
    ],
    packages=['sircuitenum'],
)


py_modules=[]
 

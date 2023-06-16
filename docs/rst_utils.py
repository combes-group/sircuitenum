import pandas as pd
import numpy as np
from pathlib import Path

from sympy import latex
import pypandoc
import yaml

from sircuitenum import utils
from sircuitenum import reduction as red
from sircuitenum import qpackage_interface as pi


def gen_notes(yaml_file, df):

    notes_vec = [""]*df.shape[0]

    with open(yaml_file, 'r') as file:
        notes = yaml.full_load(file)

    for key in notes:
        qubit = notes[key]
        match = red.isomorphic_circuit_in_set(qubit['circuit'],
                                              qubit['edges'],
                                              df['circuit'].values,
                                              df['edges'].values,
                                              True)
        if not np.isnan(match):
            notes_vec[match] = qubit["notes"]

    return notes_vec


def make_md_table(title, df, outfile=None):
    md_str = ""
    md_str += f"# {title}\n"
    md_str += "| Circuit |"
    for col in df.columns:
        if col != "filename":
            md_str += f" {col} |"
    md_str += "\n"
    md_str += "| ------- |"
    for col in df.columns:
        if col != "filename":
            md_str += f" {'-'*len(col)} |"
    md_str += "\n"

    for i, row in df.iterrows():
        # md_str += f"|![]({row['filename']})"+"{width=500px}|"
        md_str += f"|![]({row['filename']})|"
       
        for col in df.columns:
            if col != "filename":
                md_str += f"{row[col]}|"
        md_str += "\n"

    if outfile is not None:
        with open(outfile, "w") as f:
            if "md" in outfile:
                f.write(md_str)
            elif "rst" in outfile:
                f.write(md_to_rst(md_str))

    return md_str


def md_to_rst(md_str):
    return pypandoc.convert_text(md_str, 'rst', 'md',
                                 extra_args=["--list-tables"])


def gen_qubit_tables(db, n_nodes):

    # Load n node circuit database
    cir = utils.get_unique_qubits(db, n_nodes)

    # Filter out any circuits with single JJ's
    cir = cir[[("J",) not in x for x in cir.circuit.values]]

    # Locate images
    filenames = [str(Path("img", f"{n_nodes}_node_circuits", f"{x}.svg"))
                 for x in cir['unique_key']]

    # Make scqubits/sqcircuit Hamiltonians
    sc_hams = []
    sq_hams = []
    for i, row in cir.iterrows():
        # scqubits
        try:
            c1 = pi.to_SCqubits(row.circuit, row.edges)
            h1 = str(latex(c1.sym_hamiltonian(return_expr=True)))
            h1 = "$" + h1 + "$"
        except:
            h1 = "N/A"
        # sqcircuit
        try:
            c2 = pi.to_SQcircuit(row.circuit, row.edges)
            h2 = c2.description(tp="ltx", _test=True)
            h2 = "$" + h2[:h2.find("\n")] + "$"
        except:
            h2 = "N/A"
            
        sc_hams.append(h1)
        sq_hams.append(h2)

    df = pd.DataFrame({"filename": filenames,
                       "SCqubits": sc_hams,
                       "SQcircuit": sq_hams})

    df["Notes"] = gen_notes("circuit_notes.yaml", cir)
    make_md_table(f"{n_nodes} Node Circuits", df,
                  str(Path("source", f"{n_nodes}_node_circuits.rst")))


if __name__ == "__main__":

    db = "/home/eweissler/scratch/circuits.db"
    gen_qubit_tables(db, 2)
    gen_qubit_tables(db, 3)

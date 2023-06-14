import pandas as pd
import numpy as np

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


if __name__ == "__main__":

    # Load 2 node circuit database
    db = "/home/eweissler/scratch/circuits.db"
    cir = utils.get_unique_qubits(db, 2)

    # Locate images
    filenames = [f"img/2_node_circuits/{x}.svg" for x in cir['unique_key']]

    # Make scqubits Hamiltonian
    sc_hams = cir.apply(lambda row: str(latex(pi.to_SCqubits(row.circuit, row.edges).sym_hamiltonian(return_expr=True))), axis=1).values
    sc_hams = ["$" + x + "$" for x in sc_hams]
    # sc_hams = ["{math}`" + x + "`" for x in sc_hams]

    # Make sqcircuit Hamiltonian
    sq_hams = cir.apply(lambda row: pi.to_SQcircuit(row.circuit, row.edges).description(tp="ltx", _test=True), axis=1).values
    sq_hams = ["$"+x[:x.find("\n")]+"$" for x in sq_hams]
    # sq_hams = [r"{math}`" + x + "`" for x in sq_hams]

    df = pd.DataFrame({"filename": filenames,
                       "SCqubits": sc_hams,
                       "SQcircuit": sq_hams})

    df["Notes"] = gen_notes("circuit_notes.yaml", cir)
    make_md_table("2 Node Circuits", df, "source/2_node_circuits.rst")

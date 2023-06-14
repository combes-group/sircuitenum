import glob
import pandas as pd
from sympy import latex

from sircuitenum import utils
from sircuitenum import qpackage_interface as pi


def make_md_table(title, df, outfile):
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
        md_str += f"|![]({row['filename']})|"
        for col in df.columns:
            if col != "filename":
                md_str += f"{row[col]}|"
        md_str += "\n"

    with open(outfile, "w") as f:
        f.write(md_str)

    return md_str


if __name__ == "__main__":

    # Load 2 node circuit database
    db = "/home/eweissler/scratch/circuits.db"
    df = utils.get_unique_qubits(db, 2)

    # Locate images
    filenames = [f"img/2_node_circuits/{x}.svg" for x in df['unique_key']]

    # Make scqubits Hamiltonian
    sc_hams = df.apply(lambda row: str(latex(pi.to_SCqubits(row.circuit, row.edges).sym_hamiltonian(return_expr=True))), axis=1).values
    sc_hams = ["$" + x + "$" for x in sc_hams]

    # Make sqcircuit Hamiltonian
    sq_hams = df.apply(lambda row: pi.to_SQcircuit(row.circuit, row.edges).description(tp="ltx", _test=True), axis=1).values
    sq_hams = ["$"+x[:x.find("\n")]+"$" for x in sq_hams]
    df = pd.DataFrame({"filename": filenames,
                       "SCqubits": sc_hams,
                       "SQcircuit": sq_hams})
    make_md_table("2 Node Circuits", df, "2_node_circuits.md")












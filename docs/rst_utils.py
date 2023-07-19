import pandas as pd
import numpy as np
from pathlib import Path
import re

from sympy import latex, collect, expand_mul, Mul, Dummy, simplify
from sympy.core.add import Add
from sympy.core.symbol import Symbol


import pypandoc
import yaml

from sircuitenum import utils
from sircuitenum import reduction as red
from sircuitenum import qpackage_interface as pi
from sircuitenum import visualize as viz


def gen_notes(yaml_file: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a notes column from the provided yaml file


    Args:
        yaml_file (str): path to yaml file
        df (pd.DataFrame): Dataframe with circuit entries.

    Returns:
        pd.DataFrame: _description_
    """

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


def make_md_table(title: str, df: pd.DataFrame,
                  outfile=None, do_images: bool = True) -> str:
    """
    Makes a markdown table out of the given dataframe

    Args:
        title (str): Title for the page
        df (pd.DataFrame): dataframe to describe. Makes a column
                           in table for each column in df.
        outfile (str, optional): file to write to. Needs to be
                                 .md or .rst.
        do_images (bool, optional): Include images or not

    Returns:
        str: markdown for the specified table
    """
    md_str = f"# {title}\n"
    if do_images:
        md_str += "| Circuit |"
    else:
        md_str += "|"
    for col in df.columns:
        if col != "filename":
            md_str += f" {col} |"
    md_str += "\n"
    if do_images:
        md_str += "| ------- |"
    for col in df.columns:
        if col != "filename":
            md_str += f" {'-'*len(col)} |"
    md_str += "\n"

    for i, row in df.iterrows():

        if do_images:
            md_str += f"|![]({row['filename']})|"
        else:
            md_str += "|"

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
    """
    Uses pandoc to convert a string in markdown to a
    string in rst.

    Args:
        md_str (str): markdown to convert

    Returns:
        str: converted markdown in rst
    """
    return pypandoc.convert_text(md_str, 'rst', 'md',
                                 extra_args=["--list-tables"])


def gen_qubit_page(entry: pd.Series, img_dir: str,
                   outfile: str = None) -> str:
    """
    Generates a markdown or rst page to describe the
    qubit, includes circuit diagram.

    Args:
        entry (pd.Series): entry of circuit dataframe
        img_dir (str): path to a directory to store images
        outfile (str): .md or .rst file to save. Just returns
                        string if none is given.

    Returns:
        str: Full page description of a qubit
    """

    # Make the circuit diagram
    img_path = Path(img_dir, entry["unique_key"] + ".svg")
    Path(img_dir).mkdir(exist_ok=True)
    viz.draw_circuit_diagram(entry["circuit"], entry["edges"], img_path)

    # Make scqubits/sqcircuit/circuitq Hamiltonians
    # scqubits
    try:
        c_sc = pi.to_SCqubits(entry.circuit, entry.edges)
        h_sc = str(latex(c_sc.sym_hamiltonian(return_expr=True,
                                              float_round=2)))
    except:
        h_sc = "N/A"

    # sqcircuit
    try:
        c_sq = pi.to_SQcircuit(entry.circuit, entry.edges)
        h_sq = c_sq.description(tp="ltx", _test=True).replace("---", "")
        h_sq = r"\begin{align*} &" + h_sq + r"\end{align*}"

        # Insert newlines for mode/parameters
        inserts = [m.start() for m in re.finditer('text{mode}', h_sq)]
        inserts += [m.start() for m in re.finditer('text{parameters}', h_sq)]
        inserts += [m.start() for m in re.finditer('text{loops}', h_sq)]

        for n, idx in enumerate(sorted(inserts)):

            to_insert = r"\\ &"

            idx_real = idx + 4*n - 1
            h_sq = h_sq[:idx_real] + to_insert + h_sq[idx_real:]

    except:
        h_sq = "N/A"

    # circuitq
    try:
        c_cq = pi.to_CircuitQ(entry.circuit, entry.edges, ground_nodes=[0])
        h_cq = c_cq.h

        # Possible q values to group
        q_list = [q for q in h_cq.free_symbols if "q_{" in str(q)]
        qpos = []
        for q1 in q_list:
            for q2 in q_list:
                qpos.append(q1*q2)
        h_cq = str(latex(collect_expression(h_cq, q_list)))
    except:
        h_cq = "N/A"

    # Generate the page

    entry_df = pd.DataFrame([entry])[["unique_key", "n_nodes", "graph_index",
                                     "circuit", "edges"]]

    md_str = make_md_table(entry["unique_key"], entry_df,
                           do_images=False) + "\n"

    md_str += f"Notes: {entry['Notes']} \n \n"

    md_str += f"![]({img_path})\n"

    md_str += "### Circuit Hamiltonian\n"
    md_str += "For scQubits and SQcircuit, default numerical values are "
    md_str += "given as $E_C = 0.2$ GHz, $E_L = 1$ GHz, $E_J = 5$ GHz, "
    md_str += "and $E_{CJ} = 20$ GHz.\n"

    md_str += "### scQubits:\n"
    md_str += "Nodes index from 1, and are assumed to be "
    md_str += "connected to a voltage source via a coupling capacitor.\n"
    md_str += f"$${h_sc}$$\n"

    md_str += "### SQcircuit:\n"
    md_str += f"$${h_sq}$$\n"

    md_str += "### CircuitQ:\n"
    md_str += "Nodes index from 0, with node 0 assigned to be ground. "
    md_str += "Flux biases are included, but offset charges are ignored.\n"
    md_str += f"$${h_cq}$$\n"

    if outfile is not None:
        with open(outfile, "w") as f:
            if "md" in outfile:
                f.write(md_str)
            elif "rst" in outfile:
                f.write(md_to_rst(md_str))

    return md_str

def collect_expression(expr: Add, syms: list[Symbol]) -> Add:
    """
    Collects the terms in a sympy expression that
    contain the specified symbols

    Args:
        expr (Add): Sympy expression from circuitq for hamiltonian
        syms (list[Symbol]): list of symbols to expand/collect.
                             intended to be list of q variables.

    Returns:
        Add: Modified expression with syms terms collected
    """

    m = [i for i in expr.atoms(Mul) if not any([i.has(x) for x in syms])]
    reps = dict(zip(m, [Dummy() for i in m]))
    return collect(expand_mul(expr.xreplace(reps)
                              ).subs([(v, k) for k, v in reps.items()]), syms)


def gen_basegraph_page(db_file: str, n_nodes: int,
                       graph_index: int,
                       image_dir: str,
                       outfile: str = None) -> str:
    """
    Creates a page containing an image of the basegraph
    on top, followed by all unique qubits formed from
    said basegraph.

    Args:
        db_file (str): path to database file
        n_nodes (int): number of nodes
        graph_index (int): basegraph index
        image_dir (str): folder to save images in
        outfile (str): .md or .rst file to save. Just returns
                        string if none is given.

    Returns:
        str: markdown string
    """

    # Load n node circuit database
    df = utils.get_unique_qubits(db, n_nodes)

    # Filter out for specified basegraph and add notes
    df = df[[graph_index == x for x in df["graph_index"].values]]
    df["Notes"] = gen_notes("circuit_notes.yaml", df)

    # Generate image of basegraph
    img_path = Path(image_dir, f"basegraph_{graph_index}_{n_nodes}_nodes.svg")
    Path(img_dir).mkdir(exist_ok=True)
    viz.draw_basegraph(utils.get_basegraphs(n_nodes)[graph_index],
                       f"{n_nodes} Nodes, Basegraph {graph_index}",
                       img_path)

    # Header
    md_str = ""
    md_str += f"# {n_nodes} Nodes, Basegraph {graph_index}\n"
    md_str += f"![]({img_path})\n"
    md_str += "All unique qubits derived from the above base graph are "
    md_str += "shown below. Circuits with series linear elements or no "
    md_str += "no Josephson Junctions are excluded.\n"

    # Add each Qubit Individually
    md_str += "\n".join((df.apply(lambda row: gen_qubit_page(row, img_dir),
                                  axis=1)).values)

    if outfile is not None:
        with open(outfile, "w") as f:
            if "md" in outfile:
                f.write(md_str)
            elif "rst" in outfile:
                f.write(md_to_rst(md_str))

    return md_str

def gen_qubit_tables(db, n_nodes):

    # Load n node circuit database
    cir = utils.get_unique_qubits(db, n_nodes)

    # Filter out any circuits with single JJ's
    cir = cir[[("J",) not in x for x in cir.circuit.values]]

    # Locate images
    filenames = [str(Path("img", f"{n_nodes}_node_circuits", f"{x}.svg"))
                 for x in cir['unique_key']]

    

    df = pd.DataFrame({"filename": filenames,
                       "SCqubits": sc_hams,
                       "SQcircuit": sq_hams})
    df = df[["filename", "SQcircuit", "SCqubits"]]

    df["Notes"] = gen_notes("circuit_notes.yaml", cir)
    make_md_table(f"{n_nodes} Node Circuits", df,
                  str(Path("source", f"{n_nodes}_node_circuits.rst")))


if __name__ == "__main__":

    db = "/home/eweissler/scratch/circuits.db"
    # gen_qubit_tables(db, 2)
    # gen_qubit_tables(db, 3)

    # Load n node circuit database
    # df = utils.get_unique_qubits(db, 2)
    img_dir = "/home/eweissler/src/sircuitenum/docs/source/img"

    # df["Notes"] = gen_notes("circuit_notes.yaml", df)

    for n_nodes in [2, 3]:
        basegraphs = utils.get_basegraphs(n_nodes)
        for graph_index in range(len(basegraphs)):
            fname = f"Basegraph_{graph_index}_Nodes_{n_nodes}.rst"
            gen_basegraph_page(db, n_nodes, graph_index,
                               img_dir, fname)

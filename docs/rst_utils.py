import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import re

from sympy import latex, collect, expand_mul, Mul, Dummy
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
        write_md_rst(md_str, outfile)

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
    rst_str = pypandoc.convert_text(md_str, 'rst', 'md',
                                    extra_args=["--list-tables"])
    rst_str = rst_str.replace(r":raw-latex:`", r".. math:: ")
    rst_str = rst_str.replace(r"\end{align*}`", r"\end{align*}")
    return rst_str


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
    plt.close()

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
        h_sq = r"\begin{align*} &" + h_sq.replace("\n", " ") + r"\end{align*}"

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
        h_cq = str(latex(utils.collect_expression(h_cq, q_list)))
    except:
        h_cq = "N/A"

    # Generate the page

    entry_df = pd.DataFrame([entry])[["unique_key", "n_nodes", "graph_index",
                                     "circuit", "edges"]]

    md_str = make_md_table(entry["unique_key"], entry_df,
                           do_images=False) + "\n"

    md_str += f"Notes: {entry['Notes']} \n \n"

    if outfile is None:
        md_str += f"![]({img_path})\n"
    else:
        if str(outfile)[0] != "/":
            outfile = Path(str(outfile)).absolute()
        md_str += f"![]({img_path.relative_to(outfile.parent)})\n"

    md_str += "\n### Circuit Hamiltonian\n"
    md_str += "For scQubits and SQcircuit, default numerical values are "
    md_str += "given as $E_C = 0.2$ GHz, $E_L = 1$ GHz, $E_J = 5$ GHz, "
    md_str += "and $E_{CJ} = 20$ GHz.\n"

    md_str += "\n#### scQubits:\n"
    md_str += "Nodes index from 1, and are assumed to be "
    md_str += "connected to a voltage source via a coupling capacitor.\n"
    md_str += f"$${h_sc}$$\n"

    md_str += "\n#### SQcircuit:\n"
    md_str += f"{h_sq}\n"

    md_str += "\n#### CircuitQ:\n"
    md_str += "Nodes index from 0, with node 0 assigned to be ground. "
    md_str += "Flux biases are included, but offset charges are ignored.\n"
    md_str += f"$${h_cq}$$\n"

    if outfile is not None:
        write_md_rst(md_str, outfile)

    return md_str


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
    fname = f"basegraph_{n_nodes}_nodes_i_{str(graph_index).zfill(3)}.svg"
    img_path = Path(image_dir, fname)
    Path(img_dir).mkdir(exist_ok=True)
    viz.draw_basegraph(utils.get_basegraphs(n_nodes)[graph_index],
                       f"{n_nodes} Nodes, Basegraph {graph_index}",
                       img_path)
    plt.close()

    # Header
    md_str = ""
    md_str += f"# {n_nodes} Nodes, Basegraph {graph_index}\n"

    # Add image
    if outfile is None:
        md_str += f"![]({img_path})\n"
    else:
        if str(outfile)[0] != "/":
            outfile = Path(str(outfile)).absolute()
        md_str += f"![]({img_path.relative_to(outfile.parent)})\n"

    md_str += "\nAll unique qubits derived from the above base graph are "
    md_str += "shown below. Circuits with series linear elements or "
    md_str += "no Josephson Junctions are excluded.\n"

    # Add each Qubit Individually
    if outfile is None:
        temp = None
    else:
        temp = Path(Path(outfile).parent, "temp.rst")

    qubit_pages = df.apply(lambda row: "\n#"+gen_qubit_page(row, img_dir,
                                                            temp),
                           axis=1).values

    # Organize into number of Josephson Junctions
    n_jj = np.array([utils.count_elems_mapped(x)["J"]
                     for x in df.circuit.values])
    order = np.argsort(n_jj)
    qubit_pages = qubit_pages[order]
    n_jj = n_jj[order]

    # Add delimiters
    qubit_pages[0] = f"\n## {n_jj[0]} Josephson Junction \n---\n" + qubit_pages[0]
    for i in range(1, len(n_jj)):
        if n_jj[i] != n_jj[i-1]:
            qubit_pages[i] = f"\n## {n_jj[i]} Josephson Junctions \n---\n" + qubit_pages[i]

    md_str += "\n---\n".join(qubit_pages)

    if outfile is not None:
        write_md_rst(md_str, outfile)

        # Delte temporary file
        Path(temp).unlink()

    return md_str


def gen_basegraph_summary(max_nodes: int,
                          image_dir: str,
                          outfile: str = None) -> str:
    """
    Generates a page that shows images of every basegraph
    in a table separated by number of nodes.

    Args:
        max_nodes (int, optional): Maximum number of nodes to show up to.
                                   Defaults to 5.
        image_dir (str): folder to save images in
        outfile (str, optional): path to .md or .rst to save to.
                                 returns only str of markdown if 
                                 none is given.

    Returns:
        str: markdown text
    """
    md_str = "# All Basegraphs\n"
    for n_nodes in range(2, max_nodes + 1):
        md_str += f"## {n_nodes} Nodes\n"
        basegraphs = utils.get_basegraphs(n_nodes)
        df = []
        for ig, G in enumerate(basegraphs):
            entry = {}
            entry["Nodes"] = n_nodes
            entry["Index"] = ig

            # Make the image
            fname = f"basegraph_{n_nodes}_nodes_i_{str(ig).zfill(3)}.svg"
            img_path = Path(image_dir, fname)
            Path(img_dir).mkdir(exist_ok=True)
            viz.draw_basegraph(G, f"{n_nodes} Nodes, Basegraph {ig}",
                               img_path)
            plt.close()
            if outfile is not None:
                if str(outfile)[0] != "/":
                    outfile = Path(str(outfile)).absolute()
                entry["filename"] = img_path.relative_to(outfile.parent)
            else:
                entry["filename"] = img_path

            df.append(entry)

        df = pd.DataFrame(df)
        md_str += make_md_table("", df)[1:] + "\n"

    if outfile is not None:
        write_md_rst(md_str, outfile)

    return md_str


def write_md_rst(md_str, outfile):
    outfile = str(outfile)
    with open(outfile, "w") as f:
        if ".md" == outfile[-3:]:
            f.write(md_str)
        elif ".rst" == outfile[-4:]:
            f.write(md_to_rst(md_str))

if __name__ == "__main__":

    db = "/home/eweissler/scratch/circuits.db"
    # gen_qubit_tables(db, 2)
    # gen_qubit_tables(db, 3)

    # Load n node circuit database
    # df = utils.get_unique_qubits(db, 2)
    img_dir = "/home/eweissler/src/sircuitenum/docs/source/img"

    gen_basegraph_summary(5, img_dir, "source/Basegraph_Summary.rst")

    for n_nodes in [2, 3]:
        basegraphs = utils.get_basegraphs(n_nodes)
        for graph_index in range(len(basegraphs)):
            fname = f"source/Basegraph_{graph_index}_Nodes_{n_nodes}.rst"
            gen_basegraph_page(db, n_nodes, graph_index,
                               img_dir, fname)

import glob

from sircuitenum import utils


def make_md_table(title, filenames, outfile):
    with open(outfile, "w") as f:
        f.write(f"# {title}\n")
        f.write("| Circuit | Hamiltonian |\n")
        f.write("| ------- | ----------- |\n")
        for fn in filenames:
            f.write(f"|![]({fn})|placeholder|\n")


if __name__ == "__main__":
    filenames = glob.glob("img/2_node_circuits/*")
    make_md_table("2 Node Circuits", filenames, "2_node_circuits.md")

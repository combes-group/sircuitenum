"edge_enumerate.py: Contains functions to visualize the circuits present"
__author__ = "Mohit Bhat, Eli Weissler"
__version__ = "0.1.0"
__status__ = "Development"

# -------------------------------------------------------------------
# Import Statements
# -------------------------------------------------------------------

import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
from tqdm import tqdm
from scipy.spatial.distance import pdist

import schemdraw
import schemdraw.elements as elm

from sircuitenum import utils
from sircuitenum import reduction as red
from sircuitenum import visualize as viz


G_POS = {'2': [{0: np.array([-1/np.sqrt(2), -1/np.sqrt(2)]),
                1: np.array([0., 0.])}],
         '3': [{0: np.array([-1/np.sqrt(2), 1/np.sqrt(2)]),
                1: np.array([1/np.sqrt(2), -1/np.sqrt(2)]),
                2: np.array([0., 0.])},
               {0: np.array([0., 0.]),
                1: np.array([0.5, np.sqrt(3)/2]),
                2: np.array([-0.5, np.sqrt(3)/2])}],
         '4': [{0: np.array([np.sqrt(3)/2, -0.5]),
                1: np.array([0., 1.]),
                2: np.array([-np.sqrt(3)/2, -0.5]),
                3: np.array([0., 0.])},
               {0: -1*np.array([1/np.sqrt(2), 1/np.sqrt(2)]),
                1: np.array([1/np.sqrt(2), 1/np.sqrt(2)]),
                2: -2*np.array([1/np.sqrt(2), 1/np.sqrt(2)]),
                3: np.array([0., 0.])},
               {0: np.array([-0.5, np.sqrt(3)/2]),
                1: np.array([0., -1.]),
                2: np.array([0.5, np.sqrt(3)/2]),
                3: np.array([0., 0.])},
               {0: np.array([0., 0.]),
                1: np.array([1., 1.]),
                2: np.array([1., 0.]),
                3: np.array([0., 1.])},
               {0: np.array([-0.5, np.sqrt(3)/2]),
                1: np.array([1., 0.]),
                2: np.array([0.5, np.sqrt(3)/2]),
                3: np.array([0., 0.])},
               {0: (3/np.sqrt(3))*np.array([0.5, np.sqrt(3)/5]),
                1: (3/np.sqrt(3))*np.array([1., 0.]),
                2: (3/np.sqrt(3))*np.array([0.5, np.sqrt(3)/2]),
                3: (3/np.sqrt(3))*np.array([0., 0.])}]}


def black_or_white_text(color: tuple):
    """
    Determines whether it's more appropriate
    to write using black or white text on the
    given color.

    From: https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color

    Args:
        color (tuple): (R, G, B) between 0 and 1 each

    Returns:
        True for black text, False for white text
    """
    thresh = color[0]*0.299 + color[1]*0.587 + color[2]*0.114
    # 186/255
    return thresh > 0.729


def draw_port_graph(circuit: list, edges: list, out="port_graph.png",
                    node_size: float = 10000, scale: float = 6,
                    font_size: int = 30):
    """
    Draw the port graph corresponding to the given circuit

    Args:
        circuit (list of str): a list of elements for the desired circuit
                                 (i.e., [[['C'],['C'],['L'],['C','J']])
        edges (list of tuples of ints): a list of edge connections for the
                             desired circuit (i.e., [(0,1),(1,2),(2,3),(3,0)])
        out (str, optional): filename to save as, including extension.
                                 Defaults to "port_graph.png".
        node_size (float, optional): size for tuning size of nodes in plot
        scale (float, optional): size for tuning overall spacing of nodes
        font_size (int, optional): text size for node labels

    Returns:
        matplotlib figure if out is "", else nothing
    """

    # Get the layout and scale it
    fig = plt.figure()
    fig.set_size_inches(fig.get_size_inches()*scale)
    G = red.convert_circuit_to_port_graph(circuit, edges)
    if nx.is_planar(G):
        pos = nx.planar_layout(G)
    else:
        pos = nx.spring_layout(G)
    for n in pos:
        pos[n] = pos[n]*scale

    # Use a colormap to generate a color for each node
    # And use that color to decide on white vs. black text for
    # each node
    node_color_map = nx.get_node_attributes(G, "color")
    node_color = np.array([node_color_map[n] for n in G.nodes()]).astype(float)
    node_color /= np.max(node_color)
    cmap = matplotlib.cm.get_cmap('viridis')
    black_text_nodes = {}
    white_text_nodes = {}

    node_color_mapped = []
    for i, n in enumerate(G.nodes()):
        color = cmap(node_color[i])
        node_color_mapped.append(color)
        if black_or_white_text(color):
            black_text_nodes[n] = pos[n]
        else:
            white_text_nodes[n] = pos[n]

    nx.draw(G, pos, node_color=node_color, node_size=node_size)
    # Draw black text nodes
    Gk = nx.Graph()
    for n in black_text_nodes:
        Gk.add_node(n)
    nx.draw_networkx_labels(Gk, black_text_nodes,
                            font_color='k', font_size=font_size)
    # Draw white text nodes
    Gw = nx.Graph()
    for n in white_text_nodes:
        Gw.add_node(n)
    nx.draw_networkx_labels(Gw, white_text_nodes,
                            font_color='w', font_size=font_size)

    if out != "":
        plt.savefig(out)
        plt.close()

    else:
        return fig


def print_bare_graphs(all_graphs: list):
    """Plots unlabeled graphs from graph list returned
    from get_graphs_from_file() function

    Args:
        all_graphs (list): a list of unlabeled graphs
    """
    for i, G in enumerate(all_graphs):
        draw_basegraph(G, f"graph index: {i}")


def draw_all_basegraphs(base_path: str, n_start: int = 2, n_end: int = 4):
    """
    Draws all the basegraphs for nodes with number
    n_start through n_end.

    Args:
        base_path (str): folder to save images in
        n_start (int, optional): start drawing graphs
                                 for this number of nodes
        n_end (int, optional): stop drawing graphs for this
                               number of nodes (inclusive)

    Returns:
        dict: positions of nodes for each plot
    """
    pos = {}
    for n_nodes in range(n_start, n_end + 1):
        pos[str(n_nodes)] = []
        all_graphs = utils.get_basegraphs(n_nodes)
        for i, G in enumerate(all_graphs):
            fname = str(Path(base_path, f"n{n_nodes}_g{i}.svg"))
            title = f"{n_nodes} nodes, graph {i}"
            f, p = draw_basegraph(G, title, fname,
                                  G_POS[str(n_nodes)][i])
            for k in p:
                p[k] = np.round(p[k], 2)
            pos[str(n_nodes)].append(p)

    return pos


def draw_basegraph(G: nx.Graph, title: str = "",
                   savename: str = "", pos: dict = {}):
    """Plots unlabeled graphs from graph list returned
    from get_graphs_from_file() function

    Args:
        G (nx.graph): networkx graph to plot
        savename (str): location to save the plots

    Returns:
        tuple: figure, positioning (x, y) of nodes
    """
    f = plt.figure()
    if len(pos) == 0:
        pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos=pos)
    plt.title(title)
    plt.gca().set_aspect('equal')
    if len(savename) > 0:
        plt.savefig(savename)
    return f, pos


def draw_all_qubits(file: str, n_nodes: int, out_dir: str,
                    layout: str = 'fixed', format: str = ".svg"):

    # So plots don't pop up
    matplotlib.use('agg')
    df = utils.get_unique_qubits(file, n_nodes)
    for uid, row in tqdm(df.iterrows(), total=df.shape[0]):
        circuit = row.circuit
        edges = row.edges
        graph_index = row.graph_index
        viz.draw_circuit_diagram(circuit, edges,
                                 out=Path(out_dir, f"{uid}{format}"),
                                 layout=layout, graph_index=graph_index)
        plt.close()


def draw_circuit_diagram(circuit: list, edges: list,
                         out: str = "circuit_diagram.png",
                         scale: float = 4.0, layout: str = 'planar',
                         spread: float = 2/5, graph_index: int = None):
    """
    Draws the circuit diagram using schemdraw.

    For parallel elements goes to 1/4 of the way along
    the connection and fans oout to do the elements in parallel.

    Doesn't do anything to avoid overlap for non-planar graphs.

    Args:
        circuit (list): a list of element labels for the desired circuit
                        e.g. [["J"],["L", "J"], ["C"]]
        edges (list): a list of edge connections for the desired circuit
                        e.g. [(0,1), (0,2), (1,2)]
        out (str): filename to save the plot to,
                    a blank string makes the plot show up interactively
        scale (float): scaling factor for the networkx positions, to spread out
                        the plots if needed.
        layout (str): options for graph layouts.
                      Spring seems to produce prettier circuits, but it often
                      results in overlapping elements, even for planar graphs.
        spread (float): fraction of edge length to fan out parallel components
        graph_index (int): Required for fixed layout. base graph index.

    Returns:
        None: displays plot if out == ""
    """

    elem_dict = {
        'C': {'default_unit': 'GHz', 'default_value': 0.2},
        'L': {'default_unit': 'GHz', 'default_value': 1.0},
        'J': {'default_unit': 'GHz', 'default_value': 5.0},
        }
    params = utils.gen_param_dict(circuit, edges, elem_dict)
    G = utils.convert_circuit_to_graph(circuit, edges,
                                       params=params)

    # Get layout of vertices
    if layout == 'planar':
        if nx.is_planar(G):
            pos = nx.planar_layout(G)
        else:
            print("Not a planar graph... reverting to spring layout")
            pos = nx.spring_layout(G)
    elif layout == 'spring':
        pos = nx.spring_layout(G)
    elif layout == 'fixed' and graph_index is not None:
        pos = G_POS[str(G.number_of_nodes())][graph_index]
    else:
        raise ValueError("must specify layout for graph and include\
                          graph_index if using fixed layout")

    # Scale
    scaled_pos = {}
    for k in pos:
        scaled_pos[k] = pos[k]*scale

    # Define the circuit elements
    elem_bank = {
        'C': lambda: elm.Capacitor(),
        'L': lambda: elm.Inductor(),
        'J': lambda: elm.Josephson()
    }

    # Calculate minimum pairwise distance for plotting
    pdist_mat = pdist(np.vstack([x for x in scaled_pos.values()]))
    min_r = np.min(pdist_mat[pdist_mat > 0])

    with schemdraw.Drawing() as d:
        for n0 in G.nodes():
            # Draw a dot at every node
            d.add(elm.Dot().at(scaled_pos[n0]))
            for n1 in G.nodes():
                if n0 != n1 and n0 < n1 and G.has_edge(n0, n1):
                    edgesBetweenNodes = G[n0][n1]
                    # Single element
                    nEdges = len(edgesBetweenNodes)
                    if nEdges == 1:
                        edge = edgesBetweenNodes[0]
                        # Get the endpoints and specific circuit element
                        # that correspond to this edge
                        x0 = scaled_pos[n0]
                        x1 = scaled_pos[n1]
                        d.add(elem_bank[edge['element']]().endpoints(x0, x1))
                    # Parallel Elements
                    else:
                        # Draw a line perpendicular to the connection
                        # Split way there and spread out spread
                        # out and do them in parallel
                        split = 1/4
                        x0 = scaled_pos[n0]
                        x1 = scaled_pos[n1]

                        # Unit vectors along displacement and
                        # perpendicular to it
                        rhat = x1-x0
                        r = np.linalg.norm(rhat)
                        rhat /= r
                        norm = np.array([-rhat[1], rhat[0]])
                        perp_step = (spread*min_r/nEdges)*norm

                        # Anchor points for splitting
                        adj = split*rhat*(r-min_r)
                        a0 = x0+split*rhat*r+adj
                        a1 = x1-split*rhat*r-adj
                        d.add(elm.Wire().at(x0).to(a0))
                        d.add(elm.Wire().at(x1).to(a1))

                        # Start at 0 and go out integer
                        # steps if odd numberof edges.
                        # For even number of edges do 1/2 integer steps
                        if nEdges % 2 == 0:
                            maxSpread = (perp_step*(nEdges/2-1/2))
                            d.add(elm.Wire().at(a0+maxSpread).to(a0-maxSpread))
                            d.add(elm.Wire().at(a1+maxSpread).to(a1-maxSpread))
                            for edgeNum in range(int(nEdges/2)):
                                edge1 = edgesBetweenNodes[edgeNum]
                                edge2 = edgesBetweenNodes[nEdges-1-edgeNum]
                                d.add(elem_bank[edge1['element']]().endpoints(
                                    a0+perp_step*(edgeNum+1/2),
                                    a1+perp_step*(edgeNum+1/2)))
                                d.add(elem_bank[edge2['element']]().endpoints(
                                    a0-perp_step*(edgeNum+1/2),
                                    a1-perp_step*(edgeNum+1/2)))
                        else:
                            maxSpread = (perp_step*(nEdges-1)/2)
                            d.add(elm.Wire().at(a0+maxSpread).to(a0-maxSpread))
                            d.add(elm.Wire().at(a1+maxSpread).to(a1-maxSpread))
                            # 0th one straight across
                            d.add(elem_bank[edgesBetweenNodes[0]
                                  ['element']]().endpoints(a0, a1))

                            # Others mirrored across -- work in pairs
                            for edgeNum in range(1, int((nEdges-1)/2 + 1)):
                                edge1 = edgesBetweenNodes[edgeNum]
                                edge2 = edgesBetweenNodes[nEdges-edgeNum]
                                d.add(elem_bank[edge1['element']]().endpoints(
                                    a0+perp_step*edgeNum,
                                    a1+perp_step*edgeNum))
                                d.add(elem_bank[edge2['element']]().endpoints(
                                    a0-perp_step*edgeNum,
                                    a1-perp_step*edgeNum))
        if out != "":
            d.save(out)
    if out != "":
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":

    # Basegraphs
    base = '/home/eweissler/img/basegraphs'
    draw_all_basegraphs(base)

    # Actual Circuits
    base = "/home/eweissler/img/fixed_layout"
    toLoad = "/home/eweissler/scratch/circuits.db"
    for n_nodes in range(2, 5):
        out_dir = Path(base, f'{n_nodes}_node_circuits')
        out_dir.mkdir(parents=True, exist_ok=True)
        draw_all_qubits(toLoad, n_nodes, out_dir=out_dir, layout='fixed')

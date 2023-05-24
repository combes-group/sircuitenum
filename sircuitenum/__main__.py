
# Simple command line interface
import argparse
from sircuitenum import enum
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--db_untrimmed", type=str, default="circuits.db",
                    help="Database file to save raw enumeration out to")
parser.add_argument("-t", "--db_trimmed", type=str, default="circuits_trimmed.db",
                    help="Database file to save reduced enumeration out to")
parser.add_argument("-b", "--base", type=int, default=7,
                    help="How many different types of edges to allow")
parser.add_argument("-s", "--start", type=int, default=2,
                    help="Number of nodes to start generating from")
parser.add_argument("-p", "--stop", type=int, default=3,
                    help="Number of nodes to stop generating at (does not do this number)")
args = parser.parse_args()

enum.generate_all_graphs(args.db_untrimmed, args.db_trimmed, 
                    args.start, args.stop, args.base)
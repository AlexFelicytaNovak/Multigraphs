import sys
import argparse
from multidigraph import MultiDiGraph
from graph_functions import get_graph_from_multigraph, get_undirected_graph_from_directed_graph, read_graph_from_file

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g1', '--graph1')
    parser.add_argument('-g2', '--graph2')

    args = parser.parse_args()

    # if len(sys.argv) == 2:
    if args.graph1:
        # with open(str(sys.argv[1]), 'r') as f:
        g1 = MultiDiGraph(read_graph_from_file(args.graph1))
        g1.print()
        graph = get_graph_from_multigraph(g1)
        undirected_graph = get_undirected_graph_from_directed_graph(MultiDiGraph(graph))
        
    else:
        print('No graph data file given!')

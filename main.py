import sys
import argparse
from multidigraph import MultiDiGraph
from graph_functions import get_graph_from_multigraph, get_undirected_graph_from_directed_graph

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g1', '--graph1')
    parser.add_argument('-g2', '--graph2')

    args = parser.parse_args()

    # if len(sys.argv) == 2:
    if args.graph1:
        # with open(str(sys.argv[1]), 'r') as f:
        with open(args.graph1, 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        n = lines[0]
        rows = lines[1:-1]
        matrix = []
        for row in rows:
            matrix.append(row.split())

        g1 = MultiDiGraph(matrix)
        g1.print()
        graph = get_graph_from_multigraph(g1)
        undirected_graph = get_undirected_graph_from_directed_graph(MultiDiGraph(graph))
        
    else:
        print('No graph data file given!')

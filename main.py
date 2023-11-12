import argparse

from graph_functions import read_graph_from_file
from MultiDiGraph import MultiDiGraph

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g1', '--graph1')
    parser.add_argument('-c', '--clique', action='store_true')

    parser.add_argument('-g2', '--graph2')
    parser.add_argument('-d', '--distance', action='store_true')
    parser.add_argument('-s', '--subgraph', action='store_true')

    args = parser.parse_args()

    # if len(sys.argv) == 2:
    if args.graph1:
        # with open(str(sys.argv[1]), 'r') as f:
        g1 = MultiDiGraph(read_graph_from_file(args.graph1))
        g1.print()
        graph = MultiDiGraph.get_graph_from_multigraph(g1.adjacency_matrix)
        undirected_graph = MultiDiGraph.get_undirected_graph_from_directed_graph(graph)
        g1.maximal_cliques()

    else:
        print('No graph data file given!')
        exit()

    if args.clique:
        print("Maximal clique for graph 1: ")
        pass

    if args.graph2:
        # with open(str(sys.argv[1]), 'r') as f:
        g2 = MultiDiGraph(read_graph_from_file(args.graph2))
        g2.print()
    else:
        if args.distance or args.subgraph:
            print('No graph data file for 2nd graph given!')
        exit()

    if args.distance:
        print("Distance between graph 1 and graph 2:")
        pass

    if args.subgraph:
        print("Maximal subgraph for graph 1 and graph 2:")
        pass

import argparse

from graph_functions import read_graph_from_file
from maximum_subgraph import find_maximum_subgraphs
from MultiDiGraph import MultiDiGraph

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g1', '--graph1')
    parser.add_argument('-c', '--clique', action='store_true')
    parser.add_argument('-ac', '--approx_clique', action='store_true')

    parser.add_argument('-g2', '--graph2')
    parser.add_argument('-d', '--distance', action='store_true')
    parser.add_argument('-ad', '--approx_distance', action='store_true')
    parser.add_argument('-s', '--subgraph', action='store_true')
    parser.add_argument('-as', '--approx_subgraph', action='store_true')

    args = parser.parse_args()

    # if len(sys.argv) == 2:
    if args.graph1:
        # with open(str(sys.argv[1]), 'r') as f:
        g1 = MultiDiGraph(read_graph_from_file(args.graph1))
        g1.print()
        graph = MultiDiGraph.get_graph_from_multigraph(g1.adjacency_matrix)
        undirected_graph = MultiDiGraph.get_undirected_graph_from_directed_graph(graph)
        print(g1.maximum_cliques())

    else:
        print('No graph data file given!')
        exit()

    if args.clique:
        print("Maximal clique for graph 1: ")
        pass

    if args.approx_clique:
        print("Maximal clique approximation for graph 1: ")
        pass

    if args.graph2:
        # with open(str(sys.argv[1]), 'r') as f:
        g2 = MultiDiGraph(read_graph_from_file(args.graph2))
        g2.print()
    else:
        if args.distance or args.subgraph or args.approx_distance or args.approx_subgraph:
            print('No graph data file for 2nd graph given!')
        exit()

    if args.distance:
        print("Distance between graph 1 and graph 2:")
        pass

    if args.approx_distance:
        print("Distance approximation between graph 1 and graph 2:")
        pass

    if args.subgraph:
        print("Maximum subgraph for graph 1 and graph 2:")
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
        print(f"number of maximum subgraphs: {len(maximum_subgraphs)}")
        maximum_subgraphs[0].print()
        pass

    if args.approx_subgraph:
        print("Maximum subgraph approximation for graph 1 and graph 2:")
        pass

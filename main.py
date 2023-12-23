import argparse
from graph_functions import read_graph_from_file, print_clique_and_matrix
from distance_functions import distance_l1, distance_l2, approx_distance_l1, approx_distance_l2
from maximum_subgraph import find_maximum_subgraphs
from MultiDiGraph import MultiDiGraph

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g1', '--graph1')
    parser.add_argument('-c', '--clique', action='store_true')
    parser.add_argument('-ac', '--approx_clique', action='store_true')

    parser.add_argument('-g2', '--graph2')
    parser.add_argument('-d1', '--distance_l1', action='store_true')
    parser.add_argument('-ad1', '--approx_distance_l1', action='store_true')
    parser.add_argument('-d2', '--distance_l2', action='store_true')
    parser.add_argument('-ad2', '--approx_distance_l2', action='store_true')
    parser.add_argument('-s', '--subgraph', action='store_true')
    parser.add_argument('-as', '--approx_subgraph', action='store_true')

    args = parser.parse_args()

    # if len(sys.argv) == 2:
    if args.graph1:
        # with open(str(sys.argv[1]), 'r') as f:
        print("MultiDiGraph 1:")
        g1 = MultiDiGraph(read_graph_from_file(args.graph1))
        g1.print()
        graph = MultiDiGraph.get_graph_from_multigraph(g1.adjacency_matrix)
        undirected_graph = MultiDiGraph.get_undirected_graph_from_directed_graph(graph)

    else:
        print('No graph data file given!')
        exit()

    if args.clique:
        print('\nMaximum cliques for graph 1: ')
        cliques = g1.maximum_cliques()
        for c in cliques:
            print_clique_and_matrix(g1.adjacency_matrix, c)
        print('Maximal cliques for graph 1: ')
        cliques = g1.maximal_cliques()
        for c in cliques:
            print_clique_and_matrix(g1.adjacency_matrix, c)

    if args.approx_clique:
        print('Maximum clique(s) approximation for graph 1:')
        cliques = g1.approx_maximum_cliques()
        for c in cliques:
            print_clique_and_matrix(g1.adjacency_matrix, c)

    if args.graph2:
        print("MultiDiGraph 2:")
        g2 = MultiDiGraph(read_graph_from_file(args.graph2))
        g2.print()
    else:
        if args.distance_l1 or args.subgraph or args.approx_distance_l1 or args.approx_subgraph or args.distance_l2  or args.approx_distance_l2:
            print('No graph data file for 2nd graph given!')
        exit()

    if args.distance_l1:
        print("Distance between graph 1 and graph 2:")
        distance, _ = distance_l1(g1, g2)
        print(distance)

    if args.approx_distance_l1:
        print("Distance approximation between graph 1 and graph 2:")
        distance, _ = approx_distance_l1(g1, g2)
        print(distance)

    if args.distance_l2:
        print("Distance between graph 1 and graph 2:")
        distance, _ = distance_l2(g1, g2)
        print(distance)

    if args.approx_distance_l2:
        print("Distance approximation between graph 1 and graph 2:")
        distance, _ = approx_distance_l2(g1, g2)
        print(distance)

    if args.subgraph:
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
        print(f"Number of maximum subgraphs for graph 1 and graph 2: {len(maximum_subgraphs)}, convention for mapping "
              f"vertices used: (subgraph_vertex_index, graph_1_vertex_index, graph_2_vertex_index) ")

        for subgraph in maximum_subgraphs:
            print(f"{maximum_subgraphs.index(subgraph) +1} / {len(maximum_subgraphs)}:")
            subgraph['multi_di_subgraph'].print()
            print(f"multigraph 1 vertex set: {subgraph['graph_1_vertices']}")
            print(f"multigraph 2 vertex set: {subgraph['graph_2_vertices']}")
            print(f"vertices map: {subgraph['printable_vertex_map']}\n")

    if args.approx_subgraph:
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2, approximate=True)
        print(f"Number of maximum subgraphs approximations for graph 1 and graph 2: {len(maximum_subgraphs)}, "
              f"convention for mapping vertices used: (subgraph_vertex_index, graph_1_vertex_index, "
              f"graph_2_vertex_index) ")

        for subgraph in maximum_subgraphs:
            print(f"{maximum_subgraphs.index(subgraph) +1} / {len(maximum_subgraphs)}:")
            subgraph['multi_di_subgraph'].print()
            print(f"multigraph 1 vertex set: {subgraph['graph_1_vertices']}")
            print(f"multigraph 2 vertex set: {subgraph['graph_2_vertices']}")
            print(f"vertices map: {subgraph['printable_vertex_map']}\n")

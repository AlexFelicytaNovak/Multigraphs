import argparse
import math

import numpy

from graph_functions import read_graph_from_file, print_clique_and_matrix
from maximum_subgraph import find_maximum_subgraphs
from MultiDiGraph import MultiDiGraph
from bcolors import bcolors

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

        # print(f'{bcolors.OKBLUE}Maximal cliques: {bcolors.ENDC}')
        # cliques = g1.maximal_cliques()
        # for c in cliques:
        #     print_clique_and_matrix(g1.adjacency_matrix, c)

        # print(f'\n{bcolors.OKBLUE}Maximum cliques: {bcolors.ENDC}')
        # cliques = g1.maximum_cliques()
        # for c in cliques:
        #     print_clique_and_matrix(g1.adjacency_matrix, c)

        # print(f'{bcolors.OKBLUE}Maximum cliques approx: {bcolors.ENDC}')
        # cliques = g1.approx_maximum_cliques()
        # for c in cliques:
        #     print_clique_and_matrix(g1.adjacency_matrix, c)

    else:
        print('No graph data file given!')
        exit()

    if args.clique:
        print(f'\n{bcolors.OKBLUE}Maximum clique(s) for graph 1: {bcolors.ENDC}')
        cliques = g1.maximum_cliques()
        for c in cliques:
            print_clique_and_matrix(g1.adjacency_matrix, c)
        pass

    if args.approx_clique:
        print(f'{bcolors.OKBLUE}Maximum clique(s) approximation for graph 1:{bcolors.ENDC}')
        cliques = g1.approx_maximum_cliques()
        for c in cliques:
            print_clique_and_matrix(g1.adjacency_matrix, c)
        

    if args.graph2:
        # with open(str(sys.argv[1]), 'r') as f:
        print("MultiDiGraph 2:")
        g2 = MultiDiGraph(read_graph_from_file(args.graph2))
        g2.print()
    else:
        if args.distance or args.subgraph or args.approx_distance or args.approx_subgraph:
            print('No graph data file for 2nd graph given!')
        exit()

    if args.distance_l1:
        print("Distance between graph 1 and graph 2:")
        # Finding maximum subgraph
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
        # Calculating the L1 norm of subgraph's size
        subgraph_size_norm = maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1]

        # Calculating the L1 norm of G1's size
        g1_size_norm = g1.size[0] + g1.size[1]
        # Calculating the L1 norm of G2's size
        g2_size_norm = g2.size[0] + g2.size[1]

        # Printing the distance between G1 and G2
        print(f"{1 - subgraph_size_norm/max(g1_size_norm, g2_size_norm)}")
        pass

    if args.approx_distance_l1:
        print("Distance approximation between graph 1 and graph 2:")
        # Finding maximum subgraph
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2, approximate=True)
        # Calculating the L1 norm of subgraph's size
        subgraph_size_norm = maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1]

        # Calculating the L1 norm of G1's size
        g1_size_norm = g1.size[0] + g1.size[1]
        # Calculating the L1 norm of G2's size
        g2_size_norm = g2.size[0] + g2.size[1]

        # Printing the distance between G1 and G2
        print(f"{1 - subgraph_size_norm/max(g1_size_norm, g2_size_norm)}")
        pass

    if args.distance_l2:
        print("Distance between graph 1 and graph 2:")
        # Finding maximum subgraph
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
        # Calculating the L2 norm of subgraph's size
        subgraph_size_norm = math.sqrt(maximum_subgraphs[0].size[0]*maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1]*maximum_subgraphs[0].size[1])

        # Calculating the L2 norm of G1's size
        g1_size_norm = math.sqrt(g1.size[0]*g1.size[0] + g1.size[1]*g1.size[1])
        # Calculating the L2 norm of G2's size
        g2_size_norm = math.sqrt(g2.size[0]*g2.size[0] + g2.size[1]*g2.size[1])

        # Printing the distance between G1 and G2
        print(f"{1 - subgraph_size_norm/max(g1_size_norm, g2_size_norm)}")
        pass

    if args.approx_distance_l2:
        print("Distance approximation between graph 1 and graph 2:")
        # Finding maximum subgraph
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2, approximate=True)
        # Calculating the L2 norm of subgraph's size
        subgraph_size_norm = math.sqrt(maximum_subgraphs[0].size[0]*maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1]*maximum_subgraphs[0].size[1])

        # Calculating the L2 norm of G1's size
        g1_size_norm = math.sqrt(g1.size[0] * g1.size[0] + g1.size[1] * g1.size[1])
        # Calculating the L2 norm of G2's size
        g2_size_norm = math.sqrt(g2.size[0] * g2.size[0] + g2.size[1] * g2.size[1])

        # Printing the distance between G1 and G2
        print(f"{1 - subgraph_size_norm/max(g1_size_norm, g2_size_norm)}")
        pass

    if args.subgraph:
        print("Maximum subgraph for graph 1 and graph 2:")
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
        print(f"number of maximum subgraphs: {len(maximum_subgraphs)}")
        maximum_subgraphs[0].print()
        pass

    if args.approx_subgraph:
        print("Maximum subgraph approximation for graph 1 and graph 2:")
        _, maximum_subgraphs = find_maximum_subgraphs(g1, g2, approximation=True)
        print(f"number of maximum subgraphs: {len(maximum_subgraphs)}")
        maximum_subgraphs[0].print()
        pass

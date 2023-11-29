from time import perf_counter
import numpy as np
from MultiDiGraph import MultiDiGraph
from typing import FrozenSet, Union


def are_edge_pairs_isomorphic(e1: dict, f1: dict, e2: dict, f2: dict) -> bool:
    """Returns true if pairs of edges e1-e2 and f1-f2 are isomorphic."""

    #  disconnected edges
    if (
            e1['v0'] != f1['v0'] and
            e1['v0'] != f1['vf'] and
            e1['vf'] != f1['v0'] and
            e1['vf'] != f1['vf'] and  # e1 and e2 are disconnected

            e2['v0'] != f2['v0'] and
            e2['v0'] != f2['vf'] and
            e2['vf'] != f2['v0'] and
            e2['vf'] != f2['vf']  # f1 and f2 are disconnected
    ):
        return True

    # connected through both vertices
    if (
            e1['v0'] == f1['vf'] and
            e1['vf'] == f1['v0'] and  # e1 and e2 have ends at the same vertices

            e2['v0'] == f2['vf'] and
            e2['vf'] == f2['v0']  # f1 and f2 have ends at the same vertices
    ):
        return True

    # connected through one vertex
    if (
            (
                    e1['vf'] == f1['vf'] and
                    e1['v0'] != f1['v0'] and

                    e2['vf'] == f2['vf'] and
                    e2['v0'] != f2['v0']
            ) or
            (
                    e1['v0'] == f1['v0'] and
                    e1['vf'] != f1['vf'] and

                    e2['v0'] == f2['v0'] and
                    e2['vf'] != f2['vf']
            ) or
            (
                    e1['vf'] == f1['v0'] and
                    e1['v0'] != f1['vf'] and

                    e2['vf'] == f2['v0'] and
                    e2['v0'] != f2['vf']
            ) or
            (
                    e1['v0'] == f1['vf'] and
                    e1['vf'] != f1['v0'] and

                    e2['v0'] == f2['vf'] and
                    e2['vf'] != f2['v0']
            )
    ):
        return True

    return False


def get_edge_graph_product(g1_edges: list[dict], g2_edges: list[dict]) -> MultiDiGraph:
    """Returns edge graph product based on the lists of edges of two graphs g1 and g2."""
    g1_edges_count = len(g1_edges)
    g2_edges_count = len(g2_edges)
    vertices_count = int(g1_edges_count * g2_edges_count)
    edge_graph_product = np.zeros(shape=(vertices_count, vertices_count))

    for i in range(g1_edges_count):  # maybe not all needs to be checked? we have some repetitions? or not?
        for j in range(g1_edges_count):
            if i == j:
                continue

            for k in range(g2_edges_count):
                for l in range(g2_edges_count):  # from k+1 ?
                    if k == l:
                        continue

                    v0 = i * g2_edges_count + k
                    vf = j * g2_edges_count + l

                    if edge_graph_product[v0][vf] != 1 or edge_graph_product[vf][v0] != 1:
                        if are_edge_pairs_isomorphic(g1_edges[i], g1_edges[j], g2_edges[k], g2_edges[l]):
                            edge_graph_product[v0][vf] = edge_graph_product[vf][v0] = 1  # epg is undirected

    return MultiDiGraph(edge_graph_product)


def get_subgraph_edges(clique: FrozenSet[int], di_graph1_edges: list[dict], di_graph2_edges: list[dict]) -> list[dict]:
    """Returns a list with subgraph edge mapping for g1 and g2."""
    subgraph_edges_map = []
    di_graph2_edges_count = len(di_graph2_edges)

    for vertex in clique:
        edge_g1_index = int(vertex / di_graph2_edges_count)
        edge_g2_index = vertex - di_graph2_edges_count * edge_g1_index
        subgraph_edges_map.append({
            'edge_g1': di_graph1_edges[edge_g1_index],
            'edge_g2': di_graph2_edges[edge_g2_index],
            'count': 1
        })

    return subgraph_edges_map


def get_multisubgraph_edges(
        subgraph_edges_map: list[dict], multi_di_graph1: np.array, multi_di_graph2: np.array) -> list[dict]:
    """Returns a list with subgraph edge mapping for m1 and m2."""
    for edge in subgraph_edges_map:
        e_count = multi_di_graph1[edge['edge_g1']['v0']][edge['edge_g1']['vf']]
        f_count = multi_di_graph2[edge['edge_g2']['v0']][edge['edge_g2']['vf']]
        edge['count'] = min(e_count, f_count)

    return subgraph_edges_map


def get_matrix_from_edges(subgraph_edges_map: list[dict], graph_num: int) -> np.array:
    """Returns a subgraph based on the given list of subgraph edges map."""
    subgraph_vertices = []
    for edge in subgraph_edges_map:
        subgraph_vertices.append(edge[f'edge_g{graph_num}']['v0'])
        subgraph_vertices.append(edge[f'edge_g{graph_num}']['vf'])

    subgraph_vertices_count = len(set(subgraph_vertices))
    sorted_subgraph_vertices = sorted(set(subgraph_vertices))
    matrix = np.zeros(shape=(subgraph_vertices_count, subgraph_vertices_count))

    for edge in subgraph_edges_map:
        v0 = sorted_subgraph_vertices.index(edge[f'edge_g{graph_num}']['v0'])
        vf = sorted_subgraph_vertices.index(edge[f'edge_g{graph_num}']['vf'])
        matrix[v0][vf] = edge['count']

    return matrix


def find_maximum_subgraphs(multi_di_graph1: MultiDiGraph, multi_di_graph2: MultiDiGraph, approximation: bool = False) -> \
        (float, Union[list[np.array], None]):
    """Returns maximum subgraphs of two graphs based on node count first, edge count second.

    Algorithm:
    1. Find edge product graph based on graphs g1 nad g2 (ignoring all 'extra' edges from input multigraphs)
    2. Find maximal cliques for the edge product graph
    3. Iterate over maximal cliques, for each clique:
        a) calculate the corresponding subgraph in g1/g2
           - if it is a duplicate of any current maximum subgraphs skip this clique
        b) calculate the multisubgraph and update the maximum subgraph list
    """

    # get graphs from multigraphs
    di_graph1 = MultiDiGraph(multi_di_graph1.get_graph_from_multigraph(multi_di_graph1.adjacency_matrix))
    di_graph2 = MultiDiGraph(multi_di_graph2.get_graph_from_multigraph(multi_di_graph2.adjacency_matrix))

    # get edges of both graphs
    di_graph1_edges = MultiDiGraph.get_list_of_edges(di_graph1.adjacency_matrix)
    di_graph2_edges = MultiDiGraph.get_list_of_edges(di_graph2.adjacency_matrix)

    if not di_graph1_edges or not di_graph2_edges:
        print("Subgraph does not exist.")
        return 0, None

    # find edge graph product
    edge_graph_product = get_edge_graph_product(di_graph1_edges, di_graph2_edges)

    # get all maximal cliques
    t1 = perf_counter()
    if approximation:
        exit("approximation not implemented")
    else:
        maximal_cliques = edge_graph_product.maximal_cliques()
    t2 = perf_counter()
    maximal_clique_finding_time = t2-t1
    # print(f"finding maximal cliques: {maximal_clique_finding_time}")
    # print(f"num of maximal cliques: {len(maximal_cliques)}")

    maximum_subgraphs = []
    max_size = (0, 0)

    # iterate through all cliques
    for clique in maximal_cliques:
        subgraph_edges_map = get_subgraph_edges(clique, di_graph1_edges, di_graph2_edges)

        for maximum_subgraph in maximum_subgraphs:  # check if the subgraph is not a duplicate
            if any(x != y for x, y in zip(maximum_subgraph['subgraph_edge_map'], subgraph_edges_map)):
                continue

        multisubgraph_edges_map = get_multisubgraph_edges(subgraph_edges_map, multi_di_graph1.adjacency_matrix,
                                                          multi_di_graph2.adjacency_matrix)

        multi_di_subgraph = MultiDiGraph(get_matrix_from_edges(multisubgraph_edges_map, 1))
        multi_di_subgraph2 = MultiDiGraph(get_matrix_from_edges(multisubgraph_edges_map, 2))

        if multi_di_subgraph.size != multi_di_subgraph2.size:  # for triangular and y subgraphs
            continue

        # update the maximum subgraphs list
        if multi_di_subgraph.size[0] > max_size[0] or \
                (multi_di_subgraph.size[0] == max_size[0] and multi_di_subgraph.size[1] > max_size[1]):
            maximum_subgraphs.clear()
            maximum_subgraphs.append({
                'subgraph_edge_map': subgraph_edges_map,
                'multisubgraph_edge_map': multisubgraph_edges_map,
                'multi_di_subgraph': multi_di_subgraph
            })
            max_size = multi_di_subgraph.size

        if multi_di_subgraph.size == max_size:
            maximum_subgraphs.append({
                'subgraph_edge_map': subgraph_edges_map,
                'multisubgraph_edge_map': multisubgraph_edges_map,
                'multi_di_subgraph': multi_di_subgraph
            })

    result = []
    for maximum_subgraph in maximum_subgraphs:
        result.append(maximum_subgraph['multi_di_subgraph'])
    return maximal_clique_finding_time, result

from time import perf_counter
import numpy as np
from MultiDiGraph import MultiDiGraph
from typing import FrozenSet, Union, List, Tuple


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


def get_edge_graph_product(g1_edges: List[dict], g2_edges: List[dict]) -> MultiDiGraph:
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

    return MultiDiGraph(edge_graph_product, remove_isolated_vertices=False)


def get_subgraph_edges(clique: FrozenSet[int], di_graph1_edges: List[dict], di_graph2_edges: List[dict]) -> List[dict]:
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
        subgraph_edges_map: List[dict], multi_di_graph1: np.array, multi_di_graph2: np.array) -> List[dict]:
    """Returns a list with subgraph edge mapping for m1 and m2."""
    for edge in subgraph_edges_map:
        e_count = multi_di_graph1[edge['edge_g1']['v0']][edge['edge_g1']['vf']]
        f_count = multi_di_graph2[edge['edge_g2']['v0']][edge['edge_g2']['vf']]
        edge['count'] = min(e_count, f_count)

    return subgraph_edges_map


def get_matrix_from_edges(subgraph_edges_map: List[dict], graph_num: int) -> np.array:
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


def remove_duplicated(maximum_subgraphs: list) -> list:
    result = []
    for maximum_subgraph in maximum_subgraphs:
        if len(result) == 0:
            result.append(maximum_subgraph)
            continue

        duplicate = False
        for res in result:
            if res['multisubgraph_edge_map'] == maximum_subgraph['multisubgraph_edge_map']:
                duplicate = True
                continue

        if not duplicate:
            result.append(maximum_subgraph)

    return result


def get_subgraph_vertices_map(subgraph_edges_map: list[dict], graph_num: int) -> list[dict]:
    subgraph1_vertices = []
    for edge in subgraph_edges_map:
        subgraph1_vertices.append(edge[f'edge_g{graph_num}']['v0'])
        subgraph1_vertices.append(edge[f'edge_g{graph_num}']['vf'])

    sorted_subgraph_vertices = sorted(set(subgraph1_vertices))
    second_graph_num = 2 if graph_num == 1 else 1

    subgraph_vertices_map = []
    for subgraph_vertex in sorted_subgraph_vertices:
        second_graph_vertex = ""

        for edge in subgraph_edges_map:
            if edge[f'edge_g{graph_num}']['v0'] == subgraph_vertex:
                second_graph_vertex = edge[f'edge_g{second_graph_num}']['v0']
                break
            if edge[f'edge_g{graph_num}']['vf'] == subgraph_vertex:
                second_graph_vertex = edge[f'edge_g{second_graph_num}']['vf']
                break

        subgraph_vertices_map.append({
            'v_subgraph_index': sorted_subgraph_vertices.index(subgraph_vertex),
            f'v_graph_{graph_num}_index': subgraph_vertex,
            f'v_graph_{second_graph_num}_index': second_graph_vertex
        })

    return subgraph_vertices_map


def get_printible_vertex_map(multisubgraph_vertex_map: list[dict]) -> list[list]:
    vertex_map = []
    for v_map in multisubgraph_vertex_map:
        vertex_map.append([v_map['v_subgraph_index'], v_map['v_graph_1_index'], v_map['v_graph_2_index']])

    return vertex_map


def get_graph_vertices(subgraph_edges_map: list[dict], graph_num: int) -> set:
    subgraph_vertices = []
    for edge in subgraph_edges_map:
        subgraph_vertices.append(edge[f'edge_g{graph_num}']['v0'])
        subgraph_vertices.append(edge[f'edge_g{graph_num}']['vf'])

    return set(sorted(set(subgraph_vertices)))


def get_multigraph_with_only_subgraph_edges(graph_size: int, edge_map: dict, graph_num: int) -> np.array:
    matrix = np.zeros((graph_size, graph_size), dtype=int)
    for edge in edge_map:
        v0 = edge[f'edge_g{graph_num}']['v0']
        vf = edge[f'edge_g{graph_num}']['vf']
        matrix[v0][vf] = edge['count']

    return matrix


def find_maximum_subgraphs(multi_di_graph1: MultiDiGraph, multi_di_graph2: MultiDiGraph, approximate: bool = False) \
        -> Tuple[float, Union[List[np.array], None]]:
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
    if approximate:
        maximal_cliques = edge_graph_product.approx_maximal_cliques()
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

        di_subgraph = MultiDiGraph(get_matrix_from_edges(subgraph_edges_map, 1))
        di_subgraph2 = MultiDiGraph(get_matrix_from_edges(subgraph_edges_map, 2))

        if di_subgraph.size != di_subgraph2.size:  # for triangular and y subgraphs
            continue

        for maximum_subgraph in maximum_subgraphs:  # check if the subgraph is not a duplicate
            if any(x != y for x, y in zip(maximum_subgraph['subgraph_edge_map'], subgraph_edges_map)):
                continue

        multisubgraph_edges_map = get_multisubgraph_edges(subgraph_edges_map, multi_di_graph1.adjacency_matrix,
                                                          multi_di_graph2.adjacency_matrix)

        multi_di_subgraph = MultiDiGraph(get_matrix_from_edges(multisubgraph_edges_map, 1))
        multisubgraph_vertices_map = get_subgraph_vertices_map(multisubgraph_edges_map, 1)

        # update the maximum subgraphs list
        if multi_di_subgraph.size[0] > max_size[0] or \
                (multi_di_subgraph.size[0] == max_size[0] and multi_di_subgraph.size[1] > max_size[1]):
            maximum_subgraphs.clear()
            maximum_subgraphs.append({
                'subgraph_edge_map': subgraph_edges_map,
                'multisubgraph_edge_map': multisubgraph_edges_map,
                'multisubgraph_vertex_map': multisubgraph_vertices_map,
                'multi_di_subgraph': multi_di_subgraph
            })
            max_size = multi_di_subgraph.size

        if multi_di_subgraph.size == max_size:
            maximum_subgraphs.append({
                'subgraph_edge_map': subgraph_edges_map,
                'multisubgraph_edge_map': multisubgraph_edges_map,
                'multisubgraph_vertex_map': multisubgraph_vertices_map,
                'multi_di_subgraph': multi_di_subgraph
            })

    maximum_subgraphs = remove_duplicated(maximum_subgraphs)

    result = []
    for maximum_subgraph in maximum_subgraphs:
        result.append({
            'multi_di_subgraph': maximum_subgraph['multi_di_subgraph'],
            'multisubgraph_vertex_map': maximum_subgraph['multisubgraph_vertex_map'],
            'printable_vertex_map': get_printible_vertex_map(maximum_subgraph['multisubgraph_vertex_map']),
            'graph_1_vertices': get_graph_vertices(maximum_subgraph['multisubgraph_edge_map'], 1),
            'graph_2_vertices': get_graph_vertices(maximum_subgraph['multisubgraph_edge_map'], 2),
            'graph_1_with_only_subgraph_edges': get_multigraph_with_only_subgraph_edges(
                multi_di_graph1.size[0], maximum_subgraph['multisubgraph_edge_map'], 1),
            'graph_2_with_only_subgraph_edges': get_multigraph_with_only_subgraph_edges(
                multi_di_graph2.size[0], maximum_subgraph['multisubgraph_edge_map'], 2)
        })
    return maximal_clique_finding_time, result

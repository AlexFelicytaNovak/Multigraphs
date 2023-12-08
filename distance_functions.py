import math
from time import perf_counter

import MultiDiGraph
from maximum_subgraph import find_maximum_subgraphs


def distance_l1(g1: MultiDiGraph, g2: MultiDiGraph) -> (float, float):
    # Finding maximum subgraph
    t1 = perf_counter()
    _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
    t2 = perf_counter()
    maximum_subgraph_finding_time = t2 - t1

    # Calculating the L1 norm of subgraph's size
    subgraph_size_norm = maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1]

    # Calculating the L1 norm of G1's size
    g1_size_norm = g1.size[0] + g1.size[1]
    # Calculating the L1 norm of G2's size
    g2_size_norm = g2.size[0] + g2.size[1]

    # Calculating the distance between G1 and G2
    distance = 1 - subgraph_size_norm / max(g1_size_norm, g2_size_norm)
    return distance, maximum_subgraph_finding_time


def approx_distance_l1(g1: MultiDiGraph, g2: MultiDiGraph) -> (float, float):
    # Finding maximum subgraph
    t1 = perf_counter()
    _, maximum_subgraphs = find_maximum_subgraphs(g1, g2, approximate=True)
    t2 = perf_counter()
    maximum_subgraph_finding_time = t2 - t1

    # Calculating the L1 norm of subgraph's size
    subgraph_size_norm = maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1]

    # Calculating the L1 norm of G1's size
    g1_size_norm = g1.size[0] + g1.size[1]
    # Calculating the L1 norm of G2's size
    g2_size_norm = g2.size[0] + g2.size[1]

    # Calculating the distance between G1 and G2
    distance = 1 - subgraph_size_norm / max(g1_size_norm, g2_size_norm)
    return distance, maximum_subgraph_finding_time


def distance_l2(g1: MultiDiGraph, g2: MultiDiGraph) -> (float, float):
    # Finding maximum subgraph
    t1 = perf_counter()
    _, maximum_subgraphs = find_maximum_subgraphs(g1, g2)
    t2 = perf_counter()
    maximum_subgraph_finding_time = t2 - t1

    # Calculating the L2 norm of subgraph's size
    subgraph_size_norm = math.sqrt(
        maximum_subgraphs[0].size[0] * maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1] *
        maximum_subgraphs[0].size[1])

    # Calculating the L2 norm of G1's size
    g1_size_norm = math.sqrt(g1.size[0] * g1.size[0] + g1.size[1] * g1.size[1])
    # Calculating the L2 norm of G2's size
    g2_size_norm = math.sqrt(g2.size[0] * g2.size[0] + g2.size[1] * g2.size[1])

    # Calculating the distance between G1 and G2
    distance = 1 - subgraph_size_norm / max(g1_size_norm, g2_size_norm)
    return distance, maximum_subgraph_finding_time


def approx_distance_l2(g1: MultiDiGraph, g2: MultiDiGraph) -> (float, float):
    # Finding maximum subgraph
    t1 = perf_counter()
    _, maximum_subgraphs = find_maximum_subgraphs(g1, g2, approximate=True)
    t2 = perf_counter()
    maximum_subgraph_finding_time = t2 - t1

    # Calculating the L2 norm of subgraph's size
    subgraph_size_norm = math.sqrt(
        maximum_subgraphs[0].size[0] * maximum_subgraphs[0].size[0] + maximum_subgraphs[0].size[1] *
        maximum_subgraphs[0].size[1])

    # Calculating the L2 norm of G1's size
    g1_size_norm = math.sqrt(g1.size[0] * g1.size[0] + g1.size[1] * g1.size[1])
    # Calculating the L2 norm of G2's size
    g2_size_norm = math.sqrt(g2.size[0] * g2.size[0] + g2.size[1] * g2.size[1])

    # Calculating the distance between G1 and G2
    distance = 1 - subgraph_size_norm / max(g1_size_norm, g2_size_norm)
    return distance, maximum_subgraph_finding_time

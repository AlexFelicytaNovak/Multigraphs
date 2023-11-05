import numpy as np
from multidigraph import MultiDiGraph


def read_graph_from_file(filename: str) -> np.array:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    n = lines[0]
    rows = lines[1:-1]
    matrix = []
    for row in rows:
        matrix.append(row.split())

    return matrix


def get_graph_from_multigraph(multi_di_graph: np.array) -> np.array:
    di_graph = multi_di_graph.copy()
    di_graph[di_graph > 1] = 1
    print(di_graph)
    return di_graph


def get_undirected_graph_from_directed_graph(directed_graph: np.array) -> np.array:
    undirected_graph = directed_graph.copy()
    for i in range(0, len(undirected_graph)-1):  # TODO: if we can have loops end at len(undirected_graph)
        for j in range(i+1, len(undirected_graph)):  # TODO: if we can have loops start from i
            if undirected_graph[i][j] != 1 or undirected_graph[j][i] != 1:
                undirected_graph[i][j] = 0
                undirected_graph[j][i] = 0
    print(undirected_graph)
    return undirected_graph

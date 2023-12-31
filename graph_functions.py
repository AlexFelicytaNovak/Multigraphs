import random
import numpy as np
from sys import exit
from typing import FrozenSet, Set


def print_submat(matrix: np.array, subset: FrozenSet[int]) -> None:
    '''Prints matrix with all the entries except columns & rows in subset replaced with "." character. 

    Arguments:
        - matrix: matrix to print the entries from,
        - subset: subset of rows & columns to display.
    '''
    submat = matrix.astype(dtype=str, copy=True)
    complement = set(range(len(matrix)))
    complement = complement - subset

    # submat[np.ix_(list(complement), list(complement))] = '.'
    for index in complement:
        submat[index, :] = '.'
        submat[:, index] = '.'

    submat_str = submat.__str__()
    submat_str = submat_str.replace("'", '')
    submat_str = submat_str.replace(",", '')
    submat_str = submat_str.replace('None', '')
    print(submat_str)


def read_graph_from_file(filename: str) -> np.array:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    g_count = lines[0] 
    if int(g_count) != 1:
        print('Provide only files with single graph inside!')
        exit()

    n = lines[1]
    rows = lines[2:int(n)+2]
    matrix = []
    for row in rows:
        matrix.append(row.split())

    return np.array(matrix)


def is_symmetric(matrix: np.array) -> bool:
    """Check if given matrix is symmetric."""
    return (matrix.shape[0] == matrix.shape[1] and 
            np.all(np.abs(matrix - np.transpose(matrix)) == 0))


def get_neighbors(node: int, matrix: np.array) -> Set[int]:
    """Return set of neighbors for given node in graph defined by given matrix.

    Keyword arguments:
    node -- node index
    matrix -- adjacency matrix for undirected or directed graph
    """
    if (node < 0 or node >= len(matrix)):
        raise ValueError('Node does not exist in given graph')

    neighbors = set()
    it = np.nditer(matrix[node], flags=['f_index'])
    for col in it:
        if col > 0:
            neighbors.add(it.index)

    return neighbors
    

def bronKerbosch1(
        R: Set[int], P: Set[int], X: Set[int], matrix: np.array) -> Set[FrozenSet[int]]:
    """Recursive algorithm for finding all maximal cliques in undirected graphs.

    Keyword arguments:
        R -- required for recursive calls
        P -- required for recursive calls (first call with set of all vertices of the
                                           graph)
        X -- required for recursive calls
        matrix -- adjacency matrix for the undirected graph
    """
    # print(f'Call bronKerbosch1({R}, {P}, {X})')
    if not is_symmetric(matrix):
        raise ValueError('Input must be an undirected graph.')

    cliques = set()

    if len(P) == 0 and  len(X) == 0:
        cliques.add(frozenset(R))
        # print(f'Maximal clique size {len(R)}: {R}')

    for vertex in P:
        neighbors = get_neighbors(vertex, matrix)
        cliques = cliques | bronKerbosch1(
                R | set([vertex]), P & neighbors, X & neighbors, matrix)
        P = P - set([vertex])
        X = X | set([vertex])

    return cliques


"""
def bronKerbosch2(matrix: np.array) -> None: #List[np.array]:
    if not is_symmetric(matrix):
        raise ValueError('Input must be an undirected graph.')

    N = matrix.shape(0)
    print('shape is ', N)

    compsub = np.array(shape=(N))

    nodes = np.array(range(N))
    extend_V2(nodes, 0, N)
    

def extend_V2(old: np.array, ne: int, ce: int): #-> ?
    new = np.array(range(ce))
    nod: int
    fixp: int
    newne: int
    newce: int

    # Determine each counter value and look for minimum
    for 
"""


def get_graph_with_n_nodes_and_m_edges(n: int, m: int) -> np.array:
    """Returns a matrix of a graph with n nodes and m edges."""
    if n * n - n < m or m < 0 or n < 0:
        raise ValueError(f"Graph with {m} edges and {n} nodes cannot be created.")

    matrix = np.zeros(shape=(n, n))
    for edge in range(m):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        while i == j or matrix[i][j] == 1:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)

        matrix[i][j] = 1

    return matrix


def get_multigraph_from_graph(graph: np.array, max_num_of_edges: int) -> np.array:
    """Returns a matrix of a multigraph generated based on the given graph (multiplied edges)."""
    matrix = np.copy(graph)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 1:
                matrix[i][j] = random.randint(1, max_num_of_edges)

    return matrix


def greedy_single_maximal_clique(adjacency_matrix: np.array, starting_node: int) -> FrozenSet[int]:
    """Returns a maximal clique containing the starting_node.

    The order of adding nodes from the graph is random, thus it is not guaranteed that
    the biggest maximal clique will be returned.
    """
    clique = set([starting_node])
    nodes = list(range(len(adjacency_matrix)))
    random.shuffle(nodes)
    for node in nodes:
        if node in clique:
            continue
        if all([adjacency_matrix[node, c_node] != 0 for c_node in clique]):
            clique.add(node)
    return frozenset(clique)


def print_clique_and_matrix(graph_matrix: np.array, clique: FrozenSet[int]) -> None:
    print(f"Vertex indices from original graph: {tuple(clique)}")
    print()
    print("Matrix of resultant graph:")
    print_submat(graph_matrix, clique)
    print()

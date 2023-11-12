import numpy as np
from typing import FrozenSet, Set


def read_graph_from_file(filename: str) -> np.array:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    n = lines[0]
    rows = lines[1:-1]
    matrix = []
    for row in rows:
        matrix.append(row.split())

    return matrix


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

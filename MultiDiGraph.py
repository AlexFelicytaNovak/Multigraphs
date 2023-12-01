from typing import Set, FrozenSet, Tuple, Union, List, cast
try:
    from typing import Literal # Since Python 3.8
except ImportError:
    from typing_extensions import Literal # Before Python 3.8
import numpy as np
from graph_functions import bronKerbosch1, greedy_single_maximal_clique


class MultiDiGraph:

    def __init__(self, matrix: np.array, remove_isolated_vertices: bool = True):
        if not MultiDiGraph.is_valid_multidigraph_matrix(matrix):
            _, msg = cast(Tuple[bool, str],
                          (MultiDiGraph.is_valid_multidigraph_matrix(input)))
            raise ValueError(f'Invalid matrix for directed multigraph: {msg}')

        self.adjacency_matrix = matrix.astype(int)
        # Removing isolated vertices in MultiDiGraph
        if remove_isolated_vertices:
            indecies = np.intersect1d(np.where(~self.adjacency_matrix.any(axis=0)), np.where(~self.adjacency_matrix.any(axis=1)))
            if len(indecies) > 0:
                print(f'Removing isolated vertices ({len(indecies)}) from multigraph')
            self.adjacency_matrix = np.delete(self.adjacency_matrix, indecies, axis=0)
            self.adjacency_matrix = np.delete(self.adjacency_matrix, indecies, axis=1)
        self._size = (len(self.adjacency_matrix),
                      MultiDiGraph.count_edges(self.adjacency_matrix))
        # self._size = Tuple(len(matrix), MultiDiGraph.edgeCount()))


    def print(self):
        print('Size = ' + str(self.size))
        print(self.adjacency_matrix)
        # [print(row) for row in self.adjacency_matrix] # that is for a list of lists


    @property
    def size(self) -> Tuple[int, int]: # TODO: perhaps NamedTuple?
        return self._size


    @staticmethod
    def count_edges(matrix: np.array) -> int:
        return np.sum(matrix)

    @staticmethod
    def get_list_of_edges(matrix: np.array) -> List[dict]:
        """Returns the list of edges for a matrix."""
        edges = []
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] >= 1:
                    edges.append(
                        {
                            'v0': i,
                            'vf': j
                        }
                    )
        return edges

    @staticmethod
    def get_graph_from_multigraph(multi_di_graph: np.array) -> np.array:
        """Returns a graph based on the given multigraph (no repeat edges)."""
        di_graph = multi_di_graph.copy()
        di_graph[di_graph > 1] = 1
        return di_graph


    @staticmethod
    def get_undirected_graph_from_directed_graph(directed_graph: np.array) -> np.array:
        """Returns an undirected graph based on the given directed graph (ignoring all edges v -> u,
        where there isn't a corresponding edge u -> v).
        """
        undirected_graph = directed_graph.copy()
        for i in range(len(undirected_graph) - 1):
            for j in range(i+1, len(undirected_graph)):
                if undirected_graph[i][j] != 1 or undirected_graph[j][i] != 1:
                    undirected_graph[i][j] = 0
                    undirected_graph[j][i] = 0
        return undirected_graph


    @staticmethod
    def is_valid_multidigraph_matrix(
            matrix: np.array) -> Union[bool, Tuple[Literal[False], str]]:
        """Returns true if supplied matrix is a valid adjacency matrix for a directed
        multigraph.

        A matrix is considered valid if:
        1. it is 2-dimensional and,
        2. it is square and,
        3. it has non-negative entries and.
        """
        if len(matrix.shape) != 2:
            return (False, "Matrix is not 2-dimensional.")
        elif matrix.shape[0] != matrix.shape[1]:
            return (False, "Matrix is non-square.")
        elif not np.all(matrix.astype(int) >= 0):
            return (False, "Matrix has negative elements.")
        else:
            return True


    # TODO
    @staticmethod
    def distance(source, destination):
        raise NotImplementedError


    def approx_maximal_cliques(self) -> Set[FrozenSet[int]]:
        """Returns the approximation of maximum clique."""
        cliques = set()
        nodes, _ = self._size

        # Extract the embedded undirected graph O(n^2)
        undir_g = MultiDiGraph.get_undirected_graph_from_directed_graph(
                MultiDiGraph.get_graph_from_multigraph(self.adjacency_matrix))

        # For each vertex calculate one maximal clique that contains it O(n^3)
        for vertex in range(nodes):
            cliques.add(greedy_single_maximal_clique(undir_g, vertex))
        
        return cliques


    def maximum_cliques(self) -> Set[FrozenSet[int]]:
        """Returns the maximum cliques based on node count first, edge count second.

        Algorithm:
        1. Find the maximal clique(s) in the embedded graph (using bron-Kerbosch V.1).
        2. Filter for maximum cliques in the embedded graph.
        3. Filter for the ones that give the highest number of edges.
        """
        cliques = self.maximal_cliques()

        # Extract maximum clique(s)
        max_c_size = max(map(lambda set: len(set), cliques))
        maximum_cliques = set([c for c in cliques if len(c) == max_c_size])
        
        # Extract the clique(s) with max number of edges
        max_candidates = set()
        max_edge_count = -1

        for clique in maximum_cliques:
            c_matrix = self.adjacency_matrix[np.ix_(list(clique), list(clique))]
            edge_count = MultiDiGraph.count_edges(c_matrix)

            # print(f'Size {edge_count}, clique: {clique}')
            if edge_count > max_edge_count:
                max_candidates.clear()
                max_candidates.add(clique)
                max_edge_count = edge_count
            elif edge_count == max_edge_count:
                max_candidates.add(clique)
            # print(f'Current candidates {max_candidates}')

        return max_candidates


    def maximal_cliques(self) -> Set[FrozenSet[int]]:
        """Returns all maximal cliques from a multigraph.

        Algorithm:
        1. Extract from adjacency matrix embedded undirected graph. Edge pair
        (x -> y, y -> x) in the directed graph corresponds to (x -- y) in the
        undirected graph.
        2. Find the maximal clique(s) in the embedded graph (using bron-Kerbosch V.1).
        """
        # Extract the embedded undirected graph
        undir_g = MultiDiGraph.get_undirected_graph_from_directed_graph(
                MultiDiGraph.get_graph_from_multigraph(self.adjacency_matrix))

        # Find maximal cliques in the embedded graph
        # TODO: use 2nd version of Bron-Kerbosch for efficiency 
        cliques = bronKerbosch1(set(), set(range(len(undir_g))), set(), undir_g)
        return cliques


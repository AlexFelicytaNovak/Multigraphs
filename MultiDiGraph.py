from typing import Set, FrozenSet, Tuple, Union, cast
try:
    from typing import Literal # Since Python 3.8
except ImportError:
    from typing_extensions import Literal # Before Python 3.8
import numpy as np
from graph_functions import bronKerbosch1


class MultiDiGraph:

    def __init__(self, matrix: np.array):
        if not MultiDiGraph.is_valid_multidigraph_matrix(matrix):
            _, msg = cast(Tuple[bool, str],
                          (MultiDiGraph.is_valid_multidigraph_matrix(input)))
            raise ValueError(f'Invalid matrix for directed multigraph: {msg}')

        self.adjacency_matrix = matrix.astype(int)
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
    def get_graph_from_multigraph(multi_di_graph: np.array) -> np.array:
        di_graph = multi_di_graph.copy()
        di_graph[di_graph > 1] = 1
        # print(di_graph)
        return di_graph


    @staticmethod
    def get_undirected_graph_from_directed_graph(directed_graph: np.array) -> np.array:
        undirected_graph = directed_graph.copy()
        for i in range(len(undirected_graph) - 1):  # TODO: if we can have loops end at len(undirected_graph)
            for j in range(i+1, len(undirected_graph)):  # TODO: if we can have loops start from i
                if undirected_graph[i][j] != 1 or undirected_graph[j][i] != 1:
                    undirected_graph[i][j] = 0
                    undirected_graph[j][i] = 0
        # print(undirected_graph)
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
    

    # TODO
    def approx_maximal_clique(self):
        raise NotImplementedError


    # TODO
    def maximal_cliques(self) -> Set[FrozenSet[int]]:
        """Returns the maximal cliques based on node count first, edge count second.

        Algorithm:
        1. Extract from adjacency matrix embedded undirected graph. Edge pair
        (x -> y, y -> x) in the directed graph corresponds to (x -- y) in the
        undirected graph.
        2. Find the maximum clique(s) in the embedded graph (using bron-Kerbosch V.1).
        3. Filter for the ones that give the highest number of edges.
        """
        # Extract the embedded undirected graph
        undir_g = MultiDiGraph.get_undirected_graph_from_directed_graph(
                MultiDiGraph.get_graph_from_multigraph(self.adjacency_matrix))

        # Put ones on the diagonal
        #for i in range(len(undir_g)):
        #    undir_g[i, i] = 1

        # print('BK Input:')
        # print(undir_g)

        # Find maximum clique(s) in the embedded graph
        # TODO: use 2nd version of Bron-Kerbosch for efficiency 
        cliques = bronKerbosch1(set(), set(range(len(undir_g))), set(), undir_g)

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


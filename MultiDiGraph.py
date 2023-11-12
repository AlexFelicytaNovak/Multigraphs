import numpy as np
from graph_functions import bronKerbosch1


class MultiDiGraph:

    def __init__(self, matrix):
        self.adjacency_matrix = np.array(matrix).astype(int) # = matrix ? Do we want a list of lists or a np.array
        self.size = len(self.adjacency_matrix) # TODO: what is the actual definiton of size?

    def print(self):
        print('Size = ' + str(self.size))
        print(self.adjacency_matrix)
        # [print(row) for row in self.adjacency_matrix] # that is for a list of lists

    # TODO
    @staticmethod
    def distance(source, destination):
        raise NotImplementedError

    # TODO
    def approx_maximal_clique(self):
        raise NotImplementedError


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


    # TODO
    """
    Algorithm for finding cliques:
        1. Extract from adjacency matrix a corresponding embedded undirected graph.
            Edge pair (x -> y, y -> x) in the directed corresponds to (x -- y) in the
            undirected.
        2. Find the maximum clique(s) in the embedded graph (using bron-Kerbosch V.2).
            !!! The input graph needs to have 1s on the diagonal !!!
        3. For each of the above, check for the mapping that gives the highest number 
            of edges.
    """
    def maximal_cliques(self):
        # Extract the embedded undirected graph
        undir_g = MultiDiGraph.get_undirected_graph_from_directed_graph(
                MultiDiGraph.get_graph_from_multigraph(self.adjacency_matrix))

        # Put ones on the diagonal
        #for i in range(len(undir_g)):
        #    undir_g[i, i] = 1

        print('BK Input:')
        print(undir_g)

        # Find maximum clique(s) in the embedded graph
        # TODO: use 2nd version of Bron-Kerbosch for efficiency 
        cliques = bronKerbosch1(set(), set(range(len(undir_g))), set(), undir_g)
        
        # Check find mapping with the highest total number of edges
        raise NotImplementedError

    

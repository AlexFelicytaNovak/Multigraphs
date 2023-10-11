import sys
import numpy as np


class MultiDiGraph():

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
        pass

    # TODO
    def approx_maximal_clique(self):
        pass

    # TODO
    def maximal_clique(self):
        pass


if __name__ == '__main__':

    if len(sys.argv) == 2:

        with open(str(sys.argv[1]), 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        n = lines[0]
        rows = lines[1:-1]
        matrix = []
        for row in rows:
            matrix.append(row.split())

        
        g1 = MultiDiGraph(matrix)
        g1.print()
        
    else:
        print('No graph data file given!')

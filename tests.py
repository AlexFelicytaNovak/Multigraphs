import unittest
import numpy as np
from graph_functions import bronKerbosch1, get_neighbors, is_symmetric
from MultiDiGraph import MultiDiGraph


class TestCheckSymmetry(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng()


    def test_symmetric(self):
        """Should return true for symmetric input."""
        
        b = self.rng.integers(low=0, high=10, size=(10, 10))
        input = (b + b.T) / 2
        self.assertTrue(is_symmetric(input))


    def test_not_symmetric(self):
        """Should return false for not symmetric input."""

        b = self.rng.integers(low=0, high=10, size=(10, 10))
        input = (b + b.T) / 2
        input[5, 7] *= -1
        self.assertFalse(is_symmetric(input))


    def test_non_squre_matrix(self):
        """Should return false for non-square matrix."""
        input = np.array([
            [0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0]])
        self.assertFalse(is_symmetric(input))


class TestBronKerbosch1(unittest.TestCase):
    def setUp(self) -> None:
        self.sym_matrix = np.array([
            [0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0]])

        self.sym_matrix_2 = np.zeros(shape=(12, 12))
        self.sym_matrix_2[0, 1] = self.sym_matrix_2[1, 0] = 1
        self.sym_matrix_2[0, 2] = self.sym_matrix_2[2, 0] = 1
        self.sym_matrix_2[1, 2] = self.sym_matrix_2[2, 1] = 1
        self.sym_matrix_2[2, 3] = self.sym_matrix_2[3, 2] = 1
        self.sym_matrix_2[3, 4] = self.sym_matrix_2[4, 3] = 1
        self.sym_matrix_2[3, 5] = self.sym_matrix_2[5, 3] = 1
        self.sym_matrix_2[3, 6] = self.sym_matrix_2[6, 3] = 1
        self.sym_matrix_2[4, 5] = self.sym_matrix_2[5, 4] = 1
        self.sym_matrix_2[4, 6] = self.sym_matrix_2[6, 4] = 1
        self.sym_matrix_2[5, 6] = self.sym_matrix_2[6, 5] = 1
        self.sym_matrix_2[7, 8] = self.sym_matrix_2[8, 7] = 1
        self.sym_matrix_2[7, 9] = self.sym_matrix_2[9, 7] = 1
        self.sym_matrix_2[7, 10] = self.sym_matrix_2[10, 7] = 1
        self.sym_matrix_2[7, 11] = self.sym_matrix_2[11, 7] = 1
        self.sym_matrix_2[8, 9] = self.sym_matrix_2[9, 8] = 1
        self.sym_matrix_2[8, 10] = self.sym_matrix_2[10, 8] = 1
        self.sym_matrix_2[8, 11] = self.sym_matrix_2[11, 8] = 1
        self.sym_matrix_2[9, 10] = self.sym_matrix_2[10, 9] = 1
        self.sym_matrix_2[9, 11] = self.sym_matrix_2[11, 9] = 1
        self.sym_matrix_2[10, 11] = self.sym_matrix_2[11, 10] = 1


        self.not_sym_matrix = np.array([
            [0, 1, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1],
            [1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0]])


    def test_symmetric(self):
        """Should return set of maximal cliques for symmetric graph."""
        nodes = set(range(len(self.not_sym_matrix)))
        expected = set([frozenset([0, 1, 4]), frozenset([1, 2]), frozenset([2, 3]),
                        frozenset([3, 4]), frozenset([3, 5])])

        result = bronKerbosch1(set(), nodes, set(), self.sym_matrix)
        self.assertEqual(result, expected)


    def test_disconnected(self):
        """Should return set of maximal cliques for disconnected graph."""
        nodes = set(range(len(self.sym_matrix_2)))
        expected = set([frozenset([2,3]), frozenset([0, 1, 2]), frozenset([3, 4, 5, 6]),
                        frozenset([7, 8, 9, 10, 11])])

        result = bronKerbosch1(set(), nodes, set(), self.sym_matrix_2)
        self.assertEqual(result, expected)

    
    def test_not_symmetric(self):
        """Should raise ValueError on non-symmetric matrix."""
        nodes = set(range(len(self.not_sym_matrix)))
        self.assertRaises(
                ValueError, bronKerbosch1, set(), nodes, set(), self.not_sym_matrix)


class TestGetNeighbors(unittest.TestCase):
    def setUp(self) -> None:
        self.g_matrix = np.array([
            [0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0]])

        self.mg_matrix = np.array([
            [0, 0, 2, 0, 1],
            [0, 0, 1, 0, 0],
            [7, 1, 0, 0, 1],
            [0, 1, 2, 0, 1],
            [0, 0, 0, 4, 0]])


    def test_graph(self):
        """Should return correct set of neighbors for graph."""
        expected = set([1, 2, 4])
        result = get_neighbors(3, self.g_matrix)
        self.assertEqual(expected, result)


    def test_multigraph(self):
        """Should return correct set of neighbors for multigraph."""
        expected = set([0, 1, 4])
        result = get_neighbors(2, self.mg_matrix)
        self.assertEqual(expected, result)


    def test_isolated_node(self):
        """Should return empty set of neighbors for isolated node."""
        expected = set()
        result = get_neighbors(4, self.g_matrix)
        self.assertEqual(expected, result)


    def test_with_negative_node(self):
        """Should raise ValueError for negative node index."""
        self.assertRaises(ValueError, get_neighbors, -1, self.g_matrix)


    def test_with_too_large_node(self):
        """Should raise ValueError for node index above the greatest index."""
        self.assertRaises(ValueError, get_neighbors, len(self.g_matrix), self.g_matrix)


class TestMultiDiGraph(unittest.TestCase):
    def test_get_graph_from_multigraph(self):
        """Should return matrix with 1s in places of numbers > 1."""
        
        input = np.array([
            [0, 0, 2, 0, 1],
            [0, 0, 1, 0, 0],
            [7, 1, 0, 0, 1],
            [0, 1, 2, 0, 1],
            [0, 0, 0, 4, 0]])

        expected = np.array([
            [0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0]])
        
        result = MultiDiGraph.get_graph_from_multigraph(input)
        self.assertTrue(np.array_equal(result, expected))


    def test_get_undirected_graph_from_directed_graph(self):
        """ 
        Should return return a symmetric matrix with 1s at [i, j] & [j, i],
        if input has both 1s at those indices.
        """

        input = np.array([
            [0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0]])

        expected = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0]])

        result = MultiDiGraph.get_undirected_graph_from_directed_graph(input)
        self.assertTrue(np.array_equal(result, expected))


if __name__ == '__main__':
    unittest.main()

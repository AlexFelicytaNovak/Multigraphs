from typing import Tuple, cast
import unittest
import numpy as np
from MultiDiGraph import MultiDiGraph

class TestMultiDiGraphStaticMethods(unittest.TestCase):

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

    
    def test_is_valid_multidigraph_matrix_with_non_2d_matrix(self):
        input = np.array(range(32))
        input = np.reshape(a=input, newshape=(4, 4, 2))
        is_valid, msg = cast(Tuple[bool, str],
                             (MultiDiGraph.is_valid_multidigraph_matrix(input)))
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Matrix is not 2-dimensional.")

    
    def test_is_valid_multidigraph_matrix_with_non_square_matrix(self):
        input = np.array(range(24))
        input = np.reshape(a=input, newshape=(6, 4))
        is_valid, msg = cast(Tuple[bool, str],
                             (MultiDiGraph.is_valid_multidigraph_matrix(input)))
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Matrix is non-square.")


    def test_is_valid_multidigraph_matrix_with_negative_entry_matrix(self):
        input = np.array(range(36))
        input = np.reshape(a=input, newshape=(6, 6))
        input[2, 4] = -1
        is_valid, msg = cast(Tuple[bool, str],
                             (MultiDiGraph.is_valid_multidigraph_matrix(input)))
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Matrix has negative elements.")


    def test_is_valid_multidigraph_matrix_with_valid_directed_multigraph_matrix(self):
        input = np.array([
            [0, 0, 2, 0, 1],
            [0, 0, 1, 0, 0],
            [7, 1, 0, 0, 1],
            [0, 1, 2, 0, 1],
            [0, 0, 0, 4, 0]])
        self.assertTrue(MultiDiGraph.is_valid_multidigraph_matrix(input))


    def test_count_edges_for_matrix_with_no_edges(self):
        """Should return 0 for matrix with no edges."""
        input = np.zeros(shape=(6, 6))
        expected = 0
        result = MultiDiGraph.count_edges(input)
        self.assertEqual(result, expected)


    def test_count_edges_for_empty_matrix(self):
        """Should return 0 for empty matrix."""
        input = np.zeros(shape=(0))
        expected = 0
        result = MultiDiGraph.count_edges(input)
        self.assertEqual(result, expected)


    def test_count_edges_regular_matrix(self):
        """Should return correct edge count for multigraph matrix."""
        input = np.array([
            [0, 0, 2, 0, 1],
            [0, 0, 1, 0, 0],
            [7, 1, 0, 0, 1],
            [0, 1, 2, 0, 1],
            [0, 0, 0, 4, 0]])
        expected = 21
        result = MultiDiGraph.count_edges(input)
        self.assertEqual(result, expected)


class TestMultiDiGraphInstanceMethods(unittest.TestCase):
    def test_size_for_multigraph_with_no_edges(self):
        """Should return correct size for multigraph with no edges."""
        mdg = MultiDiGraph(np.zeros(shape=(6, 6)))
        expected = (6, 0)
        result = mdg.size
        self.assertEqual(result, expected)

    
    def test_size_for_empty_multigraph(self):
        """Should return correct size for empty multigraph."""
        mdg = MultiDiGraph(np.zeros(shape=(0)))
        expected = (0, 0)
        result = mdg.size
        self.assertEqual(result, expected)
        

    def test_size_regular_multigraph(self):
        """Should return correct size for multigraph."""
        mdg = MultiDiGraph(np.array([
            [0, 0, 2, 0, 1],
            [0, 0, 1, 0, 0],
            [7, 1, 0, 0, 1],
            [0, 1, 2, 0, 1],
            [0, 0, 0, 4, 0]]))
        expected = (5, 21)
        result = mdg.size
        self.assertEqual(result, expected)


    def test_maximal_cliques(self):
        """Should return correct maximum clique for a graph with 3 maximal cliques."""

        A = np.array([
            [0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 0, 1],
            [0, 1, 0, 2, 1, 0, 0, 2],
            [0, 3, 1, 0, 0, 0, 0, 2],
            [1, 0, 1, 0, 0, 3, 1, 0],
            [1, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1, 3, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0]])
        mg = MultiDiGraph(matrix=A)
        expected = set([frozenset([7, 1, 2, 3]), frozenset([0, 4, 5, 6]),
                        frozenset([2, 4])])
        result = mg.maximal_cliques()
        self.assertEqual(result, expected)


    def test_maximal_cliques_with_no_edges(self):
        """Should return set of singletons for graph with no edges."""

        A = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            ])
        mg = MultiDiGraph(matrix=A)
        expected = set([frozenset([2]), frozenset([1]), frozenset([0])])
        result = mg.maximal_cliques()
        self.assertEqual(result, expected)


    def test_maximum_cliques_with_exhaustive_maximum_clique(self):
        """Should return correct maximum clique - entire input graph."""

        A = np.array([
            [0, 1, 1, 3],
            [1, 0, 2, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 0]])
        mg = MultiDiGraph(matrix=A)
        expected = set([frozenset([0, 1, 2, 3])])
        result = mg.maximum_cliques()
        self.assertEqual(result, expected)


    def test_maximum_clique_with_multiple_maximum_cliques(self):
        """Should return the set  with 2 maximum cliques.
        """

        A = np.array([
            [0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 0, 1],
            [0, 1, 0, 2, 1, 0, 0, 2],
            [0, 3, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 3, 1, 0],
            [1, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1, 3, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0]])
        mg = MultiDiGraph(matrix=A)
        expected = set([frozenset([7, 1, 2, 3]), frozenset([0, 4, 5, 6])])
        result = mg.maximum_cliques()
        self.assertEqual(result, expected)


    def test_maximum_clique_with_edges(self):
        """Should return correct maximum clique for a graph with 2 maximal cliques
        with the same number of nodes, but different number of edges."""

        A = np.array([
            [0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 0, 0, 0, 1],
            [0, 1, 0, 2, 1, 0, 0, 2],
            [0, 3, 1, 0, 0, 0, 0, 2],
            [1, 0, 0, 0, 0, 3, 1, 0],
            [1, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1, 3, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0]])
        mg = MultiDiGraph(matrix=A)
        expected = set([frozenset([7, 1, 2, 3])])
        result = mg.maximum_cliques()
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()


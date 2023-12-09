from typing import Tuple, cast
import unittest
import numpy as np
from MultiDiGraph import MultiDiGraph
from graph_functions import read_graph_from_file

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
        Should return a symmetric matrix with 1s at [i, j] & [j, i],
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


    def test_get_list_of_edges_for_matrix_with_no_edges(self):
        """Should return empty list for matrix with no edges."""
        input = np.zeros(shape=(6, 6))
        expected = []
        result = MultiDiGraph.get_list_of_edges(input)
        self.assertEqual(result, expected)


    def test_get_list_of_edges_for_empty_matrix(self):
        """Should return empty list for empty matrix."""
        input = np.zeros(shape=(0))
        expected = []
        result = MultiDiGraph.get_list_of_edges(input)
        self.assertEqual(result, expected)


    def test_get_list_of_edges_regular_matrix(self):
        """Should return correct edges for multigraph matrix."""
        input = np.array([
            [0, 0, 2, 0],
            [0, 0, 1, 0],
            [7, 1, 0, 1],
            [0, 1, 2, 0]])
        expected = [
            {'v0': 0, 'vf': 2},
            {'v0': 1, 'vf': 2},
            {'v0': 2, 'vf': 0},
            {'v0': 2, 'vf': 1},
            {'v0': 2, 'vf': 3},
            {'v0': 3, 'vf': 1},
            {'v0': 3, 'vf': 2}
        ]
        result = MultiDiGraph.get_list_of_edges(input)

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


class TestMaximumCliques(unittest.TestCase):
    def setUp(self) -> None:
        self.g1 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g1_for_cliques.txt"))
        self.g2 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g2_for_cliques.txt"))
        self.g3 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g3_for_cliques.txt"))
        self.g4 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g4_for_cliques.txt"))
        return super().setUp()

    def test_on_g1(self):
        expected = set([
            # vertex numbering in svg file starts from 1 not 0,
            # so the correct vertices will be -1 here
            frozenset([6, 9, 10, 11]),
        ])
        result = self.g1.maximum_cliques()
        self.assertEqual(result, expected)

    def test_on_g2(self):
        expected = set([
            frozenset([2, 3, 5, 6]),
        ])
        result = self.g2.maximum_cliques()
        self.assertEqual(result, expected)
        
    def test_on_g3(self):
        expected = set([
            frozenset([3, 4, 5]),
        ])
        result = self.g3.maximum_cliques()
        self.assertEqual(result, expected)

    def test_on_g4(self):
        expected = set([
            frozenset([2, 3, 5]),
            frozenset([3, 4, 5]),
        ])
        result = self.g4.maximum_cliques()
        self.assertEqual(result, expected)

class TestMaximalCliques(unittest.TestCase):
    def setUp(self) -> None:
        self.g1 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g1_for_cliques.txt"))
        self.g2 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g2_for_cliques.txt"))
        self.g3 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g3_for_cliques.txt"))
        self.g4 = MultiDiGraph(read_graph_from_file(
            "./sample_graphs/g4_for_cliques.txt"))
        return super().setUp()

    def test_on_g1(self):
        expected = set([
            # vertex numbering in svg starts from 1 not 0,
            # so the correct vertices will be -1 here
            frozenset([6, 9, 10, 11]),
            frozenset([0, 1, 2, 3]),
            frozenset([4, 5, 6]),
            frozenset([2, 3, 5]),
            frozenset([3, 7]),
            frozenset([7, 8]),
            frozenset([4, 8]),
        ])
        result = self.g1.maximal_cliques()
        self.assertEqual(result, expected)

    def test_on_g2(self):
        expected = set([
            frozenset([2, 3, 5, 6]),
            frozenset([0, 1, 3, 4]),
            frozenset([1, 2, 3, 4]),
            frozenset([12, 13, 14]),
            frozenset([1, 7]),
            frozenset([7, 8]),
            frozenset([8, 9]),
            frozenset([10, 11]),
            frozenset([15]),
        ])
        result = self.g2.maximal_cliques()
        self.assertEqual(result, expected)

    def test_on_g3(self):
        expected = set([
            frozenset([3, 4, 5]),
            frozenset([0, 1, 2]),
            frozenset([7, 8, 9]),
            frozenset([2, 6]),
            frozenset([6, 10]),
            frozenset([11]),
            frozenset([12]),
        ])
        result = self.g3.maximal_cliques()
        self.assertEqual(result, expected)

    def test_on_g4(self):
        expected = set([
            frozenset([2, 3, 5]),
            frozenset([3, 4, 5]),
            frozenset([0, 1, 2]),
        ])
        result = self.g4.maximal_cliques()
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()


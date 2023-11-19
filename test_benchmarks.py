from time import strftime, gmtime, perf_counter
import unittest
from typing import TextIO
import numpy as np
from MultiDiGraph import MultiDiGraph
from bcolors import bcolors
from maximal_subgraph import find_maximal_subgraphs
from graph_functions import get_graph_with_n_nodes_and_m_edges, get_multigraph_from_graph


def maximal_subgraph_benchmark(edges: int, nodes: int, benchmark_type: str, g1: MultiDiGraph, g2: MultiDiGraph,
                               f: TextIO) -> None:
    print(f'======= BENCHMARK: {edges} EDGES {benchmark_type} =======')

    before = perf_counter()
    find_maximal_subgraphs(g1, g2)
    after = perf_counter()
    print(f' - Case passed in {bcolors.WARNING}{after - before}{bcolors.ENDC} s.\n')

    # log to file
    f.write(f'nodes: {nodes} - edges: {edges} - {benchmark_type}, {after - before};\n')


class TestBenchmarkMultiDiGraph(unittest.TestCase):

    def test_benchmark_maximum_cliques_1_to_20_nodes(self):
        """Run benchmarks for MultiDiGraphs 1 to n nodes.

        Specify upper limit of nodes by setting n"""
        n = 26

        with open(f'benchmark-run-{strftime("%y-%m-%d_%H_%M_%S", gmtime())}', 'w') as f:
            for nodes in range(1, n):
                print(f'======= BENCHMARK {nodes} NODES =======')
                A = np.ones(shape=(nodes, nodes))
                for i in range(nodes):
                    A[i][i] = 0
                print(' - Matrix initialized')
                
                mg = MultiDiGraph(matrix=A)
                expected = set([frozenset(range(nodes))])
                before = perf_counter()
                result = mg.maximal_cliques()
                after = perf_counter()

                self.assertEqual(result, expected)
                print(f' - Case passed in {bcolors.WARNING}{after - before}{bcolors.ENDC} s.\n')

                # log to file
                f.write(f'{nodes},{after - before};\n')

    def test_benchmark_maximal_subgraph(self):
        """Run benchmarks for maximal subgraphs of MultiDiGraphs with 1 to n edges (edges counted in graphs).

        Specify upper limit of edges (in a graph) by setting e
        Specify upper limit of duplicate edges in a multigraph by setting me
        Specify the number of nodes in the graphs by setting n"""

        e = 19
        me = 5
        n = 6

        with open(f'benchmark-run-{strftime("%y-%m-%d_%H_%M_%S", gmtime())}', 'w') as f:
            for edges in range(1, e):
                print(f'\n\n========================================')
                print(f'======= BENCHMARK: {edges} EDGES =======')

                g1 = MultiDiGraph(get_graph_with_n_nodes_and_m_edges(n, edges))
                g2 = MultiDiGraph(get_graph_with_n_nodes_and_m_edges(n, edges))
                m1 = MultiDiGraph(get_multigraph_from_graph(g1.adjacency_matrix, me))
                m2 = MultiDiGraph(get_multigraph_from_graph(g2.adjacency_matrix, me))

                print(' - Matrices initialized')

                maximal_subgraph_benchmark(edges, n, "same graph", g1, g1, f)
                maximal_subgraph_benchmark(edges, n, "same multigraph", m1, m1, f)
                maximal_subgraph_benchmark(edges, n, "different graphs", g1, g2, f)
                maximal_subgraph_benchmark(edges, n, "different multigraphs", m1, m2, f)


if __name__ == '__main__':
    unittest.main()

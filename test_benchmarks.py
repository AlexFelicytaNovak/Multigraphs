from time import strftime, gmtime, perf_counter
import unittest
from typing import TextIO
import numpy as np
from matplotlib import MatplotlibDeprecationWarning
from MultiDiGraph import MultiDiGraph
from bcolors import bcolors
from maximum_subgraph import find_maximum_subgraphs
from graph_functions import get_graph_with_n_nodes_and_m_edges, get_multigraph_from_graph
import matplotlib.pyplot as plt
import warnings


def maximum_subgraph_benchmark(edges: int, nodes: int, benchmark_type: str, g1: MultiDiGraph, g2: MultiDiGraph,
                               f: TextIO, approx: bool = False) -> (float, float):
    print(f'======= BENCHMARK: {edges} EDGES {benchmark_type} =======')

    before = perf_counter()
    if approx:
        cliques_finding_time, _ = find_maximum_subgraphs(g1, g2, approximate=True)
    else:
        cliques_finding_time, _ = find_maximum_subgraphs(g1, g2)
    after = perf_counter()
    print(f' - Case passed in {bcolors.WARNING}{after - before}{bcolors.ENDC} s.\n')

    # log to file
    f.write(f'nodes: {nodes} - edges: {edges} - {benchmark_type}, {after - before} (cliques finding time: '
            f'{cliques_finding_time});\n')
    return cliques_finding_time, after-before


class TestBenchmarkMultiDiGraph(unittest.TestCase):

    def test_benchmark_maximal_cliques_1_to_20_nodes(self):
        """Run benchmarks for MultiDiGraphs 1 to n nodes.

        Specify upper limit of nodes by setting n"""
        n = 13
        benchmark_data = []

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

                benchmark_data.append({
                    'time': after - before,
                    'nodes': nodes
                })

        warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)

        nodes = [entry['nodes'] for entry in benchmark_data]
        time = [entry['time'] for entry in benchmark_data]

        plt.figure(figsize=(10, 6))
        plt.plot(nodes, time, label='finding maximal cliques time')

        plt.title(f'Finding Maximum Cliques Benchmark')
        plt.xlabel('Number of Nodes')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'benchmark_maximum_cliques.png')
        plt.show()


    def test_benchmark_approx_maximal_cliques_1_to_n_nodes(self):
        """Run benchmarks for MultiDiGraphs 1 to n nodes.

        Specify upper limit of nodes by setting n"""
        n = 200
        benchmark_data = []

        with open(f'benchmark-run-{strftime("%y-%m-%d_%H_%M_%S", gmtime())}', 'w') as f:
            for nodes in range(1, n):
                print(f'======= BENCHMARK {nodes} NODES =======')
                A = np.ones(shape=(nodes, nodes))
                for i in range(nodes):
                    A[i][i] = 0
                print(' - Matrix initialized')
                
                mg = MultiDiGraph(matrix=A, remove_isolated_vertices=False)
                expected = set([frozenset(range(nodes))])
                before = perf_counter()
                result = mg.approx_maximal_cliques()
                after = perf_counter()

                self.assertEqual(result, expected)
                print(f' - Case passed in {bcolors.WARNING}{after - before}{bcolors.ENDC} s.\n')

                # log to file
                f.write(f'{nodes},{after - before};\n')

                benchmark_data.append({
                    'time': after - before,
                    'nodes': nodes
                })

        warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)

        nodes = [entry['nodes'] for entry in benchmark_data]
        time = [entry['time'] for entry in benchmark_data]

        plt.figure(figsize=(10, 6))
        plt.plot(nodes, time, label='finding approximate maximal cliques time')

        plt.title('Finding Approximate Maximal Cliques Benchmark')
        plt.xlabel('Number of Nodes')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'benchmark_maximum_cliques_approx.png')
        plt.show()


    def test_benchmark_maximum_subgraph(self):
        """Run benchmarks for maximum subgraphs of MultiDiGraphs with 1 to n edges (edges counted in graphs).

        Specify upper limit of edges (in a graph) by setting e
        Specify upper limit of duplicate edges in a multigraph by setting me
        Specify the number of nodes in the graphs by setting n"""

        e = 11
        me = 5
        n = 6

        benchmark_data = {
            'Same Graph': [],
            'Same Multigraph': [],
            'Different Graphs': [],
            'Different Multigraphs': []
        }

        with open(f'benchmark-run-{strftime("%y-%m-%d_%H_%M_%S", gmtime())}', 'w') as f:
            for edges in range(1, e):
                print(f'\n\n==============================================\n')
                print(f'======= BENCHMARK: {edges} EDGES =======')

                g1 = MultiDiGraph(get_graph_with_n_nodes_and_m_edges(n, edges))
                g2 = MultiDiGraph(get_graph_with_n_nodes_and_m_edges(n, edges))
                m1 = MultiDiGraph(get_multigraph_from_graph(g1.adjacency_matrix, me))
                m2 = MultiDiGraph(get_multigraph_from_graph(g2.adjacency_matrix, me))

                print(' - Matrices initialized\n\n')

                tsg1, tsg2 = maximum_subgraph_benchmark(edges, n, "same graph", g1, g1, f)
                tsm1, tsm2 = maximum_subgraph_benchmark(edges, n, "same multigraph", m1, m1, f)
                tdg1, tdg2 = maximum_subgraph_benchmark(edges, n, "different graphs", g1, g2, f)
                tdm1, tdm2 = maximum_subgraph_benchmark(edges, n, "different multigraphs", m1, m2, f)
                benchmark_data['Same Graph'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tsg1,
                    'whole_time': tsg2
                })

                benchmark_data['Same Multigraph'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tsm1,
                    'whole_time': tsm2
                })

                benchmark_data['Different Graphs'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tdg1,
                    'whole_time': tdg2
                })

                benchmark_data['Different Multigraphs'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tdm1,
                    'whole_time': tdm2
                })

        warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)
        for category, data in benchmark_data.items():
            edges = [entry['edges'] for entry in data]
            whole_time = [entry['whole_time'] for entry in data]
            finding_maximal_cliques_time = [entry['finding_maximal_cliques_time'] for entry in data]
            diff_time = [wt - fct for wt, fct in zip(whole_time, finding_maximal_cliques_time)]

            plt.figure(figsize=(10, 6))
            plt.plot(edges, whole_time, label='whole_time')
            plt.plot(edges, finding_maximal_cliques_time, label='finding_maximal_cliques_time')
            plt.plot(edges, diff_time, label='whole_time - finding_maximal_cliques_time')

            plt.title(f'{category} Benchmark')
            plt.xlabel('Number of Edges')
            plt.ylabel('Time (seconds)')
            plt.legend()
            plt.grid(True)
            plt.savefig(f'benchmark_maximum_subgraph_plot_{category.lower().replace(" ", "_")}.png')
            plt.show()


    def test_benchmark_approx_maximum_subgraph(self):
        """Run benchmarks for maximum subgraphs of MultiDiGraphs with 1 to n edges (edges counted in graphs).

        Specify upper limit of edges (in a graph) by setting e
        Specify upper limit of duplicate edges in a multigraph by setting me
        Specify the number of nodes in the graphs by setting n"""

        e = 25
        me = 10
        n = 8

        benchmark_data = {
            'Same Graph': [],
            'Same Multigraph': [],
            'Different Graphs': [],
            'Different Multigraphs': []
        }

        with open(f'benchmark-run-{strftime("%y-%m-%d_%H_%M_%S", gmtime())}', 'w') as f:
            for edges in range(1, e):
                print(f'\n\n==============================================\n')
                print(f'======= BENCHMARK: {edges} EDGES =======')

                g1 = MultiDiGraph(get_graph_with_n_nodes_and_m_edges(n, edges))
                g2 = MultiDiGraph(get_graph_with_n_nodes_and_m_edges(n, edges))
                m1 = MultiDiGraph(get_multigraph_from_graph(g1.adjacency_matrix, me))
                m2 = MultiDiGraph(get_multigraph_from_graph(g2.adjacency_matrix, me))

                print(' - Matrices initialized\n\n')

                tsg1, tsg2 = maximum_subgraph_benchmark(edges, n, "same graph", g1, g1, f, approx = True)
                tsm1, tsm2 = maximum_subgraph_benchmark(edges, n, "same multigraph", m1, m1, f, approx = True)
                tdg1, tdg2 = maximum_subgraph_benchmark(edges, n, "different graphs", g1, g2, f, approx = True)
                tdm1, tdm2 = maximum_subgraph_benchmark(edges, n, "different multigraphs", m1, m2, f, approx = True)
                benchmark_data['Same Graph'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tsg1,
                    'whole_time': tsg2
                })

                benchmark_data['Same Multigraph'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tsm1,
                    'whole_time': tsm2
                })

                benchmark_data['Different Graphs'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tdg1,
                    'whole_time': tdg2
                })

                benchmark_data['Different Multigraphs'].append({
                    'edges': edges,
                    'finding_maximal_cliques_time': tdm1,
                    'whole_time': tdm2
                })

        warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)
        for category, data in benchmark_data.items():
            edges = [entry['edges'] for entry in data]
            whole_time = [entry['whole_time'] for entry in data]
            finding_maximal_cliques_time = [entry['finding_maximal_cliques_time'] for entry in data]
            diff_time = [wt - fct for wt, fct in zip(whole_time, finding_maximal_cliques_time)]

            plt.figure(figsize=(10, 6))
            plt.plot(edges, whole_time, label='whole_time')
            plt.plot(edges, finding_maximal_cliques_time, label='finding_maximal_cliques_time')
            plt.plot(edges, diff_time, label='whole_time - finding_maximal_cliques_time')

            plt.title(f'{category} Benchmark')
            plt.xlabel('Number of Edges')
            plt.ylabel('Time (seconds)')
            plt.legend()
            plt.grid(True)
            plt.savefig(f'benchmark_approx_maximum_subgraph_plot_{category.lower().replace(" ", "_")}.png')
            plt.show()


if __name__ == '__main__':
    unittest.main()

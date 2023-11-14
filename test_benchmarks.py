from time import strftime, gmtime, perf_counter
import unittest
import numpy as np
from MultiDiGraph import MultiDiGraph
from bcolors import bcolors


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
                f.write(f'{nodes},{after-before};\n')


if __name__ == '__main__':
    unittest.main()


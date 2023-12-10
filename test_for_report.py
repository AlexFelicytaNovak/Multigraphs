from time import strftime, gmtime, perf_counter
import unittest
import random
import matplotlib.pyplot as plt
import numpy as np
from MultiDiGraph import MultiDiGraph
from bcolors import bcolors
import warnings
from matplotlib import MatplotlibDeprecationWarning

class TestMaximumCliqueForReport(unittest.TestCase):
    def test_meta_benchmark_on_complete_bipartite(self):
        meta = 10 
        n = 12 # number of multipartite groups

        benchmark_data = np.zeros(shape=(n - 2, 2))
        min_benchmark_data = np.full(shape=(n - 2), fill_value=np.infty)
        max_benchmark_data = np.zeros(shape=(n - 2))

        f = plt.figure(figsize=(10, 6))
        for m in range(meta):
            total_time = 0
            this_benchmark = np.zeros(shape=(n - 2))
            print(f'{bcolors.OKBLUE}=> META RUN {m + 1}{bcolors.ENDC}') 

            for groups in range(2, n):
                nodes = 3 * groups
                print(f'    -> {nodes} nodes: ', end="") 

                A = np.ones(shape=(nodes, nodes))
                for g in range(groups):
                    A[3*g:3*g+3, 3*g:3*g+3] = np.zeros(shape=(3, 3))

                mg = MultiDiGraph(matrix=A)

                before = perf_counter()
                result = mg.maximum_cliques()
                after = perf_counter()

                self.assertEqual(len(result), 3**groups)
                print(f'{bcolors.OKGREEN}{after - before}{bcolors.ENDC} s.')


                benchmark_data[groups - 2, 0] = nodes
                run = after - before
                benchmark_data[groups - 2, 1] += run
                this_benchmark[groups - 2] = run
                if min_benchmark_data[groups - 2] > run:
                    min_benchmark_data[groups - 2] = run
                if max_benchmark_data[groups - 2] < run:
                    max_benchmark_data[groups - 2] = run

                total_time += after - before

        

            total_time *= meta - (m + 1)
            print(f'=> Estimated remaining time: {bcolors.WARNING} {total_time // 60} minutes {total_time - (total_time // 60) * 60} seconds {bcolors.ENDC}')

        with open(f'benchmark-run-{strftime("%y-%m-%d_%H_%M_%S", gmtime())}', 'w') as f:
            for groups in range(0, n - 2):
                f.write(f'{benchmark_data[groups, 0]}, {benchmark_data[groups, 1] / meta};\n')

        warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)

        benchmark_data[:, 1] /= meta
        plt.plot(benchmark_data[:,0], benchmark_data[:,1], linewidth=2, label=f'Average time over {meta} runs')
        plt.fill_between(benchmark_data[:,0], min_benchmark_data, max_benchmark_data, color='tab:gray', alpha=0.5)

        plt.title('Finding Maximum Cliques Benchmark')
        plt.xlabel('Number of Nodes')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        plt.savefig('benchmark_maximum_cliques.png')
        #plt.show()

        plt.semilogy(benchmark_data[:,0], benchmark_data[:,1], linewidth=2, label=f'Logarithm of average time')
        plt.title('Finding Maximum Cliques Benchmark')
        plt.xlabel('Number of Nodes')
        plt.ylabel('Logarithm of time')
        plt.grid(True)
        plt.savefig('benchmark_maximum_cliques_semilog.png')
        #plt.show()

class TestMaximumCliqueApproxForReport(unittest.TestCase):
    def test_meta_accuracy_on_complete_bipartite(self):
        meta = 10 
        n = 31
        exact_rate = 0.0
        e_diff_rate = 0.0
        v_diff_rate = 0.0
        fail_rate = 0.0
        
        for m in range(meta):
            print(f'{bcolors.OKBLUE}=> META RUN {m + 1}{bcolors.ENDC}') 
            
            ok_counter = 0
            only_e_diff = 0
            v_diff_by_one = 0
            fail_counter = 0

            for nodes in range(2,n):
                A = np.random.randint(12, size=(nodes, nodes))
                for i in range(nodes):
                    A[i, i] = 0
                g = MultiDiGraph(A)
                approx = g.approx_maximum_cliques()
                exact = g.maximum_cliques()

                if(approx == exact):
                    ok_counter += 1
                elif (len(approx) == len(exact) and len(exact) == 1):
                    s = approx.pop()
                    e = exact.pop()
                    c_appr_matrix = g.adjacency_matrix[np.ix_(list(s), list(s))]
                    g_apr = MultiDiGraph(c_appr_matrix)
                    c_matrix = g.adjacency_matrix[np.ix_(list(e), list(e))]
                    g1 = MultiDiGraph(c_matrix)

                    if g1.size[0] - g_apr.size[0] == 0:
                        only_e_diff += 1
                    elif g1.size[0] - g_apr.size[0] == 1:
                        v_diff_by_one += 1
                    else:
                        fail_counter += 1
                else:
                    fail_counter += 1

            this_ok_rate = ok_counter / (n - 2)
            this_ed_rate = only_e_diff / (n - 2)
            this_vd_rate = v_diff_by_one / (n - 2)
            this_fail_rate = fail_counter / (n - 2)
            sum = this_ok_rate + this_ed_rate + this_vd_rate + this_fail_rate

            exact_rate += this_ok_rate 
            e_diff_rate += this_ed_rate 
            v_diff_rate += this_vd_rate 
            fail_rate += this_fail_rate

            print()
            print(f'    -> OK rate: {bcolors.OKGREEN}{ this_ok_rate} {bcolors.ENDC}')
            print(f'    -> E diff only rate: {bcolors.WARNING}{this_ed_rate} {bcolors.ENDC}')
            print(f'    -> V diff by one rate: {bcolors.WARNING}{this_vd_rate} {bcolors.ENDC}')
            print(f'    -> FAIL rate: {bcolors.FAIL}{this_fail_rate} {bcolors.ENDC}')
            print(f'    -> Sum is rate: {sum} ')

        print(f'\n{bcolors.OKBLUE}==== SUMMARY ===={bcolors.ENDC}') 
        print(f'OK rate: {bcolors.OKGREEN}{exact_rate / meta} {bcolors.ENDC}')
        print(f'E diff only rate: {bcolors.WARNING}{e_diff_rate / meta} {bcolors.ENDC}')
        print(f'V diff by one rate: {bcolors.WARNING}{v_diff_rate / meta} {bcolors.ENDC}')
        print(f'FAIL rate: {bcolors.FAIL}{fail_rate / meta} {bcolors.ENDC}')
        
        print(f'Sum is rate: {(exact_rate + e_diff_rate + v_diff_rate + fail_rate) / meta } ')

if __name__ == '__main__':
    unittest.main()


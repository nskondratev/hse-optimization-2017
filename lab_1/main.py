import os
from multiprocessing import Pool

import lab_1.util as util
import lab_1.algorithms as alg
from lab_1.constants import TEST_INSTANCES_DIR, SOLUTIONS_DIR

def apply_algorithms_to_instance(filename):
    print('==== Process file: {} ===='.format(filename))
    n, d, f = util.read_from_file(filename)
    print('[{}]: Read from file: n = {}, d.shape = {}, f.shape = {}'.format(filename, n, d.shape, f.shape))
    # initial solution
    initial_solution = util.build_random_solution(n)
    # local search
    sol, sol_obj = alg.local_search(initial_solution, n, d, f)
    print('[{}]: LS found solution: {}, objective func value = {}'.format(filename, sol, sol_obj))
    util.write_solution_to_file(filename, sol, dir='ls_{}'.format(SOLUTIONS_DIR))
    # repeated search
    sol, sol_obj = alg.repeated_local_search(initial_solution, n, d, f)
    print('[{}]: RLS found solution: {}, objective func value = {}'.format(filename, sol, sol_obj))
    util.write_solution_to_file(filename, sol, dir='rls_{}'.format(SOLUTIONS_DIR))
    # iterated search
    # number of components
    k = int(n / 3)
    sol, sol_obj = alg.iterated_local_search(initial_solution, k, n, d, f)
    print('[{}]: ILS found solution: {}, objective func value = {}'.format(filename, sol, sol_obj))
    util.write_solution_to_file(filename, sol, dir='ils_{}'.format(SOLUTIONS_DIR))
    # guided search
    # penalty parameter
    alpha = 10000
    sol, sol_obj = alg.guided_local_search(initial_solution, alpha, n, d, f)
    print('[{}]: GLS found solution: {}, objective func value = {}'.format(filename, sol, sol_obj))
    util.write_solution_to_file(filename, sol, dir='gls_{}'.format(SOLUTIONS_DIR))
    print('**** Finish working with file: {} ****'.format(filename))

if __name__ == '__main__':
    # Run algorithms on all test instances
    files = os.listdir(TEST_INSTANCES_DIR)
    pool = Pool()
    pool.map(apply_algorithms_to_instance, files)
    pool.close()
    pool.join()


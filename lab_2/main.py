from multiprocessing import Pool
import os
import numpy as np
from argparse import ArgumentParser

from lab_2.util import read_from_file, write_result_to_file, ensure_dir, logger
from lab_2.gvns import GVNS
from lab_2.rvns import RVNS
from lab_2.solution import Solution
from lab_2.local_search import *
from lab_2.shaking import *

TEST_INSTANCES_DIR = 'test_instances'
SOLUTIONS_DIR = 'solutions'


def apply_gvns(path_to_file):
    logger.info('[{}] Start processing file...'.format(path_to_file))
    # Shaking neighborhood
    shaking_neighborhood = [
        ShakingByRows,
        ShakingByColumns,
        ShakingByClustersSplitting,
        ShakingByClustersUnion
    ]
    # Local Search neighborhood
    ls_neighborhood = [
        LocalSearchByRows,
        LocalSearchByColumns,
        LocalSearchByClustersSplitting,
        LocalSearchByClustersUnion
    ]
    # Initial solution
    matrix = read_from_file(path_to_file)
    initial_solution = Solution.get_random_solution(matrix, clusters_count=2)
    max_clusters_count = min(initial_solution.m, initial_solution.p)
    for _ in range(IS_ITERATIONS):
        clusters_count = np.random.randint(2, max_clusters_count)
        tmp_solution = Solution.get_random_solution(matrix, clusters_count)
        if tmp_solution.is_better(initial_solution):
            initial_solution = tmp_solution.copy()
    logger.debug('[{}] Build random solution:\n{}'.format(path_to_file, initial_solution))
    # Improve initial solution by RVNS
    initial_solution = RVNS.solve(initial_solution, shaking_neighborhood, MAX_ITERATIONS=RVNS_ITERATIONS)
    logger.debug('[{}] Improved solution by RVNS:\n{}'.format(path_to_file, initial_solution))
    # Improve solution with GVNS
    final_solution = GVNS.solve(initial_solution, shaking_neighborhood, ls_neighborhood, MAX_ITERATIONS=GVNS_ITERATIONS)
    logger.debug('[{}] Get final solution:\n{}'.format(path_to_file, final_solution))
    # Write final solution in file
    path_to_res_file = os.path.join(SOLUTIONS_DIR,
                                    '{}_{}.sol'.format(os.path.basename(path_to_file).replace('.txt', ''),
                                                       final_solution.obj_val))
    write_result_to_file(path_to_res_file, final_solution)
    logger.info('[{}] Finished processing file.'.format(path_to_file))


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--rvns_iterations', type=int, default=500)
    parser.add_argument('--gvns_iterations', type=int, default=1000)
    parser.add_argument('--is_iterations', type=int, default=200)
    parser.add_argument('--mode', type=str, choices=['all', 'single'], default='all')
    parser.add_argument('--filename', type=str)
    parser.add_argument('--sf_iterations', type=int, default=10)
    return parser.parse_args()


def all_files(args):
    test_instances = [os.path.join(TEST_INSTANCES_DIR, x) for x in os.listdir(TEST_INSTANCES_DIR)]
    pool = Pool()
    pool.map(apply_gvns, test_instances)
    pool.close()
    pool.join()


def single_file(args):
    for i in range(args.sf_iterations):
        logger.debug('Single file iteration number: {}'.format(i))
        apply_gvns(args.filename)


if __name__ == '__main__':
    ensure_dir(SOLUTIONS_DIR)
    args = parse_args()
    RVNS_ITERATIONS = args.rvns_iterations or 500
    GVNS_ITERATIONS = args.gvns_iterations or 1000
    IS_ITERATIONS = args.is_iterations or 200
    logger.info('Iterations numbers: RVNS = {}, GVNS = {}, INITIAL_SOLUTION {}'.format(RVNS_ITERATIONS, GVNS_ITERATIONS,
                                                                                       IS_ITERATIONS))
    logger.info('Mode: {}'.format(args.mode))
    if args.mode == 'all':
        all_files(args)
    elif args.mode == 'single':
        single_file(args)

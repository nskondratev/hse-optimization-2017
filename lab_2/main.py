from multiprocessing import Pool
import os

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
    logger.debug('[{}] Build random solution:\n{}'.format(path_to_file, initial_solution))
    # Improve initial solution by RVNS
    initial_solution = RVNS.solve(initial_solution, shaking_neighborhood, MAX_ITERATIONS=100)
    logger.debug('[{}] Improved solution by RVNS:\n{}'.format(path_to_file, initial_solution))
    # Improve solution with GVNS
    final_solution = GVNS.solve(initial_solution, shaking_neighborhood, ls_neighborhood)
    logger.debug('[{}] Get final solution:\n{}'.format(path_to_file, initial_solution))
    # Write final solution in file
    path_to_res_file = os.path.join(SOLUTIONS_DIR, os.path.basename(path_to_file).replace('.txt', '') + '.sol')
    write_result_to_file(path_to_res_file, final_solution)
    logger.info('[{}] Finished processing file.'.format(path_to_file))


if __name__ == '__main__':
    ensure_dir(SOLUTIONS_DIR)
    test_instances = [os.path.join(TEST_INSTANCES_DIR, x) for x in os.listdir(TEST_INSTANCES_DIR)]
    pool = Pool()
    pool.map(apply_gvns, test_instances)
    pool.close()
    pool.join()

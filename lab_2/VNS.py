import lab_2.util as util
import lab_2.local_search as ls
import lab_2.shaking as sh
import numpy as np
from lab_2.util import logger

if __name__ == '__main__':
    test_filename = 'example_1.txt'
    matrix, m, p, n1 = util.read_from_file(test_filename)
    logger.debug(matrix)
    N = 2  # current number of clusters
    Nmax = 1
    perm_row = [x for x in range(m)]
    perm_col = [x for x in range(p)]
    # print(matrix, m, p)

    initial_matrix = matrix.copy()
    clusters_row, clusters_col = util.generate_random_solution(m, p)
    # clusters_row = [1, 1, 1, 2]
    # clusters_col = [1, 1, 1, 2, 2, 2, 2]
    obj_val = util.calc_obj_val(matrix, n1, clusters_row, clusters_col)
    logger.debug('Initial objective value: {}'.format(obj_val))

    best_obj = obj_val  # best objective value
    best_clusters = [clusters_row, clusters_col]

    '''
    # Example
    clusters_row, clusters_col = algorithms.split_random_cluster(clusters_row, clusters_col, N)
    N = N + 1

    clusters_row, clusters_col = algorithms.union_two_random_clusters(clusters_row, clusters_col, N)
    N = N - 1
    '''
    # shake rows
    matrix = sh.by_rows(matrix, m, p, perm_row)

    # local search row
    res = 0
    while res != -1:
        res = ls.by_rows(matrix, n1, m, p, clusters_row, clusters_col, perm_row)
        if res != -1:
            matrix = res[0]
            clusters_row = res[2]
            clusters_col = res[3]
            if res[1] > best_obj:
                best_obj = res[1]
                best_clusters = [clusters_row.copy(), clusters_col.copy()]
                best_perm = [perm_row.copy(), perm_col.copy()]
                logger.debug('Improved objective value: {}'.format(res[1]))
        else:
            logger.debug('Cannot improve current solution')

    # shake columns
    matrix = sh.by_columns(matrix, m, p, perm_col)

    # local search column
    res = 0
    while res != - 1:
        res = ls.by_columns(matrix, n1, m, p, clusters_row, clusters_col, perm_col)
        if res != -1:
            matrix = res[0]
            clusters_row = res[2]
            clusters_col = res[3]
            if (res[1] > best_obj):
                best_obj = res[1]
                best_clusters = [clusters_row.copy(), clusters_col.copy()]
                best_perm = [perm_row.copy(), perm_col.copy()]
                logger.debug('Improved objective value: {}'.format(res[1]))
        else:
            logger.debug('Cannot improve current solution')

    # shake split
    res = sh.by_clusters_splitting(clusters_row, clusters_col, N)
    if (res != -1):
        clusters_row, clusters_col = res
        N = N + 1
    else:
        logger.debug('Cannot split clusters')

    # local search split
    res = 0
    while res != - 1:
        res = ls.by_clusters_splitting(matrix, n1, m, p, clusters_row, clusters_col, N)
        if (res != -1):
            matrix = res[0]
            clusters_row = res[2]
            clusters_col = res[3]
            if (res[1] > best_obj):
                best_obj = res[1]
                best_clusters = [clusters_row.copy(), clusters_col.copy()]
                best_perm = [perm_row.copy(), perm_col.copy()]
                logger.debug('Improved objective value:', res[1])
                N = N + 1
        else:
            logger.debug('Cannot improve current solution')

    # shake union
    res = sh.by_clusters_union(clusters_row, clusters_col, N)
    if (res != -1):
        clusters_row, clusters_col = res
        N = N - 1
    else:
        logger.debug('Cannot union clusters')

    # local search split
    res = 0
    while res != - 1:
        res = ls.by_clusters_union(matrix, n1, m, p, clusters_row, clusters_col, N)
        if res != -1:
            matrix, cur_obj, clusters_row, clusters_col = res
            if (cur_obj > best_obj):
                best_obj = cur_obj
                best_clusters = [clusters_row.copy(), clusters_col.copy()]
                best_perm = [perm_row.copy(), perm_col.copy()]
                logger.debug('Improved objective value:', cur_obj)
                N = N - 1
        else:
            logger.debug('Cannot improve current solution')

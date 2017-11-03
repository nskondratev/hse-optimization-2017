import lab_2.util as util
import lab_2.algorithms as algorithms
import numpy as np

if __name__ == '__main__':
    test_filename = 'example_1.txt'
    matrix, m, p, n1 = util.read_from_file(test_filename)
    N = 2 #current number of clusters
    Nmax = 1
    perm_row = [x for x in range(m)]
    perm_col = [x for x in range(p)]
    #print(matrix, m, p)

    initial_matrix = matrix.copy()
    clusters_row, clusters_col = util.generate_initial_solution(m, p)
    #clusters_row = [1, 1, 1, 2]
    #clusters_col = [1, 1, 1, 2, 2, 2, 2]
    obj_val = util.objective_function(matrix, n1, clusters_row, clusters_col)
    print('Initial objective value:', obj_val)

    best_obj = obj_val  # best objective value
    best_clusters = [clusters_row, clusters_col]

    '''
    # Example
    clusters_row, clusters_col = algorithms.split_random_cluster(clusters_row, clusters_col, N)
    N = N + 1

    clusters_row, clusters_col = algorithms.union_two_random_clusters(clusters_row, clusters_col, N)
    N = N - 1
    '''
    #shake rows
    matrix = algorithms.shaking_row(matrix, m, p, perm_row)

    #local search row
    res = 0
    while(res != -1):
       res = algorithms.local_search_move_row(matrix, n1, m, p, clusters_row, clusters_col, perm_row)
       if (res != -1):
         matrix = res[0]
         clusters_row = res[2]
         clusters_col = res[3]
         if (res[1] > best_obj):
            best_obj = res[1]
            best_clusters = [clusters_row.copy(), clusters_col.copy()]
            best_perm = [perm_row.copy(), perm_col.copy()]
            print('Improved objective value:', res[1])
       else: print('Cannot improve current solution')

    #shake columns
    matrix = algorithms.shaking_col(matrix, m, p, perm_col)

    #local search column
    res = 0
    while(res != - 1):
        res = algorithms.local_search_move_col(matrix, n1, m, p, clusters_row, clusters_col, perm_col)
        if (res != -1):
          matrix = res[0]
          clusters_row = res[2]
          clusters_col = res[3]
          if (res[1] > best_obj):
              best_obj = res[1]
              best_clusters = [clusters_row.copy(), clusters_col.copy()]
              best_perm = [perm_row.copy(), perm_col.copy()]
              print('Improved objective value:', res[1])
        else: print('Cannot improve current solution')

    #shake split
    res = algorithms.shaking_split(clusters_row, clusters_col, N)
    if (res != -1):
        clusters_row, clusters_col = res
        N = N + 1
    else: print('Cannot split clusters')

    #local search split
    res = 0
    while(res != - 1):
        res = algorithms.local_search_split_cluster(matrix, n1, m, p, clusters_row, clusters_col, N)
        if (res != -1):
          matrix = res[0]
          clusters_row = res[2]
          clusters_col = res[3]
          if (res[1] > best_obj):
              best_obj = res[1]
              best_clusters = [clusters_row.copy(), clusters_col.copy()]
              best_perm = [perm_row.copy(), perm_col.copy()]
              print('Improved objective value:', res[1])
              N = N + 1
        else: print('Cannot improve current solution')

    #shake union
    res = algorithms.shaking_union(clusters_row, clusters_col, N)
    if (res != -1):
        clusters_row, clusters_col = res
        N = N - 1
    else: print('Cannot union clusters')

    #local search split
    res = 0
    while(res != - 1):
        res = algorithms.local_search_union_clusters(matrix, n1, m, p, clusters_row, clusters_col, N)
        if (res != -1):
          matrix = res[0]
          clusters_row = res[2]
          clusters_col = res[3]
          if (res[1] > best_obj):
              best_obj = res[1]
              best_clusters = [clusters_row.copy(), clusters_col.copy()]
              best_perm = [perm_row.copy(), perm_col.copy()]
              print('Improved objective value:', res[1])
              N = N - 1
        else: print('Cannot improve current solution')
import lab_2.util as util

# TODO Deprecated. Remove

# this function changes matrix, does not change clusters -> matrix, perm_row are renewed
# clusters are constant and used only to find objective function
def by_rows(matrix, n1, m, p, clusters_row, clusters_col, perm_row):
    curr_obj = util.calc_obj_val(matrix, n1, clusters_row, clusters_col)
    for i in range(m - 1):
        for j in range(i + 1, m):
            new_matrix = util.swap_rows(matrix, i, j, perm_row)
            new_obj = util.calc_obj_val(new_matrix, n1, clusters_row, clusters_col)
            if (new_obj > curr_obj): return new_matrix, new_obj, clusters_row, clusters_col
    return None


# this function changes matrix, does not change clusters -> matrix, perm_col are renewed
# clusters are constant and used only to find objective function
def by_columns(matrix, n1, m, p, clusters_row, clusters_col, perm_col):
    curr_obj = util.calc_obj_val(matrix, n1, clusters_row, clusters_col)
    for i in range(p - 1):
        for j in range(i + 1, p):
            new_matrix = util.swap_cols(matrix, i, j, perm_col)
            new_obj = util.calc_obj_val(new_matrix, n1, clusters_row, clusters_col)
            if (new_obj > curr_obj): return new_matrix, new_obj, clusters_row, clusters_col
    return -1


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
# matrix is constant and used only to find objective
def by_clusters_splitting(matrix, n1, m, p, clusters_row, clusters_col, current_number_of_clusters):
    curr_obj = util.calc_obj_val(matrix, n1, clusters_row, clusters_col)
    N = current_number_of_clusters
    for i in range(1, N + 1):
        res = util.split_clusters(clusters_row, clusters_col, N, i)
        if (res != -1):
            new_row, new_col = res
            new_obj = util.calc_obj_val(matrix, n1, new_row, new_col)
            if (new_obj > curr_obj): return matrix, new_obj, new_row, new_col
    return -1


# this function changes clusters, does not change matrix -> clusters_row, clusters_col are renewed
# matrix is constant and used only to find objective
def by_clusters_union(matrix, n1, m, p, clusters_row, clusters_col, current_number_of_clusters):
    curr_obj = util.calc_obj_val(matrix, n1, clusters_row, clusters_col)
    new_row = clusters_row.copy()
    new_col = clusters_col.copy()
    N = current_number_of_clusters
    for i in range(1, N):
        res = util.union_two_clusters(clusters_row, clusters_col, N, i)
        if (res != -1):
            new_row, new_col = res
            new_obj = util.calc_obj_val(matrix, n1, new_row, new_col)
            if (new_obj > curr_obj): return matrix, new_obj, new_row, new_col
    return -1
